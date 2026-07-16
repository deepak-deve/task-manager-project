from flask import Blueprint, render_template, request, redirect, session, flash
from database.db import get_connection
import bcrypt

auth = Blueprint("auth", __name__)


# =========================
# REGISTER
# =========================
@auth.route("/")
def register_page():
    return render_template("register.html")


@auth.route("/register", methods=["POST"])
def register():

    name = request.form["name"].strip()
    email = request.form["email"].strip().lower()
    password = request.form["password"]

    # Basic Validation
    if name == "" or email == "" or password == "":
        flash("All fields are required.")
        return redirect("/")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Check duplicate email
    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    if user:
        flash("Email already exists.")
        cursor.close()
        connection.close()
        return redirect("/")

    # Hash Password
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    cursor.execute(
        """
        INSERT INTO users(name,email,password)
        VALUES(%s,%s,%s)
        """,
        (
            name,
            email,
            hashed_password.decode("utf-8")
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    flash("Registration Successful. Please Login.")

    return redirect("/login")


# =========================
# LOGIN PAGE
# =========================
@auth.route("/login")
def login():

    return render_template("login.html")


# =========================
# LOGIN
# =========================
@auth.route("/login", methods=["POST"])
def login_post():

    email = request.form["email"].strip().lower()
    password = request.form["password"]

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if not user:

        flash("Invalid Email")

        return redirect("/login")

    if not bcrypt.checkpw(

        password.encode("utf-8"),

        user["password"].encode("utf-8")

    ):

        flash("Invalid Password")

        return redirect("/login")

    # Login Success
    session["user_id"] = user["id"]
    session["user_name"] = user["name"]

    return redirect("/dashboard")


# =========================
# DASHBOARD
# =========================
@auth.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Total Tasks
    cursor.execute(
        "SELECT COUNT(*) AS total FROM tasks WHERE user_id=%s",
        (session["user_id"],)
    )
    total = cursor.fetchone()["total"]

    # Pending Tasks
    cursor.execute(
        """
        SELECT COUNT(*) AS pending
        FROM tasks
        WHERE user_id=%s
        AND status='Pending'
        """,
        (session["user_id"],)
    )
    pending = cursor.fetchone()["pending"]

    # Completed Tasks
    cursor.execute(
        """
        SELECT COUNT(*) AS completed
        FROM tasks
        WHERE user_id=%s
        AND status='Completed'
        """,
        (session["user_id"],)
    )
    completed = cursor.fetchone()["completed"]

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        name=session["user_name"],
        total=total,
        pending=pending,
        completed=completed
    )


# =========================
# LOGOUT
# =========================
@auth.route("/logout")
def logout():

    session.clear()

    return redirect("/login")