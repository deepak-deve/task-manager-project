from flask import Blueprint, render_template, request, redirect, session
from database.db import get_connection

task = Blueprint("task", __name__)


# =========================
# TASK LIST
# =========================
@task.route("/tasks")
def tasks():

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE user_id=%s
        ORDER BY id DESC
        """,
        (session["user_id"],)
    )

    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "tasks.html",
        tasks=tasks
    )


# =========================
# ADD TASK PAGE
# =========================
@task.route("/add-task")
def add_task():

    if "user_id" not in session:
        return redirect("/login")

    return render_template("add_task.html")


# =========================
# SAVE TASK
# =========================
@task.route("/add-task", methods=["POST"])
def save_task():

    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    status = request.form["status"]
    due_date = request.form["due_date"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tasks
        (user_id,title,description,priority,status,due_date)
        VALUES(%s,%s,%s,%s,%s,%s)
        """,
        (
            session["user_id"],
            title,
            description,
            priority,
            status,
            due_date
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/tasks")

    # =========================
# DELETE TASK
# =========================
@task.route("/delete-task/<int:id>")
def delete_task(id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(

        """
        DELETE FROM tasks
        WHERE id=%s
        AND user_id=%s
        """,

        (
            id,
            session["user_id"]
        )

    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/tasks")

    # =========================
# EDIT TASK PAGE
# =========================
@task.route("/edit-task/<int:id>")
def edit_task(id):

    if "user_id" not in session:
        return redirect("/login")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE id=%s
        AND user_id=%s
        """,
        (
            id,
            session["user_id"]
        )
    )

    task_data = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template(
        "edit_task.html",
        task=task_data
    )


# =========================
# UPDATE TASK
# =========================
@task.route("/update-task/<int:id>", methods=["POST"])
def update_task(id):

    if "user_id" not in session:
        return redirect("/login")

    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    status = request.form["status"]
    due_date = request.form["due_date"]

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET
            title=%s,
            description=%s,
            priority=%s,
            status=%s,
            due_date=%s
        WHERE
            id=%s
            AND user_id=%s
        """,
        (
            title,
            description,
            priority,
            status,
            due_date,
            id,
            session["user_id"]
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/tasks")