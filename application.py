import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, list_to_string

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///penandpaper.db")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user and create world"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Please provide a username!", 400)
        username = request.form.get("username")

        # Ensure username is not taken
        rows = db.execute("SELECT * FROM worlds WHERE username=:username",
                          username=username)
        if len(rows) != 0:
            return apology("That username is taken, try again!", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("Please provide a password!", 400)
        password = request.form.get("password")

        # Ensure password contains at least 6 letters and 2 numbers (personal touch)
        letter_counter = 0
        number_counter = 0
        for i in range(len(password)):
            if password[i].isalpha():
                letter_counter += 1
            if password[i].isdigit():
                number_counter += 1
        if letter_counter < 6 or number_counter < 2:
            return apology("Your password must contain at least 6 letters and 2 numbers.", 400)

        # Ensure password confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("Please confirm your password!", 400)
        confirmation = request.form.get("confirmation")

        # Ensure password and password confirmation match
        if password != confirmation:
            return apology("Those passwords don't match, try again!", 400)

        # Hash password
        password_hashed = generate_password_hash(password)

        # Ensure worldname was submitted
        if not request.form.get("worldname"):
            return apology("Please name your world!", 400)
        worldname = request.form.get("worldname")

        # Ensure location was submitted
        if not request.form.get("location"):
            return apology("Please provide a location for your world!", 400)
        location = request.form.get("location")

        # Ensure time period was submitted
        if not request.form.get("timeperiod"):
            return apology("Please provide a time period for your world!", 400)
        timeperiod = request.form.get("timeperiod")

        # Ensure genre was selected
        if not request.form.get("genre"):
            return apology("Please select a genre for your world!", 400)
        genre = request.form.get("genre")

        # Insert new user/world into worlds table
        db.execute("INSERT INTO worlds (username, hash, worldname, location, timeperiod, genre) VALUES (:username, :hash, :worldname, :location, :timeperiod, :genre)",
                   username=username,
                   hash=password_hashed,
                   worldname=worldname,
                   location=location,
                   timeperiod=timeperiod,
                   genre=genre)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query table for username
        rows = db.execute("SELECT * FROM worlds WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/editworld", methods=["GET", "POST"])
@login_required
def editworld():
    """Edit world"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Load existing world information
        world = db.execute("SELECT * FROM worlds WHERE id = :id",
                           id=session["user_id"])
        world = world[0]

        # Ensure worldname was submitted
        if not request.form.get("worldname"):
            return apology("Please name your world!", 400)
        worldname = request.form.get("worldname")

        # Ensure location was submitted
        if not request.form.get("location"):
            return apology("Please provide a location for your world!", 400)
        location = request.form.get("location")

        # Ensure time period was submitted
        if not request.form.get("timeperiod"):
            return apology("Please provide a time period for your world!", 400)
        timeperiod = request.form.get("timeperiod")

        # Ensure genre was selected
        if not request.form.get("genre"):
            return apology("Please select a genre for your world!", 400)
        genre = request.form.get("genre")

        # Update worlds table
        db.execute("UPDATE worlds SET worldname = :worldname, location = :location, timeperiod = :timeperiod, genre = :genre WHERE id = :id",
                   worldname=worldname,
                   location=location,
                   timeperiod=timeperiod,
                   genre=genre,
                   id=session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        world = db.execute("SELECT * FROM worlds WHERE id = :id",
                           id=session["user_id"])
        return render_template("editworld.html", world=world)


@app.route("/deleteworld", methods=["GET", "POST"])
@login_required
def deleteworld():
    """Delete world"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Delete world
        db.execute("DELETE FROM worlds WHERE id = :id",
                   id=session["user_id"])

        # Clear from all other tables
        db.execute("DELETE FROM stories WHERE world_id = :world_id",
                   world_id=session["user_id"])
        db.execute("DELETE FROM characters WHERE world_id = :world_id",
                   world_id=session["user_id"])
        db.execute("DELETE FROM timeline WHERE world_id = :world_id",
                   world_id=session["user_id"])
        db.execute("DELETE FROM storycharacters WHERE world_id = :world_id",
                   world_id=session["user_id"])
        db.execute("DELETE FROM storytimeline WHERE world_id = :world_id",
                   world_id=session["user_id"])
        db.execute("DELETE FROM charactertimeline WHERE world_id = :world_id",
                   world_id=session["user_id"])

        # Redirect user to login page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        world = db.execute("SELECT * FROM worlds WHERE id = :id",
                           id=session["user_id"])
        return render_template("editworld.html", world=world)


