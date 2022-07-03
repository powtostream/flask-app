from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request
from datetime import datetime
from flask_login import UserMixin
from flask_wtf import wtforms
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "67d306982a966e1ffd01b878f26ad99cb87e282f"


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    pr = db.relationship("Profiles", backref='users', uselist=False)

    def __repr__(self):
        return f"<users {self.id}>"


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"


class RegistrationForm(Flask)

@app.route("/")
def index():
    menu = []
    try:
        menu = Users.query.all()
    except:
        print("error reading db")
    return render_template('index2.html', title='Main', menu=menu)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        try:
            psw_hash = generate_password_hash(request.form['psw'])
            u = Users(email=request.form['username'], psw=psw_hash)
            db.session.add(u)
            db.session.flush()

            p = Profiles(name=request.form['email'],
                         city=request.form['city'], user_id=u.id)
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("error adding to db")

    return render_template("register.html", title='Registration')


@app.route("/login", methods=['POST', 'GET'])
def login():
    return render_template('login2.html', title='Login')

if __name__ == "__main__":
    app.run(debug=True)
