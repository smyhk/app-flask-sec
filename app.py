from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# docker run -p 5432:5432 --name flask-postgres -e POSTGRES_PASSWORD=secretpassword -d postgres
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:secretpassword@localhost:5432/appflasksec'
db = SQLAlchemy(app)


@app.route("/")
def index():
    return "<h1>Hello Flask!</h>"


if __name__ == "__main__":
    app.run(debug=True)
