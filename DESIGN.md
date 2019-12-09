# Design Documentation for Pen&Paper #
---
This document provides an overview of the implementation and design of Pen&Paper. Since Pen&Paper critically relies on the design and use of multiple SQL tables, this document will primarily examine each SQL table as a way of explaining the implementation of each feature on the website and the design decisions made. This document will also provide a concise, convenient summary of each *feature's* design and implementation, as well as the style components. In order:

1. SQL table walkthrough
2. Feature overview
3. A few words on style

Firstly, the program is structured as follows:

---

### Program Structure ###

The directory `penandpaper/` contains two folders, `static/` and `template/s`, and 3 core files (excluding `README.md` and `DESIGN.md`): `application.py`, `helpers.py`, and `penandpaper.db`. The other 3 files (`README.md`, `DESIGN.md`, and `planningdoc.txt`) are text-based files meant to aid in understanding the program - they do not function in the program itself.

`application.py` and `helpers.py` contain the Python code used in Pen&Paper. `templates/` contains the 13 HTML files that are accessed throughout `application.py`, and `penandpaper.db` contains the 7 SQL tables created for Pen&Paper.

*All code in application.py and helpers.py is thoroughly commented so as to aid in easily understanding their function.*

*All functions mentioned below are defined in `application.py` unless otherwise noted.*

---
### SQL tables ###

The first stage of the project involved creating the SQL tables that would facilitate the implementation of the features later on. In general order of implementation:

##### worlds #####
The `worlds` table contains each world's unique identifying `id`, the user's `username`, hashed password `hash`, `worldname`, world `location`, world `timeperiod`, world `genre`, and automatic `timestamp`. `id` is referenced as foreign key `world_id` in every other SQL database.

`id` is used to query select all characters and stories within a world to display as checkable options in the **Create Story** (`createstory.html`) and **Timeline** (`timeline.html`) pages. `id` is also used to populate the **Edit World** (`editworld.html`) page and facilitate the UPDATE and DELETE queries on that page.
*When a world is deleted as via `/deleteworld`, any entry in any other table containing `world_id` is simultaneously deleted as well.*

`username`, `hash`, `worldname`, `location`, `timeperiod`, and `genre` are user inputs that are inserted into `worlds` in the **Register** process (`register.html`), which generates `id` in the first place. These user-inputted fields plus `timestamp` are query selected from `worlds` to display on the **Portal** page (`index.html`) when `/` is called. `username` and `hash` are obviously also used to check the validity of an attempted login with **Log In** (`login.html`).

Note that the world's `id` is referenced in every `db.execute` query not already referencing either a story's `id` or a character's `id` (both of which correspond to SQL table rows containing the foreign key `world_id`) to protect against the possibility of identically-named stories or characters being pulled from other worlds. This was a specific design decision implemented after the discovery of a bug that confused identically-named stories from other worlds.

##### stories #####
The `stories` table contains each story's unique identifying `id`, the story's `title`, `abstract`, `location`, `time`, `genre`, editable `link`, published link `embed`, `notes`, `outline`, automatic `timestamp`, and foreign key `world_id`. `id` is referenced as foreign key `story_id` in tables `storycharacters` and `storytimeline`.

A story is created via the **Create Story** (`createstory.html`) page when `/createstory` is called, inserting user-inputted `title`, `abstract`, `location`, `time`, `genre`, `link`, `embed`, `notes`, and `outline` into the `stories` table. `title` is used to query select the story matching the title of the hyperlink clicked when `/story` is called, populating the individual story's page (`story.html`). `title` is also used to populate the **Edit Story** page (`editstory.html`). A hidden form input containing the story's `id` is used to facilitate the UPDATE and DELETE queries on that page.

`stories` is queried in `/` (`index.html`) to populate the "Stories" table in **Portal**. It is also queried via its link to the `storytimeline` table to populate the stories relevant to each timeline entry in "Timeline", and is queried via its link to the `storycharacters` table to populate the stories relevant to a character on that character's profile page (`character.html`). `stories` is referenced on the **Timeline** (`timeline.html`) page to populate a checkbox list of all stories in that world, after which checked stories are inserted into the `storytimeline` table via `/timeline`.

