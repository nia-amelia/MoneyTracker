from flask import Blueprint, render_template, request, redirect, url_for
from database.db import get_connection
from flask import send_file
from openpyxl import Workbook
from io import BytesIO

transactions_bp = Blueprint(
    "transactions",
    __name__
)

@transactions_bp.route("/transactions")
def index():

    person_id = request.args.get("person_id")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            t.id,
            p.name,
            t.transaction_date,
            t.type,
            t.category,
            t.amount,
            t.description

        FROM transactions t

        JOIN people p
        ON p.id = t.person_id
    """

    params = []

    if person_id:

        query += """
            WHERE t.person_id = %s
        """

        params.append(person_id)

    query += """
        ORDER BY t.id DESC
    """

    cursor.execute(
        query,
        params
    )

    transactions = cursor.fetchall()

    cursor.execute("""
        SELECT
            id,
            name
        FROM people
        ORDER BY name
    """)

    people = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "transactions/index.html",
        transactions=transactions,
        people=people,
        selected_person=person_id
    )

@transactions_bp.route("/transactions/create")
def create():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,name
        FROM people
        ORDER BY name
    """)

    people = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "transactions/create.html",
        people=people
    )

@transactions_bp.route(
    "/transactions/store",
    methods=["POST"]
)
def store():

    person_id = request.form["person_id"]

    transaction_date = request.form["transaction_date"]

    type = request.form["type"]

    category = request.form["category"]

    amount = request.form["amount"]

    description = request.form["description"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (
            person_id,
            transaction_date,
            type,
            category,
            amount,
            description
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
    """,
    (
        person_id,
        transaction_date,
        type,
        category,
        amount,
        description
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(
        url_for(
            "transactions.index"
        )
    )

@transactions_bp.route("/transactions/edit/<int:id>")
def edit(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            person_id,
            transaction_date,
            type,
            category,
            amount,
            description
        FROM transactions
        WHERE id = %s
    """, (id,))

    transaction = cursor.fetchone()

    cursor.execute("""
        SELECT id, name
        FROM people
        ORDER BY name
    """)

    people = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "transactions/edit.html",
        transaction=transaction,
        people=people
    )

@transactions_bp.route(
    "/transactions/update/<int:id>",
    methods=["POST"]
)
def update(id):

    person_id = request.form["person_id"]
    transaction_date = request.form["transaction_date"]
    type = request.form["type"]
    category = request.form["category"]
    amount = request.form["amount"]
    description = request.form["description"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET
            person_id = %s,
            transaction_date = %s,
            type = %s,
            category = %s,
            amount = %s,
            description = %s
        WHERE id = %s
    """,
    (
        person_id,
        transaction_date,
        type,
        category,
        amount,
        description,
        id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(
        url_for("transactions.index")
    )

@transactions_bp.route("/transactions/delete/<int:id>")
def delete(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM transactions
        WHERE id = %s
    """, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(
        url_for("transactions.index")
    )

@transactions_bp.route("/transactions/export")
def export_excel():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.name,
            t.transaction_date,
            t.type,
            t.category,
            t.amount,
            t.description

        FROM transactions t

        JOIN people p
        ON p.id = t.person_id

        ORDER BY t.transaction_date DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    wb = Workbook()

    ws = wb.active

    ws.title = "Transaksi"

    ws.append([
        "Nama",
        "Tanggal",
        "Jenis",
        "Kategori",
        "Nominal",
        "Keterangan"
    ])

    for row in data:

        ws.append(row)

    excel_file = BytesIO()

    wb.save(excel_file)

    excel_file.seek(0)

    return send_file(
        excel_file,
        as_attachment=True,
        download_name="laporan_transaksi.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )