/* =========================================================
   Latin Site: student accounts server (Google Apps Script).
   Paste this whole file into the Apps Script editor of a Google Sheet. See server/SETUP.md.

   What it stores, all in the owner's Google Drive:
     - Sheet "Classes":  class code, class name, level, created
     - Sheet "Students": class code, login, password hash + salt, progress file id, created
     - Folder "Latin Site progress": one JSON file per student with their flashcard
       progress and activity (flashcard answers, grammar pages opened, game scores).
   No real names, emails or other personal details are stored.

   The site talks to this script with POST requests whose body is JSON (sent as text/plain,
   so browsers don't need a CORS preflight). Every reply is JSON: { ok:true, ... } or { ok:false, error }.
   ========================================================= */

const FOLDER_NAME = 'Latin Site progress';
const STUDENT_TOKEN_DAYS = 180;      // a student stays signed in on a device for up to this long
const TEACHER_TOKEN_DAYS = 7;
const MAX_EVENTS = 4000;             // activity kept per student (oldest dropped first)
const MAX_FAILS = 8, LOCK_MINUTES = 15;
const MAX_STUDENTS_PER_CALL = 60;

/* ---------- menu and setup ---------- */
function onOpen(){
  SpreadsheetApp.getUi().createMenu('Latin Site')
    .addItem('Set up, or change the teacher password', 'setTeacherPassword')
    .addToUi();
}

function setTeacherPassword(){
  const ui = SpreadsheetApp.getUi();
  const r = ui.prompt('Teacher password', 'Choose the password for the teacher dashboard (at least 10 characters). Students never see it.', ui.ButtonSet.OK_CANCEL);
  if(r.getSelectedButton() !== ui.Button.OK) return;
  const pw = r.getResponseText();
  if(pw.length < 10){ ui.alert('Please use at least 10 characters.'); return; }
  const props = PropertiesService.getScriptProperties();
  if(!props.getProperty('SECRET')) props.setProperty('SECRET', Utilities.getUuid() + Utilities.getUuid());
  const salt = Utilities.getUuid();
  props.setProperty('TEACHER', salt + ':' + sha256_(salt + ':' + pw));
  sheets_(); folder_();
  ui.alert('Saved. Next, deploy the web app: Deploy → New deployment → Web app (see the setup guide).');
}

/* ---------- web entry points ---------- */
function doGet(){ return json_({ ok:true, service:'latin-site-accounts', v:1 }); }

function doPost(e){
  let req;
  try{ req = JSON.parse(e.postData.contents); }catch(err){ return json_({ ok:false, error:'bad-request' }); }
  try{
    const fn = ACTIONS[req.action];
    if(!fn) return json_({ ok:false, error:'unknown-action' });
    return json_(fn(req));
  }catch(err){
    const msg = String(err && err.message || err);
    // an expired or forged token, or a lock that timed out because many students saved at once
    return json_({ ok:false, error: msg === 'signed-out' ? 'signed-out' : /lock/i.test(msg) ? 'busy' : msg });
  }
}

