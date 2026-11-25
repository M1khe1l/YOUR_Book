import os
import uuid
import re
import sqlite3
from cs50 import SQL
from flask import Flask, jsonify, flash, redirect, render_template,  url_for, request, session
import random
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from datetime import datetime

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Password validator
def is_valid_password(password):
    # Password must contain at least one digit, one lowercase, one uppercase, and be at least 8 characters
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$"
    return re.match(pattern, password)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///blog.db")

# link recognition
def contains_link(content):
    url_pattern = r'(https?://[^\s]+)'
    if re.search(url_pattern, content):
        return True
    return False

# data rendering format
@app.template_filter("datetimeformat")
def datetimeformat(value):
    dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%Y-%b-%d")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config['CKEDITOR_SERVE_LOCAL'] = True  # Serve the updated local or CDN version

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


# public page
@app.route("/public")
def public():

    published_posts = db.execute("SELECT * FROM posts WHERE is_public = 1 ORDER BY created_at DESC")

    if "user_id" not in session:
        return render_template("public_index.html", published_posts=published_posts, hide_left_panel=True)

    posts = db.execute("SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC", session["user_id"])
    public_posts = db.execute("SELECT * FROM posts WHERE user_id = ? AND is_public = 1 ORDER BY created_at DESC", session["user_id"])
    users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    user = users[0]
    saved_posts = db.execute("SELECT * FROM saved WHERE user_id = ?", session["user_id"])
    return render_template("public_index.html", posts=posts, public_posts=public_posts, saved_posts=saved_posts, published_posts=published_posts, user=user, hide_left_panel=True)


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/public")

    posts = db.execute("SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC", session["user_id"])
    public_posts = db.execute("SELECT * FROM posts WHERE user_id = ? AND is_public = 1 ORDER BY created_at DESC", session["user_id"])
    users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    user = users[0]
    saved_posts = db.execute("SELECT * FROM saved WHERE user_id = ?", session["user_id"])
    return render_template("profile.html", posts=posts, public_posts=public_posts, saved_posts=saved_posts, user=user)


@app.route("/upload_profile_image", methods=["POST"])
def upload_profile_image():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    if "profile_image" not in request.files:
        flash("No file selected.")
        return redirect("/profile")

    file = request.files["profile_image"]
    if file.filename == "":
        flash("No file selected.")
        return redirect("/profile")

    filename = secure_filename(file.filename)
    filepath = os.path.join("static/uploads", filename)
    file.save(filepath)

    db.execute("UPDATE users SET profile_image = ? WHERE id = ?", filepath, user_id)
    flash("Profile image updated successfully.")
    return redirect("/profile")

# User Profile Update
@app.route("/update_profile", methods=["POST"])
def update_profile():
    if "user_id" not in session:
        return redirect("/login")

    # Query database for username and password
    names = db.execute("SELECT username FROM users")
    rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    user_id = session["user_id"]
    username = request.form.get("username")
    old_password = request.form.get("old_password")

    if username:
        if username == rows[0]["username"]:
            # Username is the same; skip updating username
            pass
        elif username in names:
            flash("Username already exists, try another name")
            return redirect("/profile")
        else:
            # Update username in the database
            db.execute("UPDATE users SET username = ? WHERE id = ?", username, user_id)

    if old_password:
        # Ensure user exists and old password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], old_password):
            flash("Please Enter Old Password Correctly")
            return redirect("/profile")

        new_password = request.form.get("new_password")
        confirm = request.form.get("confirm")
        if not is_valid_password(new_password):
            flash("Password must contain at least one uppercase letter, one lowercase letter, one number, and be at least 8 characters long.")
            return redirect("/profile")

        # Ensure password was confirmed
        if new_password != confirm:
            flash("Please Confirm New Password")
            return redirect("/profile")

        # Update password in the database
        hashed_password = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE id = ?", hashed_password, user_id)

    flash("Profile updated successfully.")
    return redirect("/profile")


