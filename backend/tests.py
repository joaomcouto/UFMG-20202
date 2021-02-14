import unittest

from datetime import datetime
from flask import request
from flask_login import current_user
from baseTest import BaseTestCase

from project.controllers.routes import (save_new_user, save_new_recipe, get_user_recipes_as_dict,
get_recipe_by_filters, edit_recipe, get_recipe_by_id, check_exists_favorite, save_new_favorite, 
unfavorite_recipe, get_favorite_relation)

from project.models import User, Recipe, FavoriteRecipes, ReviewRecipe
import json


class TestCase(BaseTestCase):
    # Ensure that Flask was set up correctly
    def test_index(self):
        with self.client:
            response = self.client.get('/login', content_type='html/text')
            self.assert200(response)

    # Ensure that register page loads
    def test_register_route_works_as_expected(self):
        with self.client:
            response = self.client.get('/register', content_type='html/text')
            self.assert200(response)

    # Ensure that new recipe page requires user login
    def test_main_route_requires_login(self):
        with self.client:
            response = self.client.get('/new_recipe', follow_redirects=True)
            self.assert200(response)
            self.assertEqual('/login', request.path)

    # Ensure user is saved
    def test_save_new_user(self):
        with self.client:
            username = 'test'
            email = 'test@email.com'
            password = 'test123'
            save_new_user(username, email, password)
            savedUser = User.query.filter_by(nome=username).first()
            self.assertEqual(username, savedUser.nome)

    # Ensure that login page login works user login
    def test_login(self):
        with self.client:
            test_data = save_test_user()
        # success
            self.assert200(self.login(test_data))

    # Ensure that logout works
    def test_logout(self):
        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            response = self.client.get('/logout', follow_redirects=True)
            self.assert200(response)
            self.assertFalse(current_user.is_active)

    # Ensure that new recipes page get works
    def test_save_get_new_recipe(self):
        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            response = self.client.get('/new_recipe', content_type='html/text')
            self.assert200(response)

    # Ensure recipe is saved
    def test_save_new_recipe(self):
        newTitle = 'bolo'
        newIngredients = '2 ovos, 100ml leite, fermento'
        newDirections = 'batedeira tudo e assar'

        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newIngredients, newDirections, newAuthor)
            savedRecipe = Recipe.query.filter_by(titulo=newTitle).first()
            self.assertEqual(newAuthor, savedRecipe.autor)
            self.assertEqual(newTitle, savedRecipe.titulo)
            self.assertEqual(newIngredients, savedRecipe.ingredientes)
            self.assertEqual(newDirections, savedRecipe.modo_preparo)

    # Ensure all user recipes are fetched
    def test_get_all_user_recipes(self):
        newTitle = 'bolo'
        newIngredients = '2 ovos, 100ml leite, fermento'
        newDirections = 'batedeira tudo e assar'
        newTitle2 = 'bolo2'
        newIngredients2 = '23 ovos, 1000ml leite, 2 fermento'
        newDirections2 = 'batedeira tudo e assar'

        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newIngredients, newDirections, newAuthor)
            save_new_recipe(newTitle2, newIngredients2, newDirections2, newAuthor)
            savedRecipes = get_user_recipes_as_dict(newAuthor)
            self.assertEqual(len(savedRecipes), 2)