const ACTIONS = {
  // ----- students -----
  signin(req){
    const code = normCode_(req.code), login = normLogin_(req.login);
    if(!code || !login) return { ok:false, error:'login' };
    if(locked_('s:' + code + '/' + login)) return { ok:false, error:'locked' };
    const cls = findClass_(code);
    if(!cls){ fail_('s:' + code + '/' + login); return { ok:false, error:'code' }; }
    const st = findStudent_(code, login);
    if(!st || sha256_(st.salt + ':' + String(req.pw || '')) !== st.hash){ fail_('s:' + code + '/' + login); return { ok:false, error:'login' }; }
    clearFails_('s:' + code + '/' + login);
    return { ok:true, token: makeToken_('s', code, login, STUDENT_TOKEN_DAYS),
             login: st.login, code: cls.code, cls: cls.name, level: cls.level, data: readData_(st.fileId) };
  },
  me(req){
    const t = checkToken_(req.token, 's'), st = findStudent_(t.c, t.l);
    if(!st) return { ok:false, error:'signed-out' };
    return { ok:true, data: readData_(st.fileId) };
  },
  sync(req){
    const t = checkToken_(req.token, 's');
    return withLock_(() => {
      const st = findStudent_(t.c, t.l);
      if(!st) return { ok:false, error:'signed-out' };
      const data = readData_(st.fileId);
      mergeStore_(data.store, req.set || {});
      const seen = {};
      data.events.slice(-1000).forEach(ev => { if(ev.id) seen[ev.id] = true; });
      (req.events || []).forEach(ev => {
        if(!ev || typeof ev !== 'object' || seen[ev.id]) return;
        data.events.push(cleanEvent_(ev)); seen[ev.id] = true;
      });
      data.events.sort((a, b) => a.t - b.t);
      if(data.events.length > MAX_EVENTS) data.events.splice(0, data.events.length - MAX_EVENTS);
      data.last = data.events.length ? data.events[data.events.length - 1].t : data.last || 0;
      writeData_(st.fileId, data);
      return { ok:true };
    });
  },

  // ----- teacher -----
  teacherLogin(req){
    if(locked_('teacher')) return { ok:false, error:'locked' };
    const saved = PropertiesService.getScriptProperties().getProperty('TEACHER');
    if(!saved) return { ok:false, error:'not-set-up' };
    const [salt, hash] = saved.split(':');
    if(sha256_(salt + ':' + String(req.pw || '')) !== hash){ fail_('teacher'); return { ok:false, error:'login' }; }
    clearFails_('teacher');
    return { ok:true, token: makeToken_('t', '', '', TEACHER_TOKEN_DAYS) };
  },
  classes(req){
    checkToken_(req.token, 't');
    const students = rows_('Students');
    return { ok:true, classes: rows_('Classes').map(c => ({ code:c.code, name:c.name, level:c.level, created:c.created,
      students: students.filter(s => normCode_(s.code) === normCode_(c.code)).length })) };
  },
  createClass(req){
    checkToken_(req.token, 't');
    return withLock_(() => {
      const taken = {}; rows_('Classes').forEach(c => taken[normCode_(c.code)] = true);
      let code; do { code = pick_(CODE_WORDS) + '-' + (10 + Math.floor(Math.random() * 90)); } while(taken[normCode_(code)]);
      const level = Math.max(1, Math.min(4, parseInt(req.level, 10) || 1));
      sheets_().classes.appendRow([code, String(req.name || 'Class').slice(0, 80), level, new Date()]);
      return { ok:true, code, roster: addStudents_(code, req.n) };
    });
  },
  addStudents(req){
    checkToken_(req.token, 't');
    return withLock_(() => {
      const cls = findClass_(normCode_(req.code)); if(!cls) return { ok:false, error:'code' };
      return { ok:true, roster: addStudents_(cls.code, req.n) };
    });
  },
  resetPassword(req){
    checkToken_(req.token, 't');
    return withLock_(() => {
      const st = findStudent_(normCode_(req.code), normLogin_(req.login)); if(!st) return { ok:false, error:'login' };
      const password = freshPassword_({}), salt = Utilities.getUuid();
      const sh = sheets_().students;
      sh.getRange(st.row, 3, 1, 2).setValues([[sha256_(salt + ':' + password), salt]]);
      clearFails_('s:' + normCode_(st.code) + '/' + normLogin_(st.login));
      return { ok:true, password };
    });
  },
  deleteClass(req){
    checkToken_(req.token, 't');
    return withLock_(() => {
      const code = normCode_(req.code), sh = sheets_();
      const studs = rows_('Students').filter(s => normCode_(s.code) === code).sort((a, b) => b.row - a.row);
      studs.forEach(s => { try{ DriveApp.getFileById(s.fileId).setTrashed(true); }catch(e){} sh.students.deleteRow(s.row); });
      rows_('Classes').filter(c => normCode_(c.code) === code).sort((a, b) => b.row - a.row).forEach(c => sh.classes.deleteRow(c.row));
      return { ok:true };
    });
  },
  classData(req){
    checkToken_(req.token, 't');
    const cls = findClass_(normCode_(req.code)); if(!cls) return { ok:false, error:'code' };
    const progress = {}, students = [];
    rows_('Students').filter(s => normCode_(s.code) === normCode_(cls.code)).forEach(s => {
      students.push(s.login); progress[s.login] = readData_(s.fileId);
    });
    return { ok:true, cls:{ code:cls.code, name:cls.name, level:cls.level, students }, progress };
  },
};