@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/public")

    posts = db.execute("SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC", session["user_id"])
    public_posts = db.execute("SELECT * FROM posts WHERE user_id = ? AND is_public = 1 ORDER BY created_at DESC", session["user_id"])
    users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    user = users[0]
    saved_posts = db.execute("SELECT * FROM saved WHERE user_id = ?", session["user_id"])

    return render_template("index.html", posts=posts, public_posts=public_posts, saved_posts=saved_posts, user=user)


@app.route ("/search")
def search():
    q = request.args.get("search")
    if not q:
        return redirect("/public")

    posts = db.execute("SELECT * FROM posts WHERE is_public = 1 AND title LIKE ? ORDER BY created_at DESC", f"%{q}%")
    if len(posts) == 0:
        flash("No Such Note found")
        return redirect("/public")

    if "user_id" not in session:
        return render_template("search.html", posts=posts, q=q)

    public_posts = db.execute("SELECT * FROM posts WHERE user_id = ? AND is_public = 1 ORDER BY created_at DESC", session["user_id"])
    users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    user = users[0]
    saved_posts = db.execute("SELECT * FROM saved WHERE user_id = ?", session["user_id"])
    return render_template("search.html", posts=posts, public_posts=public_posts, saved_posts=saved_posts, q=q, user=user, hide_left_panel=True)

@app.route("/post")
def post():
    post = db.execute("SELECT * FROM posts WHERE id = ?", request.args.get("post_id"))
    if not post:
        flash("Post not found")
        return redirect("/")

    if "user_id" not in session:
        return render_template("public_post.html", post=post[0])

    users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    user = users[0]
    saved_posts = db.execute("SELECT * FROM saved WHERE user_id = ?", session["user_id"])
    posts = db.execute("SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC", session["user_id"])
    public_posts = db.execute("SELECT * FROM posts WHERE user_id = ? AND is_public = 1 ORDER BY created_at DESC", session["user_id"])

    if session["user_id"] != post[0]["user_id"]:
        saved = False
        if "user_id" in session:
            saved = db.execute("SELECT * FROM saved WHERE user_id = ? AND post_id = ?", session["user_id"], post[0]["id"])
        return render_template("public_post.html", post=post[0], posts=posts, public_posts=public_posts, saved_posts=saved_posts, user=user, saved=bool(saved), hide_left_panel=True)

    return render_template("post.html", post=post[0], posts=posts, public_posts=public_posts, saved_posts=saved_posts, user=user)


# Handle Privacy Updates with Toggle Switch
@app.route("/toggle_privacy", methods=["POST"])
def toggle_privacy():
    if "user_id" not in session:
        return jsonify({"success": False, "error": "User not logged in."}), 403

    data = request.get_json()
    post_id = data.get("post_id")
    is_public = data.get("is_public")

    if not post_id:
        return jsonify({"success": False, "error": "Invalid post ID."}), 400

    # Update the privacy status in the database
    try:
        db.execute("UPDATE posts SET is_public = ? WHERE id = ?", is_public, post_id)
        if not is_public:
            db.execute("DELETE FROM saved WHERE post_id = ?", post_id)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Save Toggle Putton
