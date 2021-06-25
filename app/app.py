from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from flask_bcrypt import Bcrypt
import json

from voice_recognition import voice_recognition
import pyrebase

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'vandyprerudidit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)

db = SQLAlchemy(app)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(50), nullable=False)

with open('credentials.json') as creds:
    configuration = json.load(creds)
firebase = pyrebase.initialize_app(configuration)
fb_db = firebase.database()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")

@app.route('/', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            flash("Incorrect Password!", 'warning')
        if user is None:
            flash("You are not authorized!", 'warning')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template("login.html", form=form)

@app.route('/speech-recognition', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        voice_sample = voice_recognition()
        if voice_sample == "forward":
            data = {
                    'command' : 0
            }
        elif voice_sample == "backward":
            data = {
                    'command' : 1
            }
        elif voice_sample == "right":
            data = {
                    'command' : 2
            }
        elif voice_sample == "left":
            data = {
                    'command' : 3
            }
        elif voice_sample == "stop":
            data = {
                    'command' : 4
            }
        else:
            data = {
                    'command' : 5
            }
        fb_db.child("arduino_command").set(data)
        return render_template("output.html", text=voice_sample)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