/* ---------- names and passwords ---------- */
const NAMES = [
  'Gaius','Lucius','Marcus','Quintus','Titus','Aulus','Decimus','Gnaeus','Publius','Servius','Sextus','Tiberius','Appius','Numerius',
  'Livia','Julia','Cornelia','Claudia','Tullia','Aemilia','Valeria','Octavia','Fabia','Sulpicia','Lucretia','Antonia','Flavia','Junia',
  'Agathon','Aspasia','Chloe','Daphne','Demetrius','Eudora','Hector','Iris','Kleon','Leander','Lysander','Melissa','Nikias','Phaedra',
  'Sappho','Theron','Xanthe','Zeno','Penelope','Ariadne','Philon','Thais','Kallias','Ione','Myron','Thalia',
  'Hamilcar','Hannibal','Hanno','Hasdrubal','Himilco','Mago','Elissa','Sophonisba','Bomilcar','Adherbal','Gisco','Maharbal','Imilce','Dido','Batbaal','Arishat'
];
// [noun, gender]; adjectives as [masculine, feminine, neuter], so the password's adjective agrees with its noun
const NOUNS = [
  ['lupus','m'],['ursus','m'],['corvus','m'],['leo','m'],['equus','m'],['taurus','m'],['cervus','m'],['piscis','m'],['delphinus','m'],
  ['cygnus','m'],['gladius','m'],['murus','m'],['hortus','m'],['ventus','m'],['mons','m'],['sol','m'],['fluvius','m'],['ignis','m'],
  ['aquila','f'],['columba','f'],['vulpes','f'],['noctua','f'],['apis','f'],['rosa','f'],['silva','f'],['stella','f'],['luna','f'],
  ['navis','f'],['turris','f'],['unda','f'],['insula','f'],['via','f'],['villa','f'],['corona','f'],['lucerna','f'],['arbor','f'],
  ['bellum','n'],['caelum','n'],['donum','n'],['saxum','n'],['scutum','n'],['templum','n'],['oppidum','n'],['flumen','n'],
  ['mare','n'],['iter','n'],['aurum','n'],['ovum','n'],['pomum','n'],['signum','n'],['vinum','n'],['tectum','n']
];
const ADJS = [
  ['ferox','ferox','ferox'],['velox','velox','velox'],['audax','audax','audax'],['felix','felix','felix'],['ingens','ingens','ingens'],
  ['fortis','fortis','forte'],['brevis','brevis','breve'],['gravis','gravis','grave'],['levis','levis','leve'],['dulcis','dulcis','dulce'],
  ['acer','acris','acre'],['celer','celeris','celere'],
  ['magnus','magna','magnum'],['parvus','parva','parvum'],['laetus','laeta','laetum'],['clarus','clara','clarum'],['aureus','aurea','aureum'],
  ['niger','nigra','nigrum'],['albus','alba','album'],['ruber','rubra','rubrum'],['viridis','viridis','viride'],['altus','alta','altum'],
  ['novus','nova','novum'],['longus','longa','longum'],['latus','lata','latum'],['bonus','bona','bonum'],['carus','cara','carum'],
  ['durus','dura','durum'],['firmus','firma','firmum'],['validus','valida','validum'],['placidus','placida','placidum'],['tacitus','tacita','tacitum'],
  ['antiquus','antiqua','antiquum'],['benignus','benigna','benignum'],['candidus','candida','candidum'],['fulvus','fulva','fulvum'],
  ['geminus','gemina','geminum'],['lentus','lenta','lentum'],['mirus','mira','mirum'],['plenus','plena','plenum'],['purus','pura','purum'],
  ['rarus','rara','rarum'],['serenus','serena','serenum'],['siccus','sicca','siccum'],['tutus','tuta','tutum'],['vivus','viva','vivum'],
  ['primus','prima','primum'],['summus','summa','summum'],['asper','aspera','asperum'],['liber','libera','liberum']
];
const CODE_WORDS = ['FORUM','VESTA','TIBER','AQUILA','LUPA','ROMA','OSTIA','CAPUA','JANUS','MINERVA','LYRA','PHAROS','DELOS','TYRUS','SIDON','UTICA','ITHACA','NAXOS','CUMAE','PAESTUM'];

