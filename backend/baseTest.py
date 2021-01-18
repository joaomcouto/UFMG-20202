from flask_testing import TestCase
from project import app, db, login_manager
from project.models import User, Recipe


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
    
    # Login with the given user info
    def login(self, user, password):
        return self.client.post('/login', data=dict(user = user, password = password))
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()