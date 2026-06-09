from flask import Flask

from routes.people import people_bp

from routes.transactions import transactions_bp

from routes.dashboard import dashboard_bp

from helpers.formatter import rupiah

app = Flask(__name__)
app.jinja_env.filters['rupiah'] = rupiah

app.register_blueprint(people_bp)
app.register_blueprint(transactions_bp)
app.register_blueprint(dashboard_bp)

if __name__ == "__main__":
    app.run(debug=True)