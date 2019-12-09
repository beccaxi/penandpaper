# User's Manual for Pen&Paper #
---

This is a user's manual for Pen&Paper, a Flask web app hosted entirely on CS50 IDE.

Pen&Paper is a web app designed to be used as a story planning and world building tool for creative minds.
Users will be able to create "world portals" linked to a username and password. Each user has the ability to create as many usernames/worlds as they would like or delete them if they wish.
Within each world, users can create, edit, and delete stories and characters, as well as create a world timeline.
Users have the ability to link stories and characters to each other and to individual timeline entries, and to view each story/character in a separate page.

The website is extremely user-friendly, but this comprehensive guide breaks down the process of using Pen&Paper and explains each feature in full detail. Let's get started!

---

### Getting started: Open the web app ###

Pen&Paper is contained in a directory aptly titled `penandpaper/` (see *Appendix*). To run the program:

1. Open a terminal
2. Change into the directory as via `cd penandpaper`.
3. Run flask as via `flask run`.
4. Click on `https://c072f0e0-c234-4cd3-b0b6-f25c5f4d01d0-ide.cs50.xyz:8080/` to open Pen&Paper in your web browser.

You will be greeted by a login page.

---

## Getting started: Register, log in ##

If this is your first time using Pen&Paper, you must first create a user account/world.

#### Register: ####
1. Click **Register** in the navbar. You will be redirected to the Registration page.
2. Follow the instructions to create a username and password and submit basic information about your world. Every field is required. (World information can edited after registration.)
*Note that a user account is the same thing as a world. Each user account corresponds to a different world. By registering a user account, you are in fact creating a new world. This means that you can create multiple worlds or share a world with someone else by sharing the username and password corresponding to that world.*
3. After submitting all required fields, you will be redirected to the **Log In** page.

#### Log In: ####
After logging in successfully with your new username and password, you will be redirected to **Portal**.
You may log out at any time via the navbar, after which you may log back in with an existing username or create a new username/world via **Register**.

---

## "Portal", explained ##

If this is your first time logging on to Pen&Paper, read this section to understand what you are looking at in **Portal**.

**Portal** is the index/homepage for Pen&Paper. The navbar at the top is the navigation tool for the website via which you can create stories, characters, and timeline entries, as well as log out or edit your world (more on that below).

Below the navbar is a Jumbotron displaying your world's basic information as well as an introduction to Pen&Paper.
If you would like to contact the website's admin (me) for any reason, simply click the link to be redirected to an email application.

Below the Jumbotron are three tables:
1. "Stories" is a table displaying any stories that you have created (in alphabetical order), along with their summaries. You may click a story's title to be redirected to that story's page.
2. "Characters" is a table displaying any characters that you have created (in alphabetical order by first name), along with character highlights. You may click a character's name to be redirected to that character's profile page.
3. "Timeline" is a table displaying all timeline entries that you have created (in chronological order, of course), along with any characters or stories that you have indicated as relevant to each entry.

Let's explore the features that allow us to handle stories, characters, and timeline entries.

---

## Story: Create, edit, delete ##

Pen&Paper allows you to create, edit, and delete as many stories as you would like.

*If this is your first time using Pen&Paper, be aware that you may want to create your characters first before creating your stories.*

#### Create: ####
1. Click **Create Story** in the navbar. You will be redirected to the Create Story page.
2. Follow the instructions to create a new story, filling in all required text fields and checking off any characters that feature in your story.
*Note that "Link to document" asks for a Google Doc link ending in /edit, while "Embed document" asks you to insert a public link that can be found by going to "File" and then "Publish to the web" in your Google Doc.*
3. After submitting all required fields, you will be redirected to **Portal** where you will see your new story in the "Stories" table. Click on the story's title to view that story's page.