@app.route("/toggle_save", methods=["POST"])
def toggle_save():
    if "user_id" not in session:
        return jsonify({"success": False, "error": "User not logged in"}), 403

    user_id = session["user_id"]
    data = request.get_json()
    post_id = data.get("post_id")
    post_title = db.execute("SELECT title FROM posts WHERE id = ?", post_id)

    if not post_id:
        return jsonify({"success": False, "error": "Post ID missing"}), 400

    # Check if the post is already saved
    saved = db.execute("SELECT * FROM saved WHERE user_id = ? AND post_id = ?", user_id, post_id)
    if saved:
        # Remove from saved
        db.execute("DELETE FROM saved WHERE user_id = ? AND post_id = ?", user_id, post_id)
        return jsonify({"success": True, "action": "unsaved"})
    else:
        # Add to saved
        db.execute("INSERT INTO saved (user_id, post_id, title) VALUES (?, ?, ?)", user_id, post_id, post_title[0]["title"])
        return jsonify({"success": True, "action": "saved"})


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return render_template("login.html")


        # Ensure password was submitted
        if not request.form.get("password"):
            flash("must provide password")
            return render_template("login.html")


        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("invalid username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/public")

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Get the submitted username and password
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm")

        # Ensure username was submitted
        if not username:
            flash("enter username")
            return render_template("register.html")

        # Ensure password was submitted
        if not password:
            flash("enter Password")
            return render_template("register.html")

        if not is_valid_password(password):
            flash("Password must contain at least one uppercase letter, one lowercase letter, one number, and be at least 8 characters long.")
            return render_template("register.html")

        # Ensure password was confirmed
        if password != confirmation:
            flash("password does not match")
            return render_template("register.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username not exists
        if len(rows) > 0:
            flash("This username already exist, please try another username")
            return render_template("register.html")

        password_hash = generate_password_hash(password)

        # Insert the new user into the database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash)

        # fetch which user has logged in and put id in session
        row = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = row[0]["id"]

        # Redirect user to home page
        return redirect("/welcome")

    else:
        return render_template("register.html")

@app.route("/new", methods=["GET", "POST"])
def new_post():

    if "user_id" not in session:
        return redirect("/login")

    posts = db.execute("SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC", session["user_id"])
    public_posts = db.execute("SELECT * FROM posts WHERE user_id = ? AND is_public = 1 ORDER BY created_at DESC", session["user_id"])
    users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    user = users[0]
    saved_posts = db.execute("SELECT * FROM saved WHERE user_id = ?", session["user_id"])

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        author = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])

        # Handle file upload
        image_file = request.files.get('image_file')
        image_url = None
        if image_file and allowed_file(image_file.filename):
            # Generate a unique filename using a timestamp and UUID
            extension = image_file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}.{extension}"
            # filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(file_path)
            # Use the file path in database
            image_url = file_path
        try:
             # Use parameterized queries to safely insert data
            if not image_file:
                # Insert into the database
                db.execute("INSERT INTO posts (user_id, author, title, content) VALUES (?, ?, ?, ?)",
                            session["user_id"], author[0]["username"], title, content)
            else:
                # Insert into the database
                db.execute("INSERT INTO posts (user_id, author, title, content, image_url) VALUES (?, ?, ?, ?, ?)",
                            session["user_id"], author[0]["username"], title, content, image_url)
            # Fetch the ID of the newly created post
            new_post_id = db.execute("SELECT last_insert_rowid() AS id")[0]["id"]

            # Fetch the newly created post
            new_post = db.execute("SELECT * FROM posts WHERE id = ?", new_post_id)[0]

            flash("Post created successfully!")
            return render_template("post.html", posts=posts, public_posts=public_posts, saved_posts=saved_posts, user=user, post=new_post)

        except sqlite3.Error as e:
            flash(f"An error occurred: {e}", "error")
            return redirect("/new")

    return render_template("new_post.html", posts=posts, public_posts=public_posts, saved_posts=saved_posts, user=user)


@app.route("/edit", methods=["GET", "POST"])
def edit_post():
    if "user_id" not in session:
        return redirect("/login")

    # POST
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        # Handle file upload
        image_file = request.files.get('image_file')
        image_url = None
        if image_file and allowed_file(image_file.filename):
            # Generate a unique filename using a timestamp and UUID
            extension = image_file.filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}.{extension}"
            # filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(file_path)
            # Use the file path in your database
            image_url = file_path

        # update database
        try:
            if not image_file:
                db.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?",
                    title, content, request.form.get("post_id"))
            else:
                db.execute("UPDATE posts SET title = ?, content = ?, image_url = ? WHERE id = ?",
                        title, content, image_url, request.form.get("post_id"))

            flash("Post Updated Successfully")
            return redirect("/")

        except sqlite3.Error as e:
            flash(f"An error occurred: {e}", "error")
            return redirect("/new")

    # GET
    if request.method == "GET":
        post = db.execute("SELECT * FROM posts WHERE id = ?", request.args.get("post_id"))
        if not post:
            flash("could not find post")
            return redirect("/")

        users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        user = users[0]
        posts = db.execute("SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC", session["user_id"])
        public_posts = db.execute("SELECT * FROM posts WHERE user_id = ? AND is_public = 1 ORDER BY created_at DESC", session["user_id"])
        saved_posts = db.execute("SELECT * FROM saved WHERE user_id = ?", session["user_id"])
        return render_template("edit.html", post=post[0], posts=posts, public_posts=public_posts, saved_posts=saved_posts, user=user)


