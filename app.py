from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

app = Flask(__name__)

# docker run -p 5432:5432 --name flask-postgres -e POSTGRES_PASSWORD=secretpassword -d postgres
# this will be loaded from a config file or env for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:secretpassword@localhost:5432/appflasksec'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # supress deprecation warning
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = '$2a$16$PnnIgfMwkOjGX4SkHqSOPO'

db = SQLAlchemy(app)


# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/profile/<email>")
@login_required
def profile(email):
    user = User.query.filter_by(email=email).one()
    return render_template('profile.html', user=user)


if __name__ == "__main__":
    app.run(debug=True)