function pick_(a){ return a[Math.floor(Math.random() * a.length)]; }
function freshPassword_(used){
  for(let i = 0; i < 1000; i++){
    const n = pick_(NOUNS), a = pick_(ADJS), pw = n[0] + a[{ m:0, f:1, n:2 }[n[1]]];
    if(!used[pw]){ used[pw] = true; return pw; }
  }
  return pick_(NOUNS)[0] + Math.floor(100 + Math.random() * 900);
}
function addStudents_(code, n){
  n = Math.max(1, Math.min(MAX_STUDENTS_PER_CALL, parseInt(n, 10) || 1));
  const taken = {}; rows_('Students').filter(s => normCode_(s.code) === normCode_(code)).forEach(s => taken[normLogin_(s.login)] = true);
  const pool = NAMES.filter(x => !taken[normLogin_(x)]).sort(() => Math.random() - 0.5);
  const sh = sheets_().students, folder = folder_(), roster = [], used = {}, rowsOut = [];
  for(let i = 0; roster.length < n; i++){
    const base = pool.length ? pool[i % pool.length] : pick_(NAMES);
    const login = (i < pool.length) ? base : base + (Math.floor(i / Math.max(1, pool.length)) + 1);
    if(taken[normLogin_(login)]) continue;
    taken[normLogin_(login)] = true;
    const password = freshPassword_(used), salt = Utilities.getUuid();
    const file = folder.createFile(normCode_(code) + '__' + normLogin_(login) + '.json', JSON.stringify(emptyData_()), 'application/json');
    rowsOut.push([code, login, sha256_(salt + ':' + password), salt, file.getId(), new Date()]);
    roster.push({ login, password });
  }
  if(rowsOut.length) sh.getRange(sh.getLastRow() + 1, 1, rowsOut.length, rowsOut[0].length).setValues(rowsOut);
  return roster;   // plain passwords are returned once, here, and never stored
}

/* ---------- progress files ---------- */
function emptyData_(){ return { store:{}, events:[], last:0 }; }
function readData_(id){
  try{ const d = JSON.parse(DriveApp.getFileById(id).getBlob().getDataAsString()); d.store = d.store || {}; d.events = d.events || []; return d; }
  catch(e){ return emptyData_(); }
}
function writeData_(id, data){ DriveApp.getFileById(id).setContent(JSON.stringify(data)); }

// Spaced-repetition cards merge one by one (the more recently studied copy wins), so two devices never overwrite each other.
function newer_(a, b){ return !b || (a.t == null ? -1 : a.t) > (b.t == null ? -1 : b.t) || ((a.t == null ? -1 : a.t) === (b.t == null ? -1 : b.t) && (a.r || 0) > (b.r || 0)); }
function mergeStore_(store, set){
  Object.keys(set).forEach(k => {
    if(!/^(srs|fc:[\w:.\/-]{1,80})$/.test(k)) return;               // only flashcard keys are accepted
    const v = set[k];
    if(k === 'srs' && v && v.cards){
      const cur = store.srs && store.srs.cards ? store.srs : { v:1, cards:{}, newLog:{} };
      Object.keys(v.cards).forEach(c => { if(newer_(v.cards[c], cur.cards[c])) cur.cards[c] = v.cards[c]; });
      Object.keys(v.newLog || {}).forEach(s => {
        const a = v.newLog[s], b = cur.newLog[s];
        if(!b || a.day > b.day || (a.day === b.day && a.n > b.n)) cur.newLog[s] = a;
      });
      store.srs = cur;
    } else store[k] = v;
  });
}
function cleanEvent_(ev){
  const out = {}, keep = ['id','t','k','d','c','la','g','v','p','title','s','of'];
  keep.forEach(k => { if(ev[k] !== undefined) out[k] = typeof ev[k] === 'string' ? ev[k].slice(0, 160) : ev[k]; });
  out.t = Number(out.t) || Date.now();
  return out;
}

