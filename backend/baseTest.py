from flask_testing import TestCase
from project import app, db, login_manager
from project.models import User, Recipe
import json


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        login_manager.login_view = "routes.login"
        db.create_all()
    
    # Login with the given user info
    def login(self, test_data):
        return self.client.post('/login', data=json.dumps(test_data), headers={'Content-type':'application/json'})
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()