@app.route("/")
@login_required
def index():
    """Generate world portal"""

    # Get username and world basic info
    world = db.execute("SELECT * FROM worlds WHERE id = :id",
                       id=session["user_id"])

    # Get list of stories
    stories = db.execute("SELECT * FROM stories WHERE world_id = :world_id ORDER BY title ASC",
                         world_id=session["user_id"])

    # Get list of characters
    characters = db.execute("SELECT * FROM characters WHERE world_id = :world_id ORDER BY name ASC",
                            world_id=session["user_id"])

    # Get timeline
    timeline = db.execute("SELECT * FROM timeline WHERE world_id = :world_id ORDER BY date ASC",
                          world_id=session["user_id"])

    # Get story and character information relevant to each timeline entry
    for entry in timeline:
        entry_id = entry["id"]
        this_entries_characters_temp = db.execute("SELECT * FROM characters WHERE id IN (SELECT character_id FROM charactertimeline WHERE timeline_id = :timeline_id)",
                                                  timeline_id=entry_id)
        this_entries_stories_temp = db.execute("SELECT * FROM stories WHERE id IN (SELECT story_id FROM storytimeline WHERE timeline_id = :timeline_id)",
                                               timeline_id=entry_id)
        chars = []
        entry_stories = []
        for c in this_entries_characters_temp:
            chars.append(c["name"])
        for s in this_entries_stories_temp:
            entry_stories.append(s["title"])

        entry["chars"] = list_to_string(chars)
        entry["stories"] = list_to_string(entry_stories)

    # Return HTML table
    return render_template("index.html", world=world, stories=stories, characters=characters, timeline=timeline)


