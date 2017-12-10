from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# docker run -p 5432:5432 --name flask-postgres -e POSTGRES_PASSWORD=secretpassword -d postgres
# this will be loaded from a config file or env for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:secretpassword@localhost:5432/appflasksec'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r' % self.username


@app.route("/")
def index():
    return "<h1>Hello Flask!</h>"


if __name__ == "__main__":
    app.run(debug=True)
