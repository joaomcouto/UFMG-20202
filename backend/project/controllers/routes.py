from flask import Flask, flash, escape, request, render_template, redirect, url_for, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_bcrypt import Bcrypt
from project import db, bcrypt   # pragma: no cover
from project.models import User, Recipe, FavoriteRecipes, ReviewRecipe  # pragma: no cover
import json
from datetime import datetime

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
        try:
            data = request.get_json()
            newUser = data['name']
            newEmail = data['email']
            newPassword = data['password']
            save_new_user(newUser, newEmail, newPassword)
            dbUser = User.query.filter_by(email=newEmail).first()
            return json.dumps(dbUser.as_dict())
       
        except:
            return json.dumps({'success':False}), 505, {'ContentType':'application/json'}

@routes_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return OK
    else:
        try:
            data = request.get_json()
            loginUser = data['email']
            loginPass = data['password']
            dbUser = User.query.filter_by(email=loginUser).first()
            if(bcrypt.check_password_hash(dbUser.senha, loginPass)):
                login_user(dbUser)
                return json.dumps(dbUser.as_dict())
                
            else:
                return json.dumps({'success':False}), 400, {'ContentType':'application/json'}
            
        except:
            return json.dumps({'success':False}), 505, {'ContentType':'application/json'}

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
        try:
            data = request.get_json()
            title = data['title']
            ingredients = data['ingredients']
            directions = data['directions']
            author = current_user.get_id() 
            time = data['time'] 
            text = data['text']
            image = data['image']
            save_new_recipe(title, ingredients, directions, author, time, text, image)
            return OK 
        except:
            return json.dumps({'success':False}), 505, {'ContentType':'application/json'}

@routes_blueprint.route('/edit_recipe', methods=['GET', 'POST'])
@login_required
def edit_recipe():
    if request.method == 'GET':
        return OK
    else:
        try:
            data = request.get_json()
            ID = data['id']
            title = data['title']
            ingredients = data['ingredients']
            directions = data['directions']
            author = current_user.get_id() 
            time = data['time'] 
            text = data['text']
            image = data['image']
            edit_recipe(ID, title, ingredients, directions, author, time, text, image)
            return OK
        except:
            return json.dumps({'success':False}), 505, {'ContentType':'application/json'}

@routes_blueprint.route('/delete_recipe', methods=['POST'])
@login_required
def delete_recipe():   
    try:
        data = request.get_json()
        ID = data['id']
        delete_recipe(ID)
        return OK
    except:
        return json.dumps({'success':False}), 505, {'ContentType':'application/json'}


@routes_blueprint.route('/receitas/user_all_recipes', methods=['GET'])
@login_required
def get_user_recipes():
    return json.dumps(get_user_recipes_as_dict(current_user.get_id()), default=str)

@routes_blueprint.route('/receitas', methods=['GET'])
@login_required
def get_recipe_by_search():
    search = request.args.get('search',type=str)
    orderBy = request.args.get('orderBy',type=str)
    favorites = request.args.get('favorites', type=str)
    
    try:
        return json.dumps(get_recipe_by_filters(search, orderBy, favorites), default=str)

    except:    
        return json.dumps({'success':False}), 505, {'ContentType':'application/json'}
        
@routes_blueprint.route('/receitas/ById', methods=['GET'])
@login_required
def get_recipe_by_ID():
    Id = request.args.get('id', type=str)

    if(Id):
        try:
            return json.dumps(get_recipe_by_id(Id))
        except:
            return json.dumps({'success':False}), 505, {'ContentType':'application/json'}
    else:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

@routes_blueprint.route('/favorite', methods=['POST'])
@login_required
def favorite_or_unfavorite_a_recipe():
    data = request.get_json()
    ID = data['id']
    author = current_user.get_id()

    if(check_exists_favorite(ID, author)):
        try:
            unfavorite_recipe(ID, author)           
            return OK
        except:
            return json.dumps({'success':False}), 505, {'ContentType':'application/json'}

    else:
        try:
            save_new_favorite(Id, author)
            return OK
        except:
            return json.dumps({'success':False}), 505, {'ContentType':'application/json'}