@app.route("/createstory", methods=["GET", "POST"])
@login_required
def createstory():
    """Create new story"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Loop over all characters
        characters = db.execute("SELECT * FROM characters WHERE world_id = :world_id ORDER BY name ASC",
                                world_id=session["user_id"])

        # Ensure story title was submitted
        if not request.form.get("title"):
            return apology("Please provide a title for your story!", 400)
        title = request.form.get("title")

        # Ensure abstract was submitted
        if not request.form.get("abstract"):
            return apology("Please provide a few lines describing your story!", 400)
        abstract = request.form.get("abstract")

        # Ensure genre was selected
        if not request.form.get("genre"):
            return apology("Please select a genre for your story!", 400)
        genre = request.form.get("genre")

        # Ensure outline was submitted
        if not request.form.get("outline"):
            return apology("Please provide an outline for your story!", 400)
        outline = request.form.get("outline")

        # (Optional) location, time, link, embed, notes
        location = request.form.get("location")
        time = request.form.get("time")
        link = request.form.get("link")
        embed = request.form.get("embed")
        notes = request.form.get("notes")

        # Insert new story into stories table
        new_story = db.execute("INSERT INTO stories (title, abstract, location, time, genre, link, embed, notes, outline, world_id) VALUES (:title, :abstract, :location, :time, :genre, :link, :embed, :notes, :outline, :world_id)",
                               title=title,
                               abstract=abstract,
                               location=location,
                               time=time,
                               genre=genre,
                               link=link,
                               embed=embed,
                               notes=notes,
                               outline=outline,
                               world_id=session["user_id"])

        # Look up checked characters in characters table
        for character in characters:
            character_name = character["name"]
            if request.form.get(character_name) == "1":
                checked_character = db.execute("SELECT * FROM characters WHERE name = :character_name AND world_id = :world_id",
                                               character_name=character_name,
                                               world_id=session["user_id"])
                checked_character = checked_character[0]["id"]

                # Insert checked characters into storycharacters table
                db.execute("INSERT INTO storycharacters (story_id, character_id, world_id) VALUES (:story_id, :character_id, :world_id)",
                           story_id=new_story,
                           character_id=checked_character,
                           world_id=session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        characters = db.execute("SELECT name FROM characters WHERE world_id = :world_id",
                                world_id=session["user_id"])
        return render_template("createstory.html", characters=characters)


@app.route("/story", methods=["GET"])
@login_required
def story():
    """Generate story page"""

    # User reached route via GET (as by clicking a link)
    title = request.args.get("title")

    # Get story information from stories table
    story = db.execute("SELECT * FROM stories WHERE title = :title AND world_id = :world_id",
                       title=title,
                       world_id=session["user_id"])
    story_id = story[0]["id"]
    story = story[0]
    if story["location"] == '':
        story["location"] = "none"
    if story["time"] == '':
        story["time"] = "none"

    # Get characters from storycharacters table
    characters = db.execute("SELECT * FROM characters WHERE id IN (SELECT character_id FROM storycharacters WHERE story_id = :story_id) ORDER BY name ASC",
                            story_id=story_id)

    # Get timeline from storytimeline table
    timeline = db.execute("SELECT * FROM timeline WHERE id IN (SELECT timeline_id FROM storytimeline WHERE story_id = :story_id) ORDER BY date",
                          story_id=story_id)

    # assert story[0]["title"] == title

    return render_template("story.html", story=story, characters=characters, timeline=timeline)


@app.route("/editstory", methods=["GET", "POST"])
@login_required
def editstory():
    """Edit existing story"""

    # User reached route via GET (as by clicking a link)
    if request.method == "GET":

        title = request.args.get("title")

        # Load existing story information
        story = db.execute("SELECT * FROM stories WHERE title = :title AND world_id = :world_id",
                           title=title,
                           world_id=session["user_id"])
        story_id = story[0]["id"]
        story = story[0]

        # Loop over all characters
        characters = db.execute("SELECT name FROM characters WHERE world_id = :world_id",
                                world_id=session["user_id"])

        return render_template("editstory.html", story=story, characters=characters)

    # User reached route via POST (as by submitting a form via POST)
    else:

        # Identify story
        story_id = request.form.get("id")

        # Ensure story title was submitted
        if not request.form.get("title"):
            return apology("Please provide a title for your story!", 400)
        title = request.form.get("title")

        # Ensure abstract was submitted
        if not request.form.get("abstract"):
            return apology("Please provide a few lines describing your story!", 400)
        abstract = request.form.get("abstract")

        # Ensure genre was selected
        if not request.form.get("genre"):
            return apology("Please select a genre for your story!", 400)
        genre = request.form.get("genre")

        # Ensure outline was submitted
        if not request.form.get("outline"):
            return apology("Please provide an outline for your story!", 400)
        outline = request.form.get("outline")

        # (Optional) location, time, link, embed, notes
        location = request.form.get("location")
        time = request.form.get("time")
        link = request.form.get("link")
        embed = request.form.get("embed")
        notes = request.form.get("notes")

        # Update stories table
        db.execute("UPDATE stories SET title = :title, abstract = :abstract, location = :location, time = :time, genre = :genre, link = :link, embed = :embed, notes = :notes, outline = :outline WHERE id = :id",
                   title=title,
                   abstract=abstract,
                   location=location,
                   time=time,
                   genre=genre,
                   link=link,
                   embed=embed,
                   notes=notes,
                   outline=outline,
                   id=story_id)

        # Clear pre-existing checked characters from storycharacters table
        db.execute("DELETE FROM storycharacters WHERE story_id = :story_id",
                   story_id=story_id)

        # Get characters (again)
        characters = db.execute("SELECT name FROM characters WHERE world_id = :world_id",
                                world_id=session["user_id"])

        # Look up checked characters in characters table
        for character in characters:
            character_name = character["name"]
            if request.form.get(character_name) == "1":
                checked_character = db.execute("SELECT * FROM characters WHERE name = :character_name AND world_id = :world_id",
                                               character_name=character_name,
                                               world_id=session["user_id"])
                checked_character = checked_character[0]["id"]

                # Create new checked characters in storycharacters table
                db.execute("INSERT INTO storycharacters (story_id, character_id, world_id) VALUES (:story_id, :character_id, :world_id)",
                           story_id=story_id,
                           character_id=checked_character,
                           world_id=session["user_id"])

        # Redirect user to home page
        return redirect("/")


@app.route("/deletestory", methods=["POST"])
@login_required
def deletestory():
    """Delete story"""

    # User reached route via POST (as by submitting a form via POST)

    # Identify story
    story_id = request.form.get("id")

    # Delete story
    db.execute("DELETE FROM stories WHERE id = :id",
               id=story_id)

    # Clear from all other tables
    db.execute("DELETE FROM storycharacters WHERE story_id = :story_id",
               story_id=story_id)
    db.execute("DELETE FROM storytimeline WHERE story_id = :story_id",
               story_id=story_id)

    # Redirect user to home page
    return redirect("/")


@app.route("/createcharacter", methods=["GET", "POST"])
@login_required
def createcharacter():
    """Create new character"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure character name was submitted
        if not request.form.get("name"):
            return apology("Please provide a name for your character!", 400)
        name = request.form.get("name")

        # Ensure key attributes were submitted
        if not request.form.get("highlights"):
            return apology("Please provide your character's key attributes/characteristics!", 400)
        highlights = request.form.get("highlights")

        # Ensure birthday was submitted
        if not request.form.get("bday"):
            return apology("Please provide your character's birthday!", 400)
        bday = request.form.get("bday")

        # Ensure gender was submitted
        if not request.form.get("gender"):
            return apology("Please provide your character's gender!", 400)
        gender = request.form.get("gender")

        # Ensure nationality/ethnicity was submitted
        if not request.form.get("nateth"):
            return apology("Please provide your character's nationality/ethnicity!", 400)
        nateth = request.form.get("nateth")

        # Ensure place of origin was submitted
        if not request.form.get("home"):
            return apology("Please provide your character's place of origin!", 400)
        home = request.form.get("home")

        # Ensure physical description was submitted
        if not request.form.get("phys"):
            return apology("Please provide a physical description for your character!", 400)
        phys = request.form.get("phys")

        # Ensure personality was submitted
        if not request.form.get("pers"):
            return apology("Please provide a personality description for your character!", 400)
        pers = request.form.get("pers")

        # Ensure career/position was submitted
        if not request.form.get("job"):
            return apology("Please provide your character's career/position!", 400)
        job = request.form.get("job")

        # Ensure skills/talents/hobbies were submitted
        if not request.form.get("acts"):
            return apology("Please provide your character's skills/talents/hobbies!", 400)
        acts = request.form.get("acts")

        # (Optional) notes
        other = request.form.get("notes")

        # Insert new character into characters table
        db.execute("INSERT INTO characters (name, highlights, gender, bday, nateth, home, phys, pers, job, acts, other, world_id) VALUES (:name, :highlights, :gender, :bday, :nateth, :home, :phys, :pers, :job, :acts, :other, :world_id)",
                   name=name,
                   highlights=highlights,
                   gender=gender,
                   bday=bday,
                   nateth=nateth,
                   home=home,
                   phys=phys,
                   pers=pers,
                   job=job,
                   acts=acts,
                   other=other,
                   world_id=session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("createcharacter.html")


@app.route("/character", methods=["GET"])
@login_required
def character():
    """Generate character bio page"""

    # User reached route via GET (as by clicking a link)
    name = request.args.get("name")

    # Get character information from characters table
    character = db.execute("SELECT * FROM characters WHERE name = :name AND world_id = :world_id",
                           name=name,
                           world_id=session["user_id"])
    character_id = character[0]["id"]
    character = character[0]

    # Get stories from storycharacters table
    stories = db.execute("SELECT * FROM stories WHERE id IN (SELECT story_id FROM storycharacters WHERE character_id = :character_id)",
                         character_id=character_id)

    # Get timeline from charactertimeline table
    timeline = db.execute("SELECT * FROM timeline WHERE id IN (SELECT timeline_id FROM charactertimeline WHERE character_id = :character_id)",
                          character_id=character_id)

    return render_template("character.html", character=character, stories=stories, timeline=timeline)


@app.route("/editcharacter", methods=["GET", "POST"])
@login_required
def editcharacter():
    """Edit existing character"""

    # User reached route via GET (as by clicking a link)
    if request.method == "GET":

        name = request.args.get("name")

        # Load existing character information
        character = db.execute("SELECT * FROM characters WHERE name = :name AND world_id = :world_id",
                               name=name,
                               world_id=session["user_id"])
        character_id = character[0]["id"]
        character = character[0]

        return render_template("editcharacter.html", character=character)

    # User reached route via POST (as by submitting a form via POST)
    else:

        # Identify character
        character_id = request.form.get("id")

        # Ensure character name was submitted
        if not request.form.get("name"):
            return apology("Please provide a name for your character!", 400)
        name = request.form.get("name")

        # Ensure key attributes were submitted
        if not request.form.get("highlights"):
            return apology("Please provide your character's key attributes/characteristics!", 400)
        highlights = request.form.get("highlights")

        # Ensure birthday was submitted
        if not request.form.get("bday"):
            return apology("Please provide your character's birthday!", 400)
        bday = request.form.get("bday")

        # Ensure gender was submitted
        if not request.form.get("gender"):
            return apology("Please provide your character's gender!", 400)
        gender = request.form.get("gender")

        # Ensure nationality/ethnicity was submitted
        if not request.form.get("nateth"):
            return apology("Please provide your character's nationality/ethnicity!", 400)
        nateth = request.form.get("nateth")

        # Ensure place of origin was submitted
        if not request.form.get("home"):
            return apology("Please provide your character's place of origin!", 400)
        home = request.form.get("home")

        # Ensure physical description was submitted
        if not request.form.get("phys"):
            return apology("Please provide a physical description for your character!", 400)
        phys = request.form.get("phys")

        # Ensure personality was submitted
        if not request.form.get("pers"):
            return apology("Please provide a personality description for your character!", 400)
        pers = request.form.get("pers")

        # Ensure career/position was submitted
        if not request.form.get("job"):
            return apology("Please provide your character's career/position!", 400)
        job = request.form.get("job")

        # Ensure skills/talents/hobbies were submitted
        if not request.form.get("acts"):
            return apology("Please provide your character's skills/talents/hobbies!", 400)
        acts = request.form.get("acts")

        # (Optional) notes
        other = request.form.get("notes")

        # Update characters table
        db.execute("UPDATE characters SET name = :name, highlights = :highlights, gender = :gender, bday = :bday, nateth = :nateth, home = :home, phys = :phys, pers = :pers, job = :job, acts = :acts, other = :other WHERE id = :id",
                   name=name,
                   highlights=highlights,
                   gender=gender,
                   bday=bday,
                   nateth=nateth,
                   home=home,
                   phys=phys,
                   pers=pers,
                   job=job,
                   acts=acts,
                   other=other,
                   id=character_id)

        # Redirect user to home page
        return redirect("/")


@app.route("/deletecharacter", methods=["POST"])
@login_required
def deletecharacter():
    """Delete character"""

    # User reached route via POST (as by submitting a form via POST)

    # Identify character
    character_id = request.form.get("id")

    # Delete character
    db.execute("DELETE FROM characters WHERE id = :id",
               id=character_id)

    # Clear from all other tables
    db.execute("DELETE FROM storycharacters WHERE character_id = :character_id",
               character_id=character_id)
    db.execute("DELETE FROM charactertimeline WHERE character_id = :character_id",
               character_id=character_id)

    # Redirect user to home page
    return redirect("/")


@app.route("/timeline", methods=["GET", "POST"])
@login_required
def timeline():
    """Add new entry to timeline"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Loop over all characters
        characters = db.execute("SELECT name FROM characters WHERE world_id = :world_id ORDER BY name ASC",
                                world_id=session["user_id"])

        # Loop over all stories
        stories = db.execute("SELECT title FROM stories WHERE world_id = :world_id ORDER BY title ASC",
                             world_id=session["user_id"])

        # Ensure event was submitted
        if not request.form.get("event"):
            return apology("Please provide an event!", 400)
        event = request.form.get("event")

        # Ensure date was submitted
        if not request.form.get("date"):
            return apology("Please provide a date!", 400)
        date = request.form.get("date")

        # Insert new entry into timeline table
        new_entry = db.execute("INSERT INTO timeline (event, date, world_id) VALUES (:event, :date, :world_id)",
                               event=event,
                               date=date,
                               world_id=session["user_id"])

        # Look up checked characters in characters table
        for character in characters:
            character_name = character["name"]
            if request.form.get(character_name) == "1":
                checked_character = db.execute("SELECT * FROM characters WHERE name = :character_name AND world_id = :world_id",
                                               character_name=character_name,
                                               world_id=session["user_id"])
                checked_character = checked_character[0]["id"]

                # Insert checked characters into charactertimeline table
                db.execute("INSERT INTO charactertimeline (character_id, timeline_id, world_id) VALUES (:character_id, :timeline_id, :world_id)",
                           character_id=checked_character,
                           timeline_id=new_entry,
                           world_id=session["user_id"])

        # Look up checked stories in stories table
        for story in stories:
            story_title = story["title"]
            if request.form.get(story_title) == "1":
                checked_story = db.execute("SELECT * FROM stories WHERE title = :story_title AND world_id = :world_id",
                                           story_title=story_title,
                                           world_id=session["user_id"])
                checked_story = checked_story[0]["id"]

                # Insert checked stories into storytimeline table
                db.execute("INSERT INTO storytimeline (story_id, timeline_id, world_id) VALUES (:story_id, :timeline_id, :world_id)",
                           story_id=checked_story,
                           timeline_id=new_entry,
                           world_id=session["user_id"])

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        characters = db.execute("SELECT name FROM characters WHERE world_id = :world_id",
                                world_id=session["user_id"])
        stories = db.execute("SELECT title FROM stories WHERE world_id = :world_id",
                             world_id=session["user_id"])
        return render_template("timeline.html", characters=characters, stories=stories)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
