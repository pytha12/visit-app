"""
Main module of the server file
"""

# 3rd party moudles
from flask import render_template

# Local modules
import config


# Get the application instance
connex_app = config.connex_app

# Read the swagger.yml file to configure the endpoints
connex_app.add_api("swagger.yml")


# Create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/

    :return:        the rendered template "home.html"
    """
    return render_template("home.html")


# Create a URL route in our application for "/user"
@connex_app.route("/users")
@connex_app.route("/users/<int:user_id>")
def users(user_id=""):
    """
    This function just responds to the browser URL
    localhost:5000/user

    :return:        the rendered template "people.html"
    """
    return render_template("user.html", user_id=user_id)



# Create a URL route to the notes page
@connex_app.route("/users/<int:user_id>")
@connex_app.route("/users/<int:user_id>/visit")
@connex_app.route("/users/<int:user_id>/visit/<int:visit_id>")
def visits(user_id, visit_id=""):
    """
    This function responds to the browser URL
    localhost:5000/notes/<person_id>

    :param user_id:   Id of the user to show visit for
    :return:            the rendered template "notes.html"
    """
    return render_template("notes.html", user_id=user_id, visit_id=visit_id)


if __name__ == "__main__":
    connex_app.run(debug=True)