@app.route("/welcome")
def welcome():
    if "user_id" not in session:
        return redirect("/login")

    posts = db.execute("SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC", session["user_id"])
    public_posts = db.execute("SELECT * FROM posts WHERE user_id = ? AND is_public = 1 ORDER BY created_at DESC", session["user_id"])
    users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    user = users[0]
    saved_posts = db.execute("SELECT * FROM saved WHERE user_id = ?", session["user_id"])
    return render_template("welcome.html", posts=posts, public_posts=public_posts, saved_posts=saved_posts, user=user)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # While we do not use server, it just flashes success message, to imitate the sending message
        flash("Your message is sent, Thanks For contacting us")
        return redirect("/contact")

    if request.method == "GET":
        if "user_id" in session:
            users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
            user = users[0]
            posts = db.execute("SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC", session["user_id"])
            public_posts = db.execute("SELECT * FROM posts WHERE user_id = ? AND is_public = 1 ORDER BY created_at DESC", session["user_id"])
            saved_posts = db.execute("SELECT * FROM saved WHERE user_id = ?", session["user_id"])
            return render_template("contact.html", posts=posts, public_posts=public_posts, saved_posts=saved_posts, user=user)
        else:
            return render_template("contact.html")


@app.route("/delete", methods=["POST"])
def delete_post():
    post_id = request.form.get("post_id")
    # check if post_id
    if not post_id:
        flash("post not found")
        return redirect("/")

    # delete post from database
    db.execute("DELETE FROM saved WHERE post_id = ?", post_id)
    db.execute("DELETE FROM posts WHERE id = ? AND user_id = ?", post_id, session["user_id"])
    flash("Post Deleted Successfully")
    return redirect("/")

# DELETE USER ACCOUNT FROM database
@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":
        password = request.form.get("password")
        users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        delete_posts = request.form.get("delete_posts")

        # Check if there is only 1 user
        if len(users) != 1:
            flash("Critical Error, Something went wrong, please try again later")
            return redirect("/profile")

        if not password:
            flash("Please enter your password")
            return redirect("/delete_account")

        # Ensure password is correct
        if not check_password_hash(users[0]["hash"], password):
            flash("Password does not match, try again")
            return redirect("/delete_account")

        # DELETE User Information and Posts from database
        db.execute("DELETE FROM saved WHERE user_id = ?", session["user_id"])
        posts = db.execute("SELECT * FROM posts WHERE user_id = ?", session["user_id"])

        if delete_posts == "yes":
            post_ids = [post["id"] for post in posts]
            if post_ids:  # Proceed only if there are posts
                db.execute(f"DELETE FROM saved WHERE post_id IN ({','.join(['?']*len(post_ids))})", *post_ids)
            db.execute("DELETE FROM posts WHERE user_id = ?", session["user_id"])

        else:
            post_ids = [post["id"] for post in posts]
            if post_ids:  # Proceed only if there are posts
                db.execute(f"UPDATE posts SET user_id = NULL WHERE id IN ({','.join(['?']*len(post_ids))})", *post_ids)
                db.execute("DELETE FROM posts WHERE user_id = NULL AND is_public = false")

        # Delete user from users
        db.execute("DELETE FROM users WHERE id = ?", session["user_id"])
        # Forget any user_id
        session.clear()
        # Redirect user to login form
        flash("Your account is deleted")
        return redirect("/public")

    if request.method == "GET":
        users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        user = users[0]
        posts = db.execute("SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC", session["user_id"])
        public_posts = db.execute("SELECT * FROM posts WHERE user_id = ? AND is_public = 1 ORDER BY created_at DESC", session["user_id"])
        saved_posts = db.execute("SELECT * FROM saved WHERE user_id = ?", session["user_id"])
        return render_template("delete_account.html", posts=posts, public_posts=public_posts, saved_posts=saved_posts, user=user)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to public form
    return redirect("/public")
