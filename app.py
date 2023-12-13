from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, validators
from flask_session import Session

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)
Session(app)

# Basic configs of sqlite database
app.config['SECRET_KEY'] = 'test'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Create databse table and fields
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(50), unique = True)
    fname = db.Column(db.String(150))
    lname = db.Column(db.String(150))
    password = db.Column(db.String(100))

# define a register& login form class, with valdiator and restrictions
class regForm(FlaskForm):
    username = StringField("User name", validators=[validators.DataRequired(), validators.Length(min = 3, max = 31)])
    fname = StringField("First Name", validators=[validators.DataRequired()])
    lname = StringField("Last name", validators=[validators.DataRequired()])
    password = PasswordField("password", validators = [validators.DataRequired(), validators.Length(min = 5, max = 15)], id='password')
    showPassword = BooleanField('Show password', id='check')
    registerbtn = SubmitField("Register")

class logForm(FlaskForm):
    username = StringField("User name", validators=[validators.DataRequired(), validators.Length(min = 3, max = 31)])
    password = PasswordField("password", validators = [validators.DataRequired(), validators.Length(min = 5, max = 15)], id='password')
    showPassword = BooleanField('Show password', id='check')
    loginbtn = SubmitField("Log in")

db.create_all()

# web root page, which render index.html
@app.route('/')
def index():
    if not session.get("username"):
        #if user not recognised redirect them to login page
        # this here protectthe main page
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/register', methods = ["GET", "POST"])
def register():
    rForm = regForm(request.form)
    if request.method == "POST":
        if rForm.validate_on_submit():
            # get user generated data from wtforms
            username = rForm.username.data
            fname = rForm.fname.data
            lname = rForm.lname.data
            password = rForm.password.data

            # if this returns a user, then the user already exists in database
            user = User.query.filter_by(username = username).first()

            if user: # if a user is found, we want to redirect back to login page so user can try again
                flash(u'Entered User name is already exists, try loging in!', 'warning')
                return redirect(url_for('login'))

            # create a new user with the form data. Hash the password so the plaintext version isn't saved.
            new_user = User(username = username, fname = fname, lname = lname, password = generate_password_hash(password, method = 'sha256'))

            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect(url_for('index'))
    return render_template('register.html', form = rForm)\
    
@app.route('/login', methods = ["GET", "POST"])
def login():
    lForm = logForm(request.form)
    if request.method == "POST":
        if lForm.validate_on_submit():
            username = lForm.username.data
            password = lForm.password.data

            user = User.query.filter_by(username = username).first()

            # check if the user actually exists
            # take the user's password, hash it, and compare it to the hashed password in the database
            if not user:
                flash('User name not found, please try signing up!')
                return redirect(url_for('register')) # if the user doesn't exist, redirect to register page
            # if password is wrong, ask user to try again
            elif not check_password_hash(user.password, password):
                flash(u'Password is wrong! Try again.', 'error')
            # none of the aboves? user can log in now
            else:
                session['username'] = username
                return redirect(url_for('index'))
    return render_template('login.html', form = lForm)

@app.route('/logout')
def logout():
    session['username'] = None
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug = True)
