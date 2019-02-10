from flask import Flask, render_template, url_for, flash, redirect
from form import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time

app = Flask(__name__)
#protects from CSRF(cross site request frodgery) and cookies
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) #posts object has relatioship with Post class
    # backref='author' returns the complete user model
    def __repr__(self):
        return "User('{self.username}', '{self.email}', '{self.image_file}')".format(self=self)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #Foreign key refernce relationship with User class

    def __repr__(self):
		return "Post('{self.title}', '{self.date_posted}')".format(self=self)

posts = [
    {
        'author': 'Elango',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': time.ctime()
    },
    {
        'author': 'Nike',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': time.ctime()
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash('Account created for {}!'.format(form.username.data), 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
	app.run(debug=True)