@routes_blueprint.route('/favoriteStatus', methods=['GET'])
@login_required
def favorite_status():
    ID = request.args.get('id',type=str)
    author = current_user.get_id()

    if(ID):
        favorite = FavoriteRecipes.query.filter(FavoriteRecipes.recipe == ID)\
                                .filter(FavoriteRecipes.user == author)\
                                .first()
        return (json.dumps(True) if favorite else json.dumps(False))
    else:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

###########################################
#### User Functions #######################
###########################################
def save_new_user(newUser, newEmail, newPassword):
    user = User(
        nome = newUser, 
        email = newEmail,
        senha = bcrypt.generate_password_hash(newPassword))

    db.session.add(user)
    db.session.commit()

###########################################
#### Recipe Functions #####################
###########################################
def save_new_recipe(title, ingredients, directions, author, time=None, text=None, image=None):
    recipe = Recipe(
        titulo = title,
        ingredientes = ingredients,
        modo_preparo = directions,
        latest_change_date = datetime.now(),
        autor = author,
        tempo_preparo = time,
        texto = text,
        imagem = image
        )

    db.session.add(recipe)
    db.session.commit()

def get_recipe_by_id(id):
    return Recipe.query.filter(Recipe.ID == id).first()

def get_user_recipes_as_dict(id):
    recipeObjs = Recipe.query.filter(Recipe.autor == id).all()
    recipes = {}
    for x in recipeObjs:
        recipes[x.get_id()] = x.as_dict() 
    return recipes

def get_recipe_by_filters(search, orderBy, favorite):
    query = Recipe.query
    if(search):
        query = query.filter(Recipe.titulo.like("%"+search+"%"))  
    
    if(favorite):
        favorites = FavoriteRecipes.query.filter(FavoriteRecipes.user == current_user.get_id()).all()
        favorites = [x.recipe for x in favorites]
        query = query.filter(Recipe.ID.in_(favorites))
    
    if(orderBy):
        query = query.order_by(orderBy)

    recipeObjs = query.order_by(Recipe.latest_change_date).all()
    recipes = {}

    for x in recipeObjs:
        recipes[x.get_id()] = x.as_dict() 

    return recipes

def edit_recipe(id, title, ingredients, directions, author, time=None, text=None, image=None):
    recipe = Recipe.query.filter(Recipe.ID == id).first()
    
    recipe.titulo              = title
    recipe.ingredientes        = ingredients
    recipe.modo_preparo        = directions
    recipe.tempo_preparo       = time
    recipe.texto               = text
    recipe.imagem              = image
    recipe.latest_change_date  = datetime.now()

    db.session.commit()

    return recipe

def delete_recipe(id):
    Recipe.query.filter(Recipe.ID == id).delete()
    db.session.commit()

###########################################
#### Favorite Functions ###################
###########################################

def check_exists_favorite(id, author):
    exists = FavoriteRecipes.query.filter(FavoriteRecipes.recipe == id)\
                            .filter(FavoriteRecipes.user == author).all()
    return(len(exists) > 0)

def save_new_favorite(id, author):
    newFavorite = FavoriteRecipes(user = author, recipe = id, active = True)
    db.session.add(newFavorite)
    db.session.commit()

def unfavorite_recipe(id, author):
    recipe = FavoriteRecipes.query.filter(FavoriteRecipes.recipe == id)\
                            .filter(FavoriteRecipes.user == author).first()
    recipe.active = False
    db.session.commit()

def get_favorite_relation(id, author):
    return FavoriteRecipes.query.filter(FavoriteRecipes.recipe == id)\
                            .filter(FavoriteRecipes.user == author).first()
    