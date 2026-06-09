from flask import Blueprint, render_template, request, redirect, url_for
from database.db import get_connection

people_bp = Blueprint("people", __name__)


@people_bp.route("/people")
def index():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name
        FROM people
        ORDER BY id
    """)

    people = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "people/index.html",
        people=people
    )


@people_bp.route("/people/create")
def create():

    return render_template(
        "people/create.html"
    )


@people_bp.route("/people/store", methods=["POST"])
def store():

    name = request.form["name"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO people(name)
        VALUES(%s)
    """, (name,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(
        url_for("people.index")
    )

@people_bp.route("/people/edit/<int:id>")
def edit(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name
        FROM people
        WHERE id = %s
    """, (id,))

    person = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "people/edit.html",
        person=person
    )

@people_bp.route("/people/update/<int:id>", methods=["POST"])
def update(id):

    name = request.form["name"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE people
        SET name = %s
        WHERE id = %s
    """, (name, id))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(
        url_for("people.index")
    )

@people_bp.route("/people/delete/<int:id>")
def delete(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM people
        WHERE id = %s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(
        url_for("people.index")
    )