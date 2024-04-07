import sqlite3
import logging
import os
from flask import Flask, session, redirect, url_for, request, render_template, abort


app = Flask(__name__)

# Don't store the secret key in app code, but inject as env variable at runtime
app.secret_key = os.getenv("APP_SECRET_KEY", default="INVALID_KEY_GIVEN")
app.logger.setLevel(logging.INFO)


# TODO: Check existence of filename
def get_read_only_db_connection():
    # Changed to a readonly connection, since we're only using SELECT queries
    connection = sqlite3.connect("file:database.db?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def is_authenticated():
    if "username" in session:
        return True
    return False


def authenticate(username, password):
    connection = get_read_only_db_connection()

    # Use a single query to see if the username & password combination exists
    # instead of retrieving all users/passwords and looping over it.
    # Use Parameter Binding to prevent SQL injection
    is_valid_credentials = connection.execute(
        """
            SELECT 
                id
            FROM 
                users 
            WHERE
                username = :username
            AND 
                password = :password
        """,
        {"username": username, "password": password},
    ).fetchone()
    connection.close()

    # Fail early
    if not is_valid_credentials:
        app.logger.warning(f"User '{username}' has failed to login.")
        abort(401)

    app.logger.info(f"User '{username}' has succesfully logged in.")
    session["username"] = username
    return True


@app.route("/")
def index():
    return render_template("index.html", is_authenticated=is_authenticated())


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if authenticate(username, password):
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


# TODO: Bind on a different host
# TODO: Define readyz, healthz and livez endpoints
# Readyz should check database connection
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
