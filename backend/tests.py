import unittest

from flask import request
from flask_login import current_user
from baseTest import BaseTestCase
from project.controllers.routes import save_new_user, save_new_recipe, get_user_recipes_as_dict
from project.models import User, Recipe
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
        username = 'test'
        email = 'test@email.com'
        password = 'test123'
        teste_data = {
            "email":email,
            "name":username,
            "password":password,
            }
        with self.client:
            save_new_user(username, email, password)
        # success
            self.assert200(self.login(teste_data))
  
    # Ensure that logout works
    def test_logout(self):
        username = 'test'
        email = 'test@email.com'
        password = 'test123'
        teste_data = {
            "email":email,
            "name":username,
            "password":password,
            }
        with self.client:
            save_new_user(username, email, password)
            self.login(teste_data)
            response = self.client.get('/logout', follow_redirects=True)
            self.assert200(response)
            self.assertFalse(current_user.is_active)
    
    # Ensure that new recipes page get works
    def test_save_get_new_recipe(self):
        username = 'test'
        email = 'test@email.com'
        password = 'test123'
        teste_data = {
            "email":email,
            "name":username,
            "password":password,
            }
        with self.client:
            save_new_user(username, email, password)
            self.login(teste_data)
            response = self.client.get('/new_recipe', content_type='html/text')
            self.assert200(response)


    # Ensure recipe is saved
    def test_save_new_recipe(self):
        username = 'test'
        email = 'test@email.com'
        password = 'test1234'
        newTitle = 'bolo'
        newText = '2 ovos, 100ml leite, fermento'
        teste_data = {
            "email":email,
            "name":username,
            "password":password,
            }
        with self.client:
            save_new_user(username, email, password)
            self.login(teste_data)     
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newText, newAuthor)
            savedRecipe = Recipe.query.filter_by(titulo=newTitle).first()
            self.assertEqual(newAuthor, savedRecipe.autor)
            self.assertEqual(newTitle, savedRecipe.titulo)
            self.assertEqual(newText, savedRecipe.texto)
    
    # Ensure all user recipes are fetched
    def test_get_all_user_recipes(self):
        username = 'test'
        email = 'test@email.com'
        password = 'test123'
        newTitle = 'bolo'
        newText = '2 ovos, 100ml leite, fermento'
        newTitle2 = 'bolo2'
        newText2 = '23 ovos, 1000ml leite, 2 fermento'
        teste_data = {
            "email":email,
            "name":username,
            "password":password,
            }
        with self.client:
            save_new_user(username, email, password)
            self.login(teste_data)            
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newText, newAuthor)
            save_new_recipe(newTitle2, newText2, newAuthor)
            savedRecipes = get_user_recipes_as_dict(newAuthor)
            self.assertEqual(len(savedRecipes), 2)

#Testes Vinicius

    def teste_home_endpoint(self):
        with self.client:
            response = self.client.get('/', content_type='html/text')
            self.assert200(response)

    def test_register_endpoint(self):
        username = 'test'
        email = 'test@email.com'
        password = 'test123'
        teste_data = {
            "email":email,
            "name":username,
            "password":password,
            }
        with self.client:
            response = self.client.post('/register', content_type='html/text', data=teste_data)
            self.assert200(response)


if __name__ == '__main__':
    unittest.main()