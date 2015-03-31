# Flask AJAX Messenger

This a simple application which allows users to send text based messenges to each other. The messenges can be formatted with markdown. Orginally, this was a simple project to allow me to learn AJAX and JSON parsing, but it may evolve in the future.

## Technical Details

### Summary
The application works by having a series of routes in Flask. Some of these routes return templates (e.g. those for logging in and signing up, the page for viewing messages etc.) and others which query a database and return JSON (those which fetch or send messages). Then once the template for viewing and sending messages have been loaded, AJAX is then used to make requests to other routes to send and recieve messages which are then displayed.

### Technologies Used

* Languages
    * Python - the main language used to implement the backend of my application.
    * HTML
    * CSS
    * JavaScript - mostly used to make requests using AJAX, parse the returned JSON and update appropiate elements/
* Python Packages and Modules
    * Flask - a micro-framework for Python that powers the backend of my application.
    * Jinja2 - the default templating engine from Flask, I used it to not only create dynamic templates but keep inline JavaScript in a seperate file.
    * Flask-Login - used to provide login functionality to the application.
    * Flask-Bcrypt - used to hash the passwords
    * WTForms - used to help build dynamic login and registration forms
    * Flask-WTForms - used to help build dynamic login and registration forms
    * json - used to convert python objects to JSON for the requests sent via AJAX
    * re - used to allow the use of regular expressions on strings
    * Peewee - an lightweight ORM used to store my data
    * Markdown - used to convert markdown to HTML so messages can make use of markdown
* Front-end libraries
    * jQuery
    * Twitter Bootstrap - improve the deisgn of the application
    * Flat-UI - [http://designmodo.com/flat-free/](http://designmodo.com/flat-free/) - a Bootstrap theme used to create a more unique design
* Other Technologies
    * JSON - the format of data returned to the AJAX scripts
    * SQLite3 - although the Peewee ORM is used to interact with the database, a SQLite db is used
    * Regular Expressions - used to perform string operations