##### characters #####
The `characters` table contains each character's unique identifying `id`, the character's `name`, character `highlights`, character's `gender`, birthday `bday`, character's nationality/ethnicity `nateth`, character's place of origin `home`, character's physical description `phys`, personality `pers`, skills/hobbies/talents `acts`, career/position `job`, notes `other`, automatic `timestamp`, and foreign key `world_id`. `id` is referenced as foreign key `character_id` in tables `storycharacters` and `charactertimeline`.

A character is created via the **Create Character** (`createcharacter.html`) page when `/createcharacter` is called, inserting user-inputted `name`, `highlights`, `gender`, `bday`, `nateth`, `home`, `phys`, `pers`, `acts`, `job`, and `other` into the `characters` table. `name` is used to query select the character matching the name of the hyperlink clicked when `/character` is called, populating the character's profile page (`character.html`). `name` is also used to populate the **Edit Character** page (`editcharacter.html`). A hidden form input containing the character's `id` is used to facilitate the UPDATE and DELETE queries on that page.

`characters` is queried in `/` (`index.html`) to populate the "Characters" table in **Portal**. It is also queried via its link to the `charactertimeline` table to populate the characters relevant to each timeline entry in "Timeline", and is queried via its link to the `storycharacters` table to populate the characters relevant to a story on that story's page (`story.html`). `characters` is referenced on the **Create Story** (`createstory.html`) page and likewise on the **Timeline** (`timeline.html`) page to populate a checkbox list of all characters in that world, after which checked characters are inserted into `storycharacters` and `charactertimeline` via `/createstory` and `/timeline`, respectively. `characters` is also referenced on the **Edit Story** page (`editstory.html`): when `/editstory` is called via POST, a query inserts new checked characters into `storycharacters` (after the originally checked characters have been deleted via query).

##### timeline #####
The `timeline` table contains each timeline entry's unique identifying `id`, the timeline `event`, `date`, `timestamp` (not displayed anywhere), and foreign key `world_id`. `id` is referenced as foreign key `timeline_id` in tables `storytimeline` and `charactertimeline`.

A timeline entry is created via the **Timeline** (`timeline.html`) page when `/timeline` is called, inserting user-inputted `event` and `date` into the `timeline` table.

`timeline` is queried in `/` (`index.html`) to populate the "Timeline" table in **Portal**. It is also queried via its link to the `storytimeline` table to populate the timeline entries relevant to a story on that story's page (`story.html`), and is queried via its link to the `charactertimeline` table to populate the timeline entries relevant to a character on that character's profile page (`character.html`).

##### storycharacters #####
The `storycharacters` table serves to link parent tables `stories` and `characters` via foreign keys `story_id` and `character_id`. It also contains a unique identifying `id` as well as foreign key `world_id`.

User-checked characters (or rather, their `character_id` and corresponding new `story_id`) are inserted into `storycharacters` on the **Create Story** (`createstory.html`) page when `/createstory` is called. The entries in `storycharacters` are indirectly referenced when `/story` is called in order to get character names to display on a story's page (`story.html`), and likewise when `/character` is called in order to get story titles to display on a character's profile page (`character.html`). Pre-existing checked characters are cleared from `storycharacters` on the **Edit Story** (`editstory.html`) page when `/editstory` is called via POST before newly checked characters are inserted.

When characters or stories are deleted via `/deletecharacter` (`editcharacter.html`) or `/deletestory` (`editstory.html`), any entries in `storycharacters` with foreign keys referencing those character or story `id`'s are simultaneously deleted.

##### storytimeline #####
The `storytimeline` table serves to link parent tables `stories` and `timeline` via foreign keys `story_id` and `timeline_id`. It also contains a unique identifying `id` as well as foreign key `world_id`.

`story_id` and `timeline_id` are inserted into `storytimeline` on **Timeline** (`timeline.html`) when `/timeline` is called via POST.
`storytimeline` is indirectly referenced when `/` (`index.html`) is called in order to get relevant stories to display in the appropriate timeline entry in "Timeline".

When a story is deleted via `/deletestory` (`editstory.html`), any entry in `storytimeline` with a foreign key referencing that story's `id` is deleted as well.

##### charactertimeline #####
The `charactertimeline` table serves to link parent tables `characters` and `timeline` via foreign keys `character_id` and `timeline_id`. It also contains a unique identifying `id` as well as foreign key `world_id`.

`character_id` and `timeline_id` are inserted into `charactertimeline` on **Timeline** (`timeline.html`) when `/timeline` is called via POST.
`charactertimeline` is indirectly referenced when `/` (`index.html`) is called in order to get relevant characters to display in the appropriate timeline entry in "Timeline".

