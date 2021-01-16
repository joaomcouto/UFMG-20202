import unittest

from flask import request
from flask_login import current_user
from baseTest import BaseTestCase
from project.controllers.routes import save_new_user, save_new_recipe
from project.models import User, Recipe



class TestCase(BaseTestCase):
     # Ensure that Flask was set up correctly
    def test_index(self):
        with self.client:
            response = self.client.get('/login', content_type='html/text')
            self.assertEqual(response.status_code, 200)

    # Ensure that register page loads
    def test_register_route_works_as_expected(self):
        with self.client:
            response = self.client.get('/register', content_type='html/text')
            self.assertEqual(response.status_code, 200)

    # Ensure that new recipe page requires user login
    def test_main_route_requires_login(self):
        with self.client:
            self.assertEqual(200, self.client.get('/new_recipe', follow_redirects=True).status_code)
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

    # Ensure that login page login works user login, redirects to new_recipe
    def test_login(self):
        user = 'test'
        email = 'test@email.com'
        password = 'test123'
        with self.client:
            save_new_user(user, email, password)
        # success
            self.assertEqual(302, self.login(user, password).status_code)
  
    # Ensure that logout works
    def test_logout(self):
        user = 'test'
        email = 'test@email.com'
        password = 'test123'
        with self.client:
            save_new_user(user, email, password)
            self.login(user, password)
            response = self.client.get('/logout', follow_redirects=True)
            self.assertEqual(200, response.status_code)
            self.assertFalse(current_user.is_active)
    
    # Ensure that new recipes page get works
    def test_save_get_new_recipe(self):
        username = 'test'
        email = 'test@email.com'
        password = 'test123'
        with self.client:
            save_new_user(username, email, password)
            self.login(username, password)
            newAuthor = current_user.get_id()
            response = self.client.get('/new_recipe', content_type='html/text')
            self.assertEqual(200, response.status_code)


    # Ensure recipe is saved
    def test_save_new_recipe(self):
        username = 'test'
        email = 'test@email.com'
        password = 'test123'
        newTitle = 'bolo'
        newText = '2 ovos, 100ml leite, fermento'
        with self.client:
            save_new_user(username, email, password)
            self.login(username, password)            
            newAuthor = current_user.get_id()
            save_new_recipe(newTitle, newText, newAuthor)
            savedRecipe = Recipe.query.filter_by(titulo=newTitle).first()
            self.assertEqual(newAuthor, savedRecipe.autor)
            self.assertEqual(newTitle, savedRecipe.titulo)
            self.assertEqual(newText, savedRecipe.texto)

if __name__ == '__main__':
    unittest.main()