Each story's page contains a Jumbotron displaying your story's basic information, followed by an Edit button. Beneath the Jumbotron are:
1. "Story Outline" displays any information you submitted in the "Outline" field.
2. "Characters" displays any characters you checked off as relevant to your story. You may click a character's name to be redirected to that character's profile page.
3. "Timeline" displays any timeline entries that you indicated as relevant to your story (see **Timeline**).
4. If you submitted an /edit link in the "Link to document" field, you will see a hyperlink to your (editable) Google Doc followed by a frame containing the live document itself, where you can directly edit the document. If you submitted a /pub link in the "Embed document" field, you will see a frame containing a view-only version of your Google doc.

#### Edit/delete: ####
1. To edit or delete a story, go to that story's page and click **Edit your story here** at the bottom of the Jumbotron.
2. You may directly edit your story and save those changes by clicking "Save changes", after which you will be redirected to the **Portal**.
*Note that you must reselect any characters relevant to your story, regardless of whether you previously selected them or not.*
3. Alternatively, you may irreversibly delete your story (but not any characters and/or timeline entries associated with it) by clicking "Delete story forever", after which you will be redirected to the **Portal**.

---

## Character: Create, edit, delete ##

Pen&Paper allows you to create, edit, and delete as many characters as you would like.

#### Create: ####
1. Click **Create Character** in the navbar. You will be redirected to the Create Character page.
2. Follow the instructions to create a new character, filling in all required text fields.
3. After submitting all required fields, you will be redirected to **Portal** where you will see your new character in the "Characters" table. Click on the character's name to view that character's profile page.

Each character's page contains a Jumbotron displaying your character's basic information, followed by an Edit button. Beneath the Jumbotron are:
1. "Character Profile" displays the attributes you entered for the character.
2. "Stories" displays any stories that feature the character. You may click a story's title to be redirected to that story's page.
3. "Timeline" displays any timeline entries that you indicated as relevant to your character (see **Timeline**).

#### Edit/delete: ####
1. To edit or delete a character, go to that character's profile page and click **Edit your character here** at the bottom of the Jumbotron.
2. You may directly edit your character and save those changes by clicking "Save changes", after which you will be redirected to the **Portal**.
3. Alternatively, you may irreversibly delete your character (but not any stories and/or timeline entries associated with it) by clicking "Delete character forever", after which you will be redirected to the **Portal**.

---

## Timeline: Create ##

Pen&Paper allows you to create as many timeline entries as you would like. Editing or deleting timeline entries is currently not supported.

#### Create: ####
1. Click **Timeline** in the navbar. You will be redirected to the Timeline page.
2. Follow the instructions to create a new timeline entry, filling in all required text fields. Check off any characters and/or stories that are relevant to your new entry.
3. After submitting, you will be redirected to **Portal** where you will see your new entry in the "Timeline" table. The new entry will also appear on the pages of any characters or stories that you have indicated as relevant.

---

## Edit world ##

You may change your world's basic information at any time by clicking **Edit World** in the navbar. As with editing stories and characters, **Edit World** gives you two options:
1. You may directly edit your world's basic information and save those changes by clicking "Save changes", after which you will be redirected to the Portal.
2. Alternatively, you may irreversibly delete your world and all stories, characters, and timelines stored within it by clicking "Delete world forever", after which you will be redirected to the **Log In** page.

---

## Appendix: Structure ##

The directory `penandpaper/` contains two folders, `static/` and `templates/`, and 4 individual files (excluding `README.md` and `DESIGN.md`):

`static/` contains two files: `favicon-96x96.ico` is an .ico file containing the favicon displayed in the browser tab when Pen&Paper is run,
and `styles.css` is the CSS file containing all style elements for Pen&Paper's HTML code.

`templates/` contains the 13 HTML files used in Pen&Paper.

Files `application.py` and `helpers.py` contains all possible functions/routes used in Pen&Paper.

File `penandpaper.db` contains the 7 SQL tables used in Pen&Paper.

File `planningdoc.txt` is the text file used as an outline and guide throughout the making of Pen&Paper.

##### See `DESIGN.md` for an in-depth overview of Pen&Paper's structure and design. #####

---
