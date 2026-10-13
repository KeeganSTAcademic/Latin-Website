# Student accounts: setting up the Google back end

The site stays on GitHub Pages. Student progress is saved by a small Google Apps Script that runs in your own Google account and writes to a Google Sheet and a Drive folder. Nothing else is needed: no server and no payment.

## What it stores

- **Sheet "Classes":** class code, class name, level, date created.
- **Sheet "Students":** class code, login (an invented name), password hash and salt, the ID of the student's progress file, date created.
- **Drive folder "Latin Site progress":** one JSON file per student, named like `FORUM27__hamilcar.json`, holding their flashcard progress and activity (flashcard answers, grammar pages opened, game scores, with times).

No real names, emails or other personal details are stored. Passwords are stored only as salted hashes, so not even the Sheet shows them. Real-name labels typed on the teacher dashboard stay in that browser.

## Setting it up (about 10 minutes)

1. **Make the Sheet.** In Google Drive, create a new Google Sheet and name it something like *Latin Site accounts*.
2. **Add the script.** In the Sheet, choose **Extensions → Apps Script**. Delete the sample code in `Code.gs`, paste in the whole of `server/Code.gs` from the repo, and click **Save**.
3. **Set the teacher password.** Go back to the Sheet and reload it. A **Latin Site** menu appears after a few seconds. Choose **Latin Site → Set up, or change the teacher password**.
   - Google first asks you to authorize the script. Because it's your own script and not a published app, Google shows "Google hasn't verified this app". Click **Advanced → Go to (project name)**, then **Allow**. The script asks for access to the Sheet and to Drive files it creates.
   - Choose a password of at least 10 characters. This is the password for the teacher dashboard. The script also creates the two tabs and the Drive folder.
4. **Deploy it as a web app.** In the Apps Script editor, choose **Deploy → New deployment**. Click the gear next to "Select type" and choose **Web app**. Set:
   - **Execute as:** Me
   - **Who has access:** Anyone

   Click **Deploy** and copy the **Web app URL** (it ends in `/exec`).
   "Anyone" means the site can reach the script without students signing in to Google. Every action still needs a student password or the teacher password.
5. **Check it.** Paste the URL into a browser. You should see `{"ok":true,"service":"latin-site-accounts","v":1}`.
6. **Point the site at it.** In the repo, create `data/account-config.json`:

   ```json
   { "api": "https://script.google.com/macros/s/…/exec" }
   ```

   Then add `<script src="../js/account.js?v=…"></script>` right after `common.js` on the pages that should save progress (the flashcards page, the grammar pages and, later, the games). Without the config file the site runs the browser-only demo.
7. **Make a class.** Open the site's `teacher/` page, sign in with the teacher password, choose **New class**, and print the sign-in slips.

## Changing the script later

Paste the new code, save, then choose **Deploy → Manage deployments**, click the pencil on the existing deployment, set **Version** to **New version**, and click **Deploy**. This keeps the same URL. (A *new* deployment gets a new URL, which would mean editing `account-config.json`.)

## Everyday notes

- **Lost password:** use **Reset password** on the student's row. The new password is shown once.
- **Wrong passwords:** after 8 wrong tries, that login (or the teacher sign-in) is locked for 15 minutes.
- **Signing everyone out:** in the Apps Script editor, open **Project Settings → Script properties** and delete `SECRET`. All student and teacher sign-ins stop working, and everyone signs in again. Progress is kept.
- **Deleting a class:** removes its rows from the Sheet and moves its progress files to the Drive trash, where Google keeps them for 30 days.
- **Backups:** the Sheet has version history (File → Version history). The progress folder can be downloaded from Drive at any time.
- **How saving works:** the site saves a student's changes in batches, every 20 seconds while they practise and whenever they leave a page. If the connection drops, changes wait on the computer and are sent later. Signing out sends anything still waiting first; if it can't, the student stays signed in and is told why.
- **Limits:** a free Google account runs up to 30 copies of the script at once, and each request is short, so a class practising together is well within it. Saves to one Sheet happen one at a time; if many arrive at once, a few wait and retry on their own.
- **School filters:** check that `script.google.com` and `script.googleusercontent.com` are reachable on school Chromebooks. They usually are, because schools use Google.
