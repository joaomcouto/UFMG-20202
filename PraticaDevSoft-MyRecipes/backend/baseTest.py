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
    
    def login_token(self, test_data):
        return json.loads(self.login(test_data).data)['access_token']

    def login_id_and_token(self, test_data):
        logged = json.loads(self.login(test_data).data)
        return(logged['UserID'], logged['access_token'])

    def tearDown(self):
        db.session.remove()
        db.drop_all()