/* ---------- sheets ---------- */
function sheets_(){
  const ss = SpreadsheetApp.getActive();
  let c = ss.getSheetByName('Classes'), s = ss.getSheetByName('Students');
  if(!c){ c = ss.insertSheet('Classes'); c.appendRow(['code','name','level','created']); c.setFrozenRows(1); }
  if(!s){ s = ss.insertSheet('Students'); s.appendRow(['code','login','password hash','salt','progress file','created']); s.setFrozenRows(1); }
  return { classes:c, students:s };
}
function rows_(name){
  const sh = sheets_()[name === 'Classes' ? 'classes' : 'students'], vals = sh.getDataRange().getValues();
  const out = [];
  for(let i = 1; i < vals.length; i++){
    const r = vals[i];
    if(name === 'Classes') out.push({ row:i + 1, code:String(r[0]), name:String(r[1]), level:Number(r[2]) || 1, created:r[3] });
    else out.push({ row:i + 1, code:String(r[0]), login:String(r[1]), hash:String(r[2]), salt:String(r[3]), fileId:String(r[4]) });
  }
  return out;
}
function findClass_(code){ return rows_('Classes').filter(c => normCode_(c.code) === code)[0] || null; }
function findStudent_(code, login){ return rows_('Students').filter(s => normCode_(s.code) === code && normLogin_(s.login) === login)[0] || null; }
function folder_(){
  const props = PropertiesService.getScriptProperties(), id = props.getProperty('FOLDER');
  if(id){ try{ return DriveApp.getFolderById(id); }catch(e){} }
  const f = DriveApp.createFolder(FOLDER_NAME); props.setProperty('FOLDER', f.getId()); return f;
}

/* ---------- tokens, hashing, rate limits ---------- */
function normCode_(c){ return String(c || '').toUpperCase().replace(/[^A-Z0-9]/g, ''); }
function normLogin_(l){ return String(l || '').trim().toLowerCase(); }
function sha256_(s){
  return Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, s, Utilities.Charset.UTF_8)
    .map(b => ((b + 256) % 256).toString(16).padStart(2, '0')).join('');
}
function secret_(){
  const props = PropertiesService.getScriptProperties();
  let s = props.getProperty('SECRET'); if(!s){ s = Utilities.getUuid() + Utilities.getUuid(); props.setProperty('SECRET', s); }
  return s;
}
function sign_(body){ return Utilities.base64EncodeWebSafe(Utilities.computeHmacSha256Signature(body, secret_())); }
function makeToken_(role, code, login, days){
  const body = Utilities.base64EncodeWebSafe(JSON.stringify({ r:role, c:code, l:login, e:Date.now() + days * 864e5 }));
  return body + '.' + sign_(body);
}
function checkToken_(token, role){
  const parts = String(token || '').split('.');
  if(parts.length !== 2 || sign_(parts[0]) !== parts[1]) throw new Error('signed-out');
  const t = JSON.parse(Utilities.newBlob(Utilities.base64DecodeWebSafe(parts[0])).getDataAsString());
  if(t.r !== role || t.e < Date.now()) throw new Error('signed-out');
  return t;
}
function locked_(key){ return Number(CacheService.getScriptCache().get('fail:' + key) || 0) >= MAX_FAILS; }
function fail_(key){ const c = CacheService.getScriptCache(), n = Number(c.get('fail:' + key) || 0) + 1; c.put('fail:' + key, String(n), LOCK_MINUTES * 60); }
function clearFails_(key){ CacheService.getScriptCache().remove('fail:' + key); }
function withLock_(fn){
  const lock = LockService.getScriptLock();
  lock.waitLock(25000);
  try{ return fn(); } finally { lock.releaseLock(); }
}
function json_(o){ return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
