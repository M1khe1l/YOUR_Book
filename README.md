# YOUR BOOK
#### Video Demo:  [[ youtube_link](https://www.youtube.com/watch?v=WqpdWcGZsN8)]
#### Description:
 - This project is a web-based application using JavaScript, Python, and SQLite. It is a blogging platform where users can explore and share ideas through published notes.The website provides a place to read posts shared by others, create personalized notes, and publish content for public viewing.

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

## How to Use:
   - From project directory, in terminal window run `flask run` and open provided link in browser.

## File Overview:
### **app.py**
   - The main Flask application file.
   - Contains routes for user registration, authentication, post management, and more.
### **blog.db**
   - Sqlite database which contains differens tables:
      - users - contains unique id, username, hash and profile_image columns.
      - posts - contains posts informations like id, author, title, content, image_url etc.
      - saved - contains id of the saved post and id of user who saved that post.
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
