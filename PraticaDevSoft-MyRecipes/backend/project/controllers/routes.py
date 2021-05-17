from flask import Flask, flash, escape, request, render_template, redirect, url_for, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_praetorian import auth_required, current_user, auth_accepted
from sqlalchemy import desc
from project import app, db, bcrypt, guard, User   # pragma: no cover
from project.models import Recipe, FavoriteRecipes, ReviewRecipe  # pragma: no cover
import json
from datetime import datetime
import traceback
import os

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
            access = { 'access_token': guard.encode_jwt_token(dbUser) }
            login_info = dict(dbUser.as_dict(), **access)
            return json.dumps(login_info)

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
            loggedUser = guard.authenticate(loginUser, loginPass)
            
            access = { 'access_token': guard.encode_jwt_token(loggedUser) }
            login_info = dict(dbUser.as_dict(), **access)
            return json.dumps(login_info)   
        except Exception as e:
            print("Exception:", e)
            return json.dumps({'success':False}), 505, {'ContentType':'application/json'}

@routes_blueprint.route('/refresh', methods=['GET'])
def refresh():
    """
    Refreshes an existing JWT by creating a new one that is a copy of the old
    except that it has a refrehsed access expiration.
    """
    old_token = guard.read_token_from_header()
    new_token = guard.refresh_jwt_token(old_token)
    access = {'access_token': new_token}
    return json.dumps(access)

@routes_blueprint.route('/logout')
@auth_required
def logout():
    return OK 

## Recipe API
@routes_blueprint.route('/new_recipe', methods=['GET', 'POST'])
@auth_required
def new_recipe():
    if request.method == 'GET':
        return OK
    else:
        try:
            
            data = request.form.to_dict()
            #print(data)
            #print(current_user())
            title = data['title']
            ingredients = data['ingredients']
            directions = data['directions']
            author = data['userId']
            time = data['time'] 
            text = data['text']
            
            try:
                image = data['image']
            except:
                image = ''

            recipe = save_new_recipe(title, ingredients, directions, author, time, text, image)
            return json.dumps({'success': True, 'id': recipe.ID}), 201, {'ContentType':'application/json'}
        except Exception as e:
            traceback.print_exc()
            return json.dumps({'success':False}), 505, {'ContentType':'application/json'}

@routes_blueprint.route('/edit_recipe', methods=['GET', 'POST'])
@auth_required
def edit_recipe():
    if request.method == 'GET':
        return OK
    else:
        try:
            data = request.form.to_dict()
            ID = data['id']
            title = data['title']
            ingredients = data['ingredients']
            directions = data['directions']
            author = current_user().identity
            time = data['time'] 
            text = data['text']
            # image = data['image']
            image =''
            edit_recipe(ID, title, ingredients, directions, author, time, text, image)
            return OK
        except Exception as e:
            print("Exception:", e)
            return json.dumps({'success':False}), 505, {'ContentType':'application/json'}

@routes_blueprint.route('/delete_recipe', methods=['POST'])
@auth_required
def delete_recipe():   
    try:
        data = request.get_json()
        #print(data)
        ID = data['id']
        delete_recipe(ID)
        return OK
    except Exception as e:
        print("Exception:", e)
        return json.dumps({'success':False}), 505, {'ContentType':'application/json'}


@routes_blueprint.route('/receitas/user_all_recipes', methods=['GET'])
@auth_required
def get_user_recipes():
    return json.dumps(get_user_recipes_as_dict(current_user().identity), default=str)

@routes_blueprint.route('/receitas', methods=['GET'])
def get_recipe_by_search():
    search = request.args.get('search',type=str)
    orderBy = request.args.get('orderBy',type=str)
    limit = request.args.get('limit',type=str)
    
    try:
        return json.dumps(get_recipe_by_filters(search, orderBy, limit=limit), default=str)

    except Exception as e:
        print("Exception:", e)
        return json.dumps({'success':False}), 505, {'ContentType':'application/json'}

@routes_blueprint.route('/receitas/favoritas', methods=['GET'])
@auth_required
def get_favorite_recipe_by_search():
    search = request.args.get('search',type=str)
    orderBy = request.args.get('orderBy',type=str)
    favorites = True
    id = current_user().identity
    
    try:
        return json.dumps(get_recipe_by_filters(search, orderBy, favorites, id), default=str)

    except Exception as e:    
        return json.dumps({'success':False}), 505, {'ContentType':'application/json'}

@routes_blueprint.route('/receitas/<id>', methods=['GET'])
@auth_accepted
def get_recipe_by_ID(id):
    if(id):
        try:
            token = guard.read_token_from_header()
        except:
            token = '';
        
        try:
            recipe = get_recipe_by_id(int(id))
            if(token != ''):
                author = current_user().identity
                favorite_status = get_favorite_relation(id, author).is_active() if check_exists_favorite(id, author) else False
                 
                all_recipe_info = dict(recipe, **{'favorite_status': favorite_status})
                return json.dumps(all_recipe_info), 200, {'ContentType':'application/json'}

            return json.dumps(recipe), 200, {'ContentType':'application/json'}
        except Exception as e:
            print("Exception:", e)
            return json.dumps({'success':False}), 505, {'ContentType':'application/json'}
    else:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

