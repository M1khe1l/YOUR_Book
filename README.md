# YOUR BOOK
#### Video Demo:  [[ youtube_link](https://www.youtube.com/watch?v=WqpdWcGZsN8)]

#### Description:

 - A multi-user blogging platform where people write private notes, publish the ones they want to share, and save other people's published notes. Built with Flask, SQLite and Bootstrap as my final project for [CS50x](https://cs50.harvard.edu/x/).

## Design Choices:
- **Database Design:** Focused on modularity and flexibility, using separate tables for users, posts, and saved items.
- **Frontend Design:** Bootstrap was used for a responsive layout with custom CSS for finer control.
- **Security:** Used hashed passwords for user security.

## Features:
1. **User Registration and Authentication**
   - Supports password validation for secure account creation.

2. **User Profiles**
   - Customizable profiles with uploadable avatars and editable information. Also password reset functionality.

3. **Post Creation and Interaction**
   - Creating posts with thumbnail images and links.
   - Privacy controls to make posts public or private.
   - "Save" functionality for users to bookmark their favorite posts.

## Tech stack
Python 3 · Flask · Flask-Session (server-side sessions) · SQLite via the CS50 `SQL` library · Jinja2 · Bootstrap 5 · vanilla JavaScript (fetch API) · Font Awesome


## Run it locally
```bash
git clone https://github.com/M1khe1l/YOUR_Book.git
cd <YOUR_Book>

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

flask run
```

## Project structure
```
app.py              Flask routes and helpers
blog.db             Database (users, posts, saved)
requirements.txt    Python dependencies
templates/          Jinja templates; layout.html is the shared base
static/
  styles.css        Custom styles on top of Bootstrap
  blog.js           Password show/hide, scroll-to-top button
  uploads/          Thumbnails and avatar
```


## File Overview:
### **app.py**
   - The main Flask application file.
   - Contains routes for user registration, authentication, post management, and more.
### **blog.db**
| Table   | Purpose |
|---------|---------|
| `users` | id, unique username, password hash, optional avatar path |
| `posts` | id, owner, author name, title, content, image, created_at, `is_public` flag |
| `saved` | one row per (user, post) bookmark, unique together |
### **templates/**
   - Folder that contains all html files, used in the project.
   - #### 404.html
      - Custom Error html page for 404 error.
   - #### 500.html
      - Custom Error html page for 500 error.
   - #### contact.html
      - A page that allows the user to send a message to the support team. It also contains the company's contact information: email, phone, and address. Since I can't use a server for this project, it simply simulates sending a message.
   - #### delete_account.html
      - A page from which users can delete their account. Users can choose whether or not to delete their published notes along with their account. A password is required to delete an account.
   - #### edit.html
      - A page that allows users to edit a note they have written. This requires user authentication. Users can edit the title, content, and thumbnail image of the post.
   - #### index.html
      - A page that displays all notes created by a user. Authentication required.
   - #### layout.html
      - A template html file in which is defined a top and left navigation bars. This template is extended to almost all html files except Custom Error files. It contains links to include  bootstrap and font awesome in it, as well as javascript and css files from  `static` folder. Depending on whether the user is logged in or not, and depending on which file the template is distributed in, the template loads different elements.
   - #### login.html
      - A page for logging into a user account. The page contains inputs for a username and password.
   - #### new_post.html
      - A page for creating a new post. Authentication required.
   - #### post.html
      - A page that displays the entire existing post, belonging to a logged-in user. Page contains "Edit" and "Delete" buttons, with which user can edit or delete post respectively. It also contains a toggle button that allows the user to change the privacy of the post from "public" to "private" and vice versa.
   - #### profile.html
      - A page for user profile settings. Here user can upload user's avatar, or change name and password.
   - #### public_index.html
      - A page that displays all posts that have been published, created by any user. User Authentication is not required.
   - #### public_post.html
      - A page that displays the entire post that does not belong to a logged in user, or the user is not logged in at all.
   - #### register.html
      - New user registration page. It contains fields for username, password, and password confirmation.
   - #### search.html
      - A page displays posts returned by the search() function.
   - #### welcome.html
      - Welcome page for logged users, which tells user how to get started. contains links to create new post, explore published topics, set up profile and contacts.
      - A welcome page for logged-in users that tells the user how to get started. Contains links to create a new post, explore published topics, set up a profile and go to contact page.
### **static/**
   - - Contains static assets like CSS, JavaScript, and images.
   - #### uploads
      - folder, in which posts's thumbnail images or user profile avatars are uploaded.
   - #### blog.js
      - Javascript file linked in layout.html. It also applies to other html files where layout.html file is extended.
   - #### styles.css
      - Css style folder linked in layout.html. It also applies to other html files where layout.html file is extended.

## Author
Created by Mikheil Akobidze as the final project of CS50x.

