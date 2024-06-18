
**LeoWatch Video Platform**
A video platfrom project developed as part of AmaliTech’s NSS recruitment Process
=====================================================================
** Overview**
LeoWatch is a custom video hosting platform developed using Django for Paul Leonard, a video creator who requires a personalized video platform to showcase his work. The platform allows seamless video uploads, management, and viewing, all while maintaining a strong brand presence.
***TABLE OF CONTENTS***
=====================
*Features*
  •	User Features
  •	Admin Features
  •	Video Page Features
*Installation*
  •	Prerequisites
  •	Clone Repository
  •	Setup Environment
  •	Run the Application
*Usage*
  •	Signup & Login
  •	Navigating Videos
  •	Sharing Videos
*Development*
  •	Folder Structure
  •	Contribution Guidelines
*License*
*Contact*


***MAIN CONTENTS***
========================================================================
**Features**
    **User Features**
    *Signup & Login*
•	Users can create an account using an email and password.
•	Account verification via email.
•	Password recovery through email.
   *Video Navigation*
•	Users can navigate through video pages easily.
    *Video Sharing*
•	Users can share links via email to videos on different pages.

    **Controller Features**
    *Video Upload*
•	Admins can upload videos with a title and description.
•	Admins can edit the title and description of an uploaded video
•	Admins can delete videos and this will delete the file on disk, not only in the database.

   **Video Page Features**
    *Single Video Display*
•	Each video page presents one video.
•	Previous and next buttons to navigate through videos.
•	Buttons are hidden if no further videos are available in that direction.
    *Video Controls*
•	There is a video title and description under the video
•	Basic video controls such as play, pause, volume, etc.

    **Branding**
•	Business logo prominently displayed at the top-left of all pages.
•	I just made up the logo so it is not an actual representation of a reality.

    **Sharing**
•	Share button to share the link to the video page.
•	You don't have to explicitly type the URL. 
•	Add the recipient email, and optional message and we handle the rest.

    **Installation**
    *Prerequisites*
•	Python (v3.8 or later)
•	Django (v3.2 or later)

    *Clone Git Repository8
•	git clone https://github.com/owusu-king/videoPlatform.git
•	cd videoPlatform

    *Setup your Environment*
•	python -m venv venv
•	source venv/bin/activate # On Windows use `venv\Scripts\activate`
•	pip install -r requirements.txt
            
    *Running the Application*
•	In the main project folder, run 'python manage.py makemigrations'
•	Run 'python manage.py migrate' to create your database schema
•	Optionally Run 'python manage.py createsuperuser' to create an admin user
•	Alternatively use the signup page to create a new account.
•	Go to the groups model and create a new group with the name 'Controller'
•	Assign the superuser to the 'Controller' group to grant them access to admin page.

    **Database Options**    
•	Comment out the MySQL db backend if SQLite is being used
•	MySQL for Production. Comment out the SQLite database if MySQL is being used



    **Folder Structure**

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
    	

**License**
•	This project is licensed under the FSD License. See the LICENSE file for more details.

**Contact**
•	For any questions or inquiries, please contact King Owusu at owusuking401@gmail.com. 
•	I am also available on WhatsApp with +233 247 02 2382 
