from flask import Blueprint, render_template

from database.db import get_connection

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

@dashboard_bp.route("/")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            p.id,
            p.name,

            COALESCE(
                SUM(
                    CASE
                        WHEN t.type='masuk'
                        THEN t.amount
                        ELSE 0
                    END
                ),
                0
            ) AS total_masuk,

            COALESCE(
                SUM(
                    CASE
                        WHEN t.type='keluar'
                        THEN t.amount
                        ELSE 0
                    END
                ),
                0
            ) AS total_keluar,

            COALESCE(
                SUM(
                    CASE
                        WHEN t.type='masuk'
                        THEN t.amount
                        ELSE -t.amount
                    END
                ),
                0
            ) AS saldo

        FROM people p

        LEFT JOIN transactions t
        ON p.id = t.person_id

        GROUP BY
            p.id,
            p.name

        ORDER BY p.name

    """)

    summary = cursor.fetchall()

    total_dana = 0

    for row in summary:
        total_dana += float(row[4])

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(amount),
                0
            )
        FROM transactions
        WHERE type = 'masuk'
    """)

    total_masuk = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(amount),
                0
            )
        FROM transactions
        WHERE type = 'keluar'
    """)

    total_keluar = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            COUNT(*)
        FROM transactions
    """)

    jumlah_transaksi = cursor.fetchone()[0]

    chart_data = [
        {
            "kategori": "Masuk",
            "nominal": float(total_masuk)
        },
        {
            "kategori": "Keluar",
            "nominal": float(total_keluar)
        }
]

    cursor.close()
    conn.close()

    return render_template(
        "dashboard/index.html",
        summary=summary,
        total_dana=total_dana,
        total_masuk=total_masuk,
        total_keluar=total_keluar,
        jumlah_transaksi=jumlah_transaksi,
        chart_data=chart_data
    )

