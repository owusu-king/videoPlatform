# videoPlatform
A video platfrom project developed as part of AmaliTech NSS recruitment Process

LeoWatch Video Platform
=======================
# Link to the video page
http://kingowusu.pythonanywhere.com/

Project Overview
LeoWatch is a custom video hosting platform developed using Django for Paul Leonard, a video creator who requires a personalized video platform to showcase his work. The platform allows seamless video uploads, management, and viewing, all while maintaining a strong brand presence.

TABLE OF CONTENTS
=================
Features
    User Features
    Admin Features
    Video Page Features
Installation
    Prerequisites
    Clone Repository
    Setup Environment
    Run the Application
Usage
    Signup & Login
    Navigating Videos
    Sharing Videos
Development
    Folder Structure
    Contribution Guidelines
License
Contact


MAIN CONTENTS
================================================
Features
    User Features
        Signup & Login
            Users can create an account using an email and password.
            Account verification via email.
            Password recovery through email.
    Video Navigation
        Users can navigate through video pages easily.
    Video Sharing
        Users can share links via email to videos on different pages.

    Controller Features
        Video Upload
            Admins can upload videos with a title and description.
            Admins can edit the title and description of an uploaded video
            Admins can delete videos and this will delete the file on disk, not only in the database.
    Video Page Features
        Single Video Display
            Each video page presents one video.
            Previous and next buttons to navigate through videos.
            Buttons are hidden if no further videos are available in that direction.
        Video Controls
            There is a video title and description under the video
            Basic video controls such as play, pause, volume, etc.


Branding
    Business logo prominently displayed at the top-left of all pages.
    I just made up the logo so it is not an actual representation of a reality.

Sharing
    Share button to share the link to the video page.
    You don't have to explicitly type the url. just add the reciepient email, and optional message and we handle the rest.

Installation
    Prerequisites
        Python (v3.8 or later)
        Django (v3.2 or later)

Clone Git Repository
    git clone https://github.com/owusu-king/videoPlatform.git
    cd videoPlatform

Setup your Environment 
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    Optionally Create a .env file in the root directory and add the necessary environment variables:
            
Running the Application
    In the main project folder, run 'python manage.py makemigrations'
    Then run 'python manage.py migrate' to create your database schema
    Optionally Run 'python manage.py createsuperuser' to create an admin user
    Or use the signup page to create a new account after running "python manage.py runserver"
    After creating superuser account, copy your local url, typically 127.0.0.1 and a default port 8000
    Access the Admin page. using the example above, http://127.0.0.1:8000/admin
    Go to the groups model and create a new group with the name 'Controller'
    Assign the superuser to the 'Controller' group to give them access to upload and manage videos.

Database Options    
    SQLite for Development. You have to uncomment in the project settings and set debug true
    MySQL for Production. Comment out the SQLite database in project settings and uncomment the MySQL backend
    If you have MySQL installed, you can also use that in development as you wish.

Signup and Login
    Signup
        Click on the Signup link on the homepage.
        Fill in your email, firstname, lastname and password. Don't forget to check the T&C checkbox
        Verify your email through the link sent to your email address.
        The link will expire in 10 minutes so you have to click on it before it expires.

    Login
        Click on the Login link on the homepage.
        Enter your email and password to log in. 
    
    Password Recovery
        Click on Forgot Password on the login page.
        Enter your email to receive a password reset link.
        Click on the reset link and set a new password.
        Login with your new password

Navigating Videos
    Video page
        Each video page displays a single video.
        Use the Next and Previous buttons to navigate through videos.

    Sharing Videos
        Click on the Share button on the video page.
        Add the recipient email and an optional message to the pop up form.
        Click on Share now and wait for an alert of "Link successfully shared"

Folder Structure

├── videoPlatform/               # Main Django project directory
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Project URL configurations
│   ├── db.sqlite3               # SQLite database file (can be replaced by another database)
│   ├── manage.py                # Django's management script
    ├── videoPlatform/                    # Main Django project directory
    │   ├── __init__.py
    │   ├── settings.py              # Django settings
    │   ├── urls.py                  # Project URL configurations
    │   ├── wsgi.py                  # WSGI entry point for deployment
    │   ├── asgi.py                  # ASGI entry point for asynchronous handling
    │
    ├── video/                       # Django app named 'video'
    │   ├── __init__.py
    │   ├── admin.py                 # Admin configurations
    │   ├── apps.py                  # App configurations
    │   ├── forms.py                 # Forms
    │   ├── models.py                # Database models
    │   ├── tests.py                 # Test cases
    │   ├── views.py                 # View logic
    │   ├── urls.py                  # URL configurations for the app
    │   ├── templates/               # Templates directory specific to the 'video' app
    │   │   ├── video/               # Templates for the 'video' app
    │   │   │   ├── dashboard.html  
    │   │   │   ├── edit.html 
    │   │   │   ├── index.html
    │   │   │   ├── layout.html 
    │   │   │   ├── login.html
    │   │   │   ├── no-video.html   
    │   │   │   ├── share_email.html
    │   │   │   ├── signup.html
    │   │   ├── 404.html                               # Custom 404 page                 
    │   │   │   ├── verification/                      # Templates for email verification
    │   │   │   │   └── activate_email_info.html
    │   │   │   │   └── activation_complete.html
    │   │   │   │   └── activation_invalid.html
    │   │   │   │   └── already_verified.html
    │   │   │   │   └── verification_confirm.html
    │   │   │   ├── reset_password/                    # Templates for password reset
    │   │   │   │   └── password_reset_complete.html
    │   │   │   │   └── password_reset_confirm.html
    │   │   │   │   └── password_reset_done.html
    │   │   │   │   └── password_reset_email.html
    │   │   │   │   └── password_reset_form.html
    │   │   │   │   └── reset_form.html
    │   ├── static/                  # Static files directory specific to the 'video' app
    │   │   ├── video/               # Static files for the 'video' app
    │   │   │   ├── styles/          # CSS files
    │   │   │   │   └── style.css    # Main CSs
    │   │   │   │   └── small.css    # Small screens
    │   │   │   ├── js/              # JavaScript files
    │   │   │   │   └── script.js
    │   │   │   ├── images/          # Image files
    │   │   │   │   └── logo.png
    │   │   │   │   └── error.png
    │   │   │   │   └── icon.png
    │   │   │   │   └── success.png
    │   ├── management/              # Management commands directory
    │   │   ├── __init__.py
    │   │   ├── commands/            # Custom Django management commands
    │   │   │   ├── __init__.py
    │   │   │   └── clean_db.py      # Used to reset the database schema
    │   ├── migrations/              # Database migrations
    │   │   ├── __init__.py
    │
    ├── static/                      # Collected static files (generated)
    ├── media/                  # Uploaded media files (generated)
    ├── .env                         # Environment variables file
    ├── requirements.txt             # Python dependencies
    └── README.md                    # Project documentation

License
    This project is licensed under the FSD License. See the LICENSE file for more details.

Contact
    For any questions or inquiries, please contact King Owusu at owusuking401@gmail.com. 
    I am also available on WhatsApp with +233 247 02 2382  
