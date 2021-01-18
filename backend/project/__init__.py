
#################
#### imports ####
#################

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import BaseConfig
import os

################
#### config ####
################

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

from project.controllers.routes import routes_blueprint

# register our blueprints
app.register_blueprint(routes_blueprint)


from project.models import User

login_manager.login_view = "users.login"


## LOGIN ##
@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (UserID) user to retrieve

    """
    return User.query.get(user_id)