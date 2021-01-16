from flask import Flask, flash, escape, request, render_template, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_bcrypt import Bcrypt
from project import db, bcrypt   # pragma: no cover
from project.models import User, Recipe   # pragma: no cover

################
#### config ####
################

routes_blueprint = Blueprint(
    'routes', __name__,
    template_folder='templates'
)   # pragma: no cover

################
#### routes ####
################

@routes_blueprint.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>"

## USER API
@routes_blueprint.route('/register', methods=['GET', 'POST'])
def create_new_user():
    if request.method == 'GET':
        return "<h1> new user <h1>"
    else:
        newUser = request.form['user']
        newEmail = request.form['user']
        newPassword = request.form['password']       
        save_new_user(newUser, newEmail, newPassword)
        return redirect(url_for('login'))

@routes_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return "<h1>LOGIN PAGE</h1>"
    else:
        loginUser = request.form['user']
        loginPass = request.form['password']
        dbUser = User.query.filter_by(nome=loginUser).first()
        if(bcrypt.check_password_hash(dbUser.senha, loginPass)):
            login_user(dbUser)
            return redirect(url_for('routes.new_recipe'))

@routes_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.login'))

## Recipe API
@routes_blueprint.route('/new_recipe')
@login_required
def new_recipe():
    if request.method == 'GET':
        return"<h1> new Recipe <h1>"
    else:
        title = request.form['title']
        text = request.form['text']
        author = current_user.get_id()  
        save_new_recipe(title, text, author)
        return"<h1> new Recipe registered <h1>"


def save_new_recipe(title, text, author):
    recipe = Recipe(
        titulo = title, 
        texto = text,
        autor = author)

    db.session.add(recipe)
    db.session.commit()

def save_new_user(newUser, newEmail, newPassword):
    user = User(
        nome = newUser, 
        email = newEmail,
        senha = bcrypt.generate_password_hash(newPassword))

    db.session.add(user)
    db.session.commit()