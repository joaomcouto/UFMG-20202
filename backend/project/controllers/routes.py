from flask import Flask, flash, escape, request, render_template, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_bcrypt import Bcrypt
from project import db, bcrypt   # pragma: no cover
from project.models import User, Recipe   # pragma: no cover
import json

OK = json.dumps({'success':True}), 200, {'ContentType':'application/json'}

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
        return OK
    else:
        data = request.get_json()
        newUser = data['name']
        newEmail = data['email']
        newPassword = data['password']
        save_new_user(newUser, newEmail, newPassword)
        dbUser = User.query.filter_by(email=newEmail).first()
        return json.dumps(dbUser.as_dict()) #redirect(url_for('login'))

@routes_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return OK
    else:
        data = request.get_json()
        loginUser = data['email']
        loginPass = data['password']
        dbUser = User.query.filter_by(email=loginUser).first()
        if(bcrypt.check_password_hash(dbUser.senha, loginPass)):
            login_user(dbUser)
            return json.dumps(dbUser.as_dict()) #redirect(url_for('routes.new_recipe'))
        else:
            return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

@routes_blueprint.route('/logout')
def logout():
    logout_user()
    return OK #redirect(url_for('routes.login'))

## Recipe API
@routes_blueprint.route('/new_recipe', methods=['GET', 'POST'])
@login_required
def new_recipe():
    if request.method == 'GET':
        return OK
    else:
        data = request.get_json()
        title = data['title']
        text = data['text']
        author = current_user.get_id()  
        save_new_recipe(title, text, author)
        return OK #"<h1> new Recipe registered <h1>"

@routes_blueprint.route('/user_all_recipes')
@login_required
def get_user_recipes():
    return json.dumps(get_user_recipes_as_dict(current_user.get_id()))

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

def get_user_recipes_as_dict(id):
    recipeObjs = Recipe.query.filter_by(autor=id).all()
    recipes = {}
    for x in recipeObjs:
        recipes[x.get_id()] = x.as_dict() 
    return recipes

@routes_blueprint.route('/receitas', methods=['GET'])
@login_required
def get_recipe_by_search():
    search = request.args.get('search',type=str)
    if (search):
        
        return json.dumps({'success': True, 'search': search}), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}