@routes_blueprint.route('/favorite', methods=['POST'])
@auth_required
def favorite_or_unfavorite_a_recipe():
    data = request.get_json()
    ID = data['id']
    author = current_user().identity

    if(check_exists_favorite(ID, author)):
        try:
            if(check_favorite_relation_status(ID, author)):
                unfavorite_recipe(ID, author)           
            else:
                favorite_recipe(ID, author)
            return OK
        except:
            return json.dumps({'success':False}), 505, {'ContentType':'application/json'}

    else:
        try:
            save_new_favorite(ID, author)
            return OK
        except:
            return json.dumps({'success':False}), 505, {'ContentType':'application/json'}

@routes_blueprint.route('/favoriteStatus', methods=['GET'])
@auth_required
def favorite_status():
    ID = request.args.get('id',type=str)
    author = current_user().identity

    if(ID):
        favorite = FavoriteRecipes.query.filter(FavoriteRecipes.recipe == ID)\
                                .filter(FavoriteRecipes.user == author)\
                                .filter(FavoriteRecipes.active == True)\
                                .first()
        return (json.dumps(True) if favorite else json.dumps(False))
    else:
        return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

@routes_blueprint.route('/submit_review', methods=['POST'])
@auth_required
def submit_review():
    data = request.get_json()
    ID = data['id']
    stars = data['stars']
    author = current_user().identity

    if(check_exists_review(ID, author)):
        return json.dumps({'success': False}), 505, {'ContentType':'application/json'}
    else:
        try:
            submit_new_review(ID, author, stars)
            return OK
        except:
            return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

@routes_blueprint.route('/average_stars', methods=['GET'])
@auth_required
def average_reviews():
    ID = request.args.get('id', type=str)

    if(ID):
        recipe = Recipe.query.filter(Recipe.ID == ID).first()
        average = recipe.stars / recipe.reviews
        data = {
            'average': average
        }
        return (json.dumps(data))

###########################################
#### User Functions #######################
###########################################
def save_new_user(newUser, newEmail, newPassword):
    user = User(
        nome = newUser, 
        email = newEmail,
        senha = guard.hash_password(newPassword))

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
        imagem = upload_file(image) if image != None else image,
        reviews = 0,
        stars = 0
        )

    db.session.add(recipe)
    db.session.commit()
    return recipe

def get_recipe_by_id(id):
    recipe = Recipe.query.filter(Recipe.ID == id).first()
    if(recipe != None):
        author = User.query.filter(User.ID == recipe.autor).first()
        #author = User.query.first()
        #print(recipe.as_dict())
        #print(author.as_dict())
        all_recipe_info = dict(recipe.as_dict(), **author.as_dict())
        return all_recipe_info
    else:
        return recipe

def get_user_recipes_as_dict(id):
    recipeObjs = Recipe.query.filter(Recipe.autor == id).all()
    recipes = []
    for x in recipeObjs:
        recipes.append(get_recipe_by_id(x.get_id()))

    return recipes

def get_recipe_by_filters(search, orderBy, favorite=False, id=None, limit=None):
    query = Recipe.query
    if(search):
        query = query.filter(Recipe.titulo.like("%"+search+"%"))  
    
    if(favorite):
        query = filterWithFavorites(query, id)
    
    query = query.order_by(orderBy) if orderBy else query.order_by(Recipe.latest_change_date)

    recipeObjs = query.all()
    recipeObjs.reverse()

    recipeObjs = recipeObjs if not limit else recipeObjs[:int(limit)]
    recipes = []

    for x in recipeObjs:
        recipes.append(get_recipe_by_id(x.get_id()))

    return recipes

def filterWithFavorites(query, id):
    favorites = FavoriteRecipes.query.filter(FavoriteRecipes.user == id)\
                                        .filter(FavoriteRecipes.active == True).all()
    favorites = [x.recipe for x in favorites]
    query = query.filter(Recipe.ID.in_(favorites))
    return query

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

def check_favorite_relation_status(id, author):
    active = FavoriteRecipes.query.filter(FavoriteRecipes.recipe == id)\
                            .filter(FavoriteRecipes.user == author).first()
    return active.is_active()

def save_new_favorite(id, author):
    #if(check_exists_favorite(id, author)):
    newFavorite = FavoriteRecipes(user = author, recipe = id, active = True)
    db.session.add(newFavorite)
    db.session.commit()

def unfavorite_recipe(id, author):
    recipe = FavoriteRecipes.query.filter(FavoriteRecipes.recipe == id)\
                            .filter(FavoriteRecipes.user == author).first()
    recipe.active = False
    db.session.commit()

def favorite_recipe(id, author):
    recipe = FavoriteRecipes.query.filter(FavoriteRecipes.recipe == id)\
                            .filter(FavoriteRecipes.user == author).first()
    recipe.active = True
    db.session.commit()

def get_favorite_relation(id, author):
    return FavoriteRecipes.query.filter(FavoriteRecipes.recipe == id)\
                            .filter(FavoriteRecipes.user == author).first()



###########################################
#### Review Functions #####################
###########################################

def check_exists_review(id, author):
    exists = ReviewRecipe.query.filter(ReviewRecipe.recipe == id)\
                            .filter(ReviewRecipe.user == author).all()
    return(len(exists) > 0)

def submit_new_review(id, author, stars):
    review = ReviewRecipe(
        score = stars,
        user = author,
        recipe = id,
        active = True
    )
    recipe = Recipe.query.filter(Recipe.ID == id).first()
    recipe.reviews = recipe.reviews + 1
    recipe.stars = recipe.stars + stars
    
    db.session.add(review)
    db.session.commit()


###########################################
#### File Upload ##########################
###########################################
def upload_file(newFile):
    # try:
    #     filename = newFile.filename
    # except:
    #     filename = newFile[1]

    # print(filename)
    # path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # newFile.save(path)
    # return path
    return None