When a character is deleted via `/deletecharacter` (`editcharacter.html`), any entry in `charactertimeline` with a foreign key referencing that character's `id` is deleted as well.

**Overall, Pen&Paper makes extensive use of linked parent and child SQL tables in order to easier facilitate the implementation of the web app's various, inherently linked features.**

---
### Features ###
*(roughly in order of implementation)*

##### Register #####
* Generates `register.html` when called via GET
* Inserts user input into `worlds` table when called via POST
* Redirects to **Log In**

##### Log In #####
* Generates `login.html` when called via GET
* Checks user input against `username` and `hash` in `worlds` table when called via POST
* Redirects to **Portal**

###### Log Out ######
* Redirects user to **Log In**

##### Edit World #####
* Generates `editworld.html` when called via GET
* When called via POST:
    * Selects relevant entry from `worlds`
    * Updates `worlds` table with user input
* Redirects to **Portal**

###### Delete World (via Edit World) ######
* Deletes relevant entry from `worlds` when called via POST
    * Deletes all entries with relevant `world_id` from `stories`, `characters`, `timeline`, `storycharacters`, `storytimeline`, `charactertimeline`
* Redirects to **Log In**
*The `/deleteworld` function is hosted on the same HTML page as `/editworld` so that the user is presented with the two closely related options on the same page. When `/deleteworld` is called, all table entries containing the world's `id` are deleted from all 7 SQL tables.*

##### Create Character #####
* Generates `createcharacter.html` when called via GET
* Inserts user input into `characters` when called via POST
* Redirects to **Portal**

##### Create Story #####
* Generates `createstory.html` when called via GET
    * Selects from `characters` to populate the page
* Inserts user input into `stories` table when called via POST
    * Inserts user-checked characters into `storycharacters`
* Redirects to **Portal**

##### Timeline #####
* Generates `timeline.html` when called via GET
    * Selects from `characters` and `stories` to populate the page
* Inserts user input into `timeline` when called via POST
    * Inserts user-checked characters and stories into `charactertimeline` and `storytimeline`, respectively
* Redirects to **Portal**

##### Portal #####
* Generates `index.html`
* Selects from `worlds`, `stories`, `characters`, `timeline` to display on page
    * Selects from `characters` and `stories` via `charactertimeline` and `storytimeline`, respectively (via new function `list_to_string` defined in `helpers.py`) to display in "Timeline"

##### Character (via Portal) #####
* Generates `character.html` when called via GET
* Selects from `characters`, `stories` (via `storycharacters`), and `timeline` (via `charactertimeline`) to populate the page

##### Edit Character (via Character) #####
* Generates `editcharacter.html` when called via GET
    * Selects from `characters` to populate the page
* Updates `characters` when called via POST

###### Delete Character (via Edit Character) ######
* Deletes relevant entry from `characters` when called via POST
    * Deletes all entries with relevant `character_id` from `storycharacters`, `charactertimeline`
* Redirects to **Portal**
*As with `/deleteworld`, the `/deletecharacter` function is hosted on the same HTML page as `/editcharacter` so that the user is presented with the two closely related options on the same page.*

##### Story (via Portal) #####
* Generates `story.html` when called via GET
* Selects from `stories`, `characters` (via `storycharacters`) and `timeline` (via `charactertimeline`) to populate the page

##### Edit Story (via Story) #####
* Generates `editstory.html` when called via GET
    * Selects from `stories` and `characters` to populate the page
* Updates user input in `stories` table when called via POST
    * Deletes originally checked characters from `storycharacters`
    * Inserts newly checked characters into `storycharacters`
* Redirects to **Portal**

###### Delete Story (via Edit Story) ######
* Deletes relevant entry from `stories` when called via POST
    * Deletes all entries with relevant `story_id` from `storycharacters`, `storytimeline`
* Redirects to **Portal**
*As with `/deleteworld` and `/deletecharacter`, the `/deletestory` function is hosted on the same HTML page as `/editstory` so that the user is presented with the two closely related options on the same page.*

---
### Style ###

The stylistic components of Pen&Paper can be found in `static/`, which stores two files:
1. `favicon-96x96.ico` is a favicon that I created using an online tool and then uploaded to CS50 IDE.
2. `styles.css` lists all CSS style elements used throughout Pen&Paper's HTML pages.

---