### Tests Sprint 2 - Pedro
    def test_create_new_recipe_required_parameters(self):
        newTitle = 'bolo'
        newIngredients = '2 ovos, 100ml leite, fermento'
        newDirections = 'batedeira tudo e assar'

        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            
            recipe = Recipe(
                titulo = newTitle, 
                ingredientes = newIngredients,
                modo_preparo = newDirections,
                latest_change_date = datetime.now(), 
                autor = current_user.get_id()
                )

            self.assertEqual(recipe.titulo, newTitle)
            self.assertEqual(recipe.ingredientes, newIngredients)
            self.assertEqual(recipe.modo_preparo, newDirections)

    def test_endpoint_get_recipe_with_search_filter(self):        
        newTitle = 'bolo de chocolate'
        newIngredients = '2 ovos, 100ml leite, fermento'
        newDirections = 'batedeira tudo e assar'

        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            save_new_recipe(newTitle, newIngredients, newDirections, current_user.get_id())

            response = self.client.get(
                '/receitas?search=bolo', content_type='html/text')

            self.assert200(response)

    def test_get_recipe_by_filters(self):
        newTitle = 'bolo de chocolate'
        newIngredients = '2 ovos, 100ml leite, fermento'
        newDirections = 'batedeira tudo e assar'

        newTitle2 = 'cake'
        newIngredients2 = '2 ovos, 100ml leite, fermento'
        newDirections2 = 'batedeira tudo e assar'

        newTitle3 = 'bolo'
        newIngredients3 = '2 ovos, 100ml leite, fermento'
        newDirections3 = 'batedeira tudo e assar'

        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newIngredients, newDirections, newAuthor)
            save_new_recipe(newTitle2, newIngredients2, newDirections2, newAuthor)
            save_new_recipe(newTitle3, newIngredients3, newDirections3, newAuthor)
            result = get_recipe_by_filters('bolo', 'titulo', None)
            self.assertEqual(len(result), 2)    

    def test_save_favorite(self):
        newTitle = 'bolo de chocolate'
        newIngredients = '2 ovos, 100ml leite, fermento'
        newDirections = 'batedeira tudo e assar'
        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newIngredients, newDirections, newAuthor)
            save_new_favorite(1, newAuthor)
            self.assertEqual(check_exists_favorite(1, newAuthor), True)
    
    def test_unfavorite(self):
        newTitle = 'bolo de chocolate'
        newIngredients = '2 ovos, 100ml leite, fermento'
        newDirections = 'batedeira tudo e assar'
        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newIngredients, newDirections, newAuthor)
            save_new_favorite(1, newAuthor)
            unfavorite_recipe(1, newAuthor)
            result = get_favorite_relation(1, newAuthor)
            self.assertEqual(result.is_active(), False)

    def test_favorite_status_response(self):
        newTitle = 'bolo de chocolate'
        newIngredients = '2 ovos, 100ml leite, fermento'
        newDirections = 'batedeira tudo e assar'
        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newIngredients, newDirections, newAuthor)
            save_new_favorite(1, newAuthor)
            
            response = self.client.get(
                '/favoriteStatus?id=1', content_type='html/text')

            self.assert200(response)

    def test_get_recipe_by_filters_only_favorites(self):
        newTitle = 'bolo de chocolate'
        newIngredients = '2 ovos, 100ml leite, fermento'
        newDirections = 'batedeira tudo e assar'

        newTitle2 = 'cake'
        newIngredients2 = '2 ovos, 100ml leite, fermento'
        newDirections2 = 'batedeira tudo e assar'

        newTitle3 = 'bolo'
        newIngredients3 = '2 ovos, 100ml leite, fermento'
        newDirections3 = 'batedeira tudo e assar'

        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newIngredients, newDirections, newAuthor)
            save_new_recipe(newTitle2, newIngredients2, newDirections2, newAuthor)
            save_new_recipe(newTitle3, newIngredients3, newDirections3, newAuthor)
            save_new_favorite(1, newAuthor)
            result = get_recipe_by_filters('bolo', 'titulo', True)
            self.assertEqual(len(result), 1)

    def test_get_recipe_by_id(self):
        newTitle = 'bolo de chocolate'
        newIngredients = '2 ovos, 100ml leite, fermento'
        newDirections = 'batedeira tudo e assar'

        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newIngredients, newDirections, newAuthor)
            result = get_recipe_by_id(1)
            self.assertEqual(result.titulo, newTitle)    
            self.assertEqual(result.ingredientes, newIngredients)    
            self.assertEqual(result.modo_preparo, newDirections)

    def test_edit_recipe(self):
        newTitle = 'bolo de chocolate'
        newIngredients = '2 ovos, 100ml leite, fermento'
        newDirections = 'batedeira tudo e assar'

        editTitle = 'pao de queijo'
        editIngredients = 'agua, polvilho, 100ml leite, fermento'
        editDirections = 'na mão, assar'

        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newIngredients, newDirections, newAuthor)
            edit_recipe(1, editTitle, editIngredients, editDirections, newAuthor)
            result = get_recipe_by_id(1)
            self.assertEqual(result.titulo, editTitle)    
            self.assertEqual(result.ingredientes, editIngredients)    
            self.assertEqual(result.modo_preparo, editDirections)  
    
    def test_edit_recipe_endpoint(self):
        newTitle = 'bolo de chocolate'
        newIngredients = '2 ovos, 100ml leite, fermento'
        newDirections = 'batedeira tudo e assar'

        editTitle = 'pao de queijo'
        editIngredients = 'agua, polvilho, 100ml leite, fermento'
        editDirections = 'na mão, assar'

        test_recipe_edit_data = {
            "id": 1,
            "title": editTitle,
            "ingredients": editIngredients,
            "directions": editDirections,
            "text": None,
            "time": None,
            "image": None 
        }

        with self.client:
            test_user_data = save_test_user()
            self.login(test_user_data)
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newIngredients, newDirections, newAuthor)

            response = self.client.post(
                '/edit_recipe', data=json.dumps(test_recipe_edit_data), headers={'Content-type': 'application/json'})
            self.assert200(response)

            result = get_recipe_by_id(1)
            self.assertEqual(result.titulo, editTitle)    
            self.assertEqual(result.ingredientes, editIngredients)    
            self.assertEqual(result.modo_preparo, editDirections)    
    
    def test_delete_recipe(self):
        newTitle = 'bolo de chocolate'
        newIngredients = '2 ovos, 100ml leite, fermento'
        newDirections = 'batedeira tudo e assar'
        
        test_recipe_data = {
            "id": 1,
        }
        
        with self.client:
            test_data = save_test_user()
            self.login(test_data)
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newIngredients, newDirections, newAuthor)
            
            response = self.client.post(
                '/delete_recipe', data=json.dumps(test_recipe_data), headers={'Content-type': 'application/json'})
            result = get_recipe_by_id(1)

            self.assert200(response)
            self.assertEqual(result, None)

