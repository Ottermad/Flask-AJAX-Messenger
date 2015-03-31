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
    * JavaScript
* Python Packages and Modules
    * Flask - a micro-framework for Python that powers the backend of my application.
    * Jinja2 - the default templating engine from Flask, I used to not only create dynamic templates but keep inline JavaScript in a seperate file.
    * WTForms
    * Flask-WTForms
    * json
    * re
    * Peewee
    * PyMySql
* 