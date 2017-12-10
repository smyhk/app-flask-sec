from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# docker run -p 5432:5432 --name flask-postgres -e POSTGRES_PASSWORD=secretpassword -d postgres
# this will be loaded from a config file or env for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:secretpassword@localhost:5432/appflasksec'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # surpress deprecation warning
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


@app.route("/")
def index():
    myUsers = User.query.all()
    oneItem = User.query.filter_by(username="smyhk").one()
    return render_template('add_user.html', myUsers=myUsers, oneItem=oneItem)


@app.route("/profile/<username>")
def profile(username):
    user = User.query.filter_by(username=username).one()
    return render_template('profile.html', user=user)


@app.route("/post_user", methods=['POST'])
def post_user():
    user = User(request.form['username'], request.form['email'])
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
