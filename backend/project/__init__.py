
#################
#### imports ####
#################

from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_praetorian import Praetorian
from project.extensions import db, guard
from project.models import User
from config import BaseConfig
import os


################
#### config ####
################

app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config.from_object(BaseConfig)
db.init_app(app)
guard.init_app(app, User)


from project.controllers.routes import routes_blueprint

# register our blueprints
app.register_blueprint(routes_blueprint)


from project.models import User

