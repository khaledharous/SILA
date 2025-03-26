#_Student_Registration_System

This project is a "Flask-based web application" for student registration, login, and profile management. It includes features like user authentication, password reset (not available now), and profile display.

---

## Features
- **User Registration**: Allows users to register with their details.
- **Login System**: Users can log in with their credentials.
- **Profile Management**: Displays user information on the profile page.
- **Password Reset**: Users can reset their password via email.->('Not available')
- **Logout**: Users can securely log out of the system.

---

## Prerequisites
Before running the application, ensure you have the following installed:
1. **Python 3.7.x 'or newer'**
2. **flask**
3. **SQLite** (Database used for storing user data)

---
                       "Steps to Run the Application"
1.Download the Project:

 If the project is in a ZIP file, extract it to a folder on your 'Desktop'.->(Necessary extract it in desktop)

---
2.Open a terminal or command prompt in the project directory and run:
   >>> cd Desktop\SILA-Data-Base-V2.0

3.then check if Python is installed:
 in cmd  type the following command and press Enter:
   >>> python  --version

  (if python installed ,it will display the version "e.g: Python 3.x.x")
    .if not , download it from: <https://www.python.org>

 during installation ,make sure to check "ADD Python To Path"
 ...Verify Pip installation :
 pip (Python's package manager) is required to install dependencies
  in cmd type: 
   >>> pip --version
    .if pip installed ,you'll see somethings like "pip 23.x.x", 'or newer'

    .if not, install it, using:
   >>> python -m ensurepip --default-pip 

4.install Flask and Verify installation:
    >>> pip install flask 

 .Verify flask installation by running:
    >>> python -m flask --version
  .if flask is installed, it will show its version.

5.install SQLite and Verify installation:
  in cmd, type:
    >>> SQLite3 --version 
    if he didn't display the version download it from <https://www.sqlite.org>:
       select this : Precompiled Binaries for Windows -> "sqlite-tools-win-x64-3490100.zip" 
  then, install SQLite Viewer for VS Code:
   _Open VS Code.
   _Go to the Extensions tab (Ctrl + Shift + X).
   _Search for "SQLite Viewer" or "SQLite Explorer" and install it.
_Now You can now run the project from VS Code and to make sure your information has reached the "Data-Base":
   _Open VS Code and load your project.
   _Locate users.db in the project folder.
    ->Right-click the file → "Open With -> "SQLite Viewer".
     -Go to > "users" table to see stored information .

                                                             Important:
!!! if you plan to upload the project to "Github" make sure to delete 'users.db' before uploading to protect your information !!!


  