# Testes Vinicius
    def test_home_endpoint(self):
        with self.client:
            response = self.client.get('/', content_type='html/text')
            self.assert200(response)

    def test_register_endpoint(self):
        username = 'test'
        email = 'test@email.com'
        password = 'test123'
        test_data = {
            "email": email,
            "name": username,
            "password": password,
        }
        with self.client:
            response = self.client.post(
                '/register', data=json.dumps(test_data), headers={'Content-type': 'application/json'})
            self.assert200(response)

    def test_login_endpoint(self):
        with self.client:
            test_data = save_test_user()
            response = self.client.post(
                '/login', data=json.dumps(test_data), headers={'Content-type': 'application/json'})
            self.assert200(response)

    def test_new_recipe_endpoint(self):
        title = 'titulo de teste'
        ingredients = 'ingredientes de teste'
        directions = 'modo prepraro de teste'
        text = 'texto de teste'
        test_data = {
            "title": title,
            "ingredients": ingredients,
            "directions": directions,
            "text": text,
            "time": None,
            "image": None
        }
        with self.client:
            test_user = save_test_user()
            self.client.post(
                '/login', data=json.dumps(test_user), headers={'Content-type': 'application/json'})
            response = self.client.post(
                '/new_recipe', data=json.dumps(test_data), headers={'Content-type': 'application/json'})
            self.assert200(response)


def save_test_user():
    username = 'test'
    email = 'test@email.com'
    password = 'test123'
    
    save_new_user(username, email, password)

    return  {
            "email": email,
            "name": username,
            "password": password,
            }

if __name__ == '__main__':
    unittest.main()
