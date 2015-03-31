# Main file to AJAX/Flask messaging application

# Import statements

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    g,
    flash,
    request,
)

from flask.ext.bcrypt import (
    check_password_hash,
)

from flask.ext.login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

import forms
import models
import json
import re

# Set up application - need a secret key for secure sessions
app = Flask(__name__)
app.secret_key = "stuff"

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Non route functions


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


# Login Manager Functions


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

# Before and After request functions


@app.before_request
def before_request():
    """Connect to database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each response"""
    g.db.close()
    return response

# Routes


@app.route("/register", methods=("POST", "GET"))
def register():
    # Get register form
    form = forms.RegisterForm()

    # Check if valid form has been submitted
    if form.validate_on_submit():
        # Create new user
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        # Flash message
        flash("Yay you registered")

        # Redirect to index page
        return redirect(url_for("index"))

    # If not render register.html and pass it the register form
    return render_template("register.html", form=form)


@app.route("/login", methods=("GET", "POST"))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password does not exist.", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in.", "success")
                return redirect(url_for("index"))
            else:
                flash("Your email or password does not exist.", "error")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out. Come back soon.")
    return redirect(url_for("index"))


@app.route("/")
def index():
    if current_user.is_authenticated():
        return redirect(url_for("message"))
    return render_template("index.html")


@app.route("/message", methods=("POST", "GET"))
@login_required
def message():
    users = models.User.get_usernames()
    user = models.User.get(models.User.id == current_user.get_id())
    username = user.username
    return render_template("message.html", users=users, username=username)


@app.route("/new_message", methods=("POST", "GET"))
@login_required
def new_message():
    result = {"result": None}
    try:
        my_content = clean_html(request.form["content"])
        models.Message.create(
            from_user=g.user._get_current_object(),
            to_user=models.User.get_user(request.form["to_user"]),
            content=my_content
        )
        result["result"] = True
    except:
        result["result"] = False
    return json.dumps(result)


@app.route("/get_messages")
@login_required
def get_messages():
    messages = models.Message.get_messages(current_user.get_id())
    return json.dumps(messages)


@app.route("/get_messages_from", methods=("POST", "GET"))
@login_required
def get_messages_from():
    messages = models.Message.get_messages_from(
        current_user.get_id(),
        models.User.get(models.User.username == request.form["from_user"]).id
    )
    print(json.dumps(messages))
    return json.dumps(messages)


if __name__ == "__main__":
    models.initialize()
    app.run(debug=True)
