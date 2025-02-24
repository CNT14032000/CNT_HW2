![image](https://github.com/user-attachments/assets/ea4904b3-3aff-4e88-9bcb-e0b9a0a4c16b)# CNT_HW2
I did my homework 2 by writing a web application with features like authentication that allows users to log in and redirects to a profile page for each user, allowing users to create accounts and the profile will be displayed with data related to each account. Implemented password hashing using Bcrypt and allowed logout to change password, also the site allows users to update their profile information and avatar. All data is stored in Mongodb.
## Basic part:
Implement authentication feature   
### 1.1 Listen on localhost:5000 
The Flask application listens on port 5000, serving as the entry point for users.
### 1.2 Render authentication form at http://localhost:5000/  
At http://localhost:5000/ the website will send a login form asking the user to authenticate his account.</br>
![login page image](static/images/login.PNG) </br>
### 1.3 Redirect user to profile page if successfully authenticated 
Upon successful authentication, users are redirected to their profile page
### 1.4 Show profile page for authenticated user only at http://localhost:5000/profile   
If the user authenticates successfully, the site will be redirected to the profile page at http://localhost:5000/profile. </br>
![profile page image](static/images/profile.PNG) </br>
### 1.5 User name and password are stored in Mongodb or Redis
User data is stored using mongodb.</br>
![data base image](static/images/db.PNG) </br>
## Advanced part (optional):   
### 2.1 Implement feature that allows users to create new account, profile will be shown with data respected to each account.  
On the login page, if the user does not have an account, they can click Sign Up to create a new account, the website will redirect to the sign up page. After completing the account registration, the user needs to log in to the newly created account. If successful, they will be redirected to the profile page of that account.</br>
![sign up image](static/images/SignUp.PNG) </br>
### 2.2 Implement password hashing, logout and password change features 
* Password hashing is done using bcrypt.</br>
hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
* User logout feature can click this button on the profile page.</br>
![logout image](static/images/logout.PNG) </br>
* User change password feature click this button on the profile page, then the website is redirected to the password change page where the user can change the password and update his password. After successful the user needs to log in again to enter the profile page.</br>
![data base image](static/images/change_password.PNG) </br>
### 2.3 Allow users to update profile picture (new user will have a default profile picture) 

