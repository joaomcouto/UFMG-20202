<<<<<<< HEAD
from project.extensions import db
import datetime

=======
from project import db
import datetime
>>>>>>> 587e97049ceb5bcf41cfd386da9dd4f22b1e34c3

class Recipe(db.Model):
    __tablename__ = 'receitas'
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    ingredientes = db.Column(db.Text, nullable=False)
    modo_preparo = db.Column(db.Text, nullable=False)
    latest_change_date = db.Column(db.DateTime, nullable=False)
    texto = db.Column(db.Text, nullable=True)
    tempo_preparo = db.Column(db.String(200), nullable=True)
    imagem = db.Column(db.Text, nullable=True)
    autor = db.Column(db.Integer, db.ForeignKey('users.ID'), nullable=False)
    reviews = db.Column(db.Integer, nullable=False)
    stars = db.Column(db.Integer, nullable=False)

    def get_id(self):
        return self.ID

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if type(getattr(self, c.name)) is not datetime.datetime}

class FavoriteRecipes(db.Model):
    __tablename__ = 'favorite_recipes'
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.ID'), nullable=False)
    recipe = db.Column(db.Integer, db.ForeignKey('receitas.ID'), nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    def get_id(self):
        return self.ID

    def is_active(self):
        return self.active

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ReviewRecipe(db.Model):
    __tablename__ = 'review_recipe'
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey('users.ID'), nullable=False)
    recipe = db.Column(db.Integer, db.ForeignKey('receitas.ID'), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    def get_id(self):
        return self.ID
    
    def is_active(self):
        return self.active
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(db.Model):
    __tablename__ = 'users'
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.Text(100), unique=False, nullable=False)
    email = db.Column(db.Text(100), unique=True, nullable=False)
    senha = db.Column(db.Text, nullable=False)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default="true")
    receitas = db.relationship('Recipe', backref='users', lazy=True)


    @property
    def identity(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has an ``identity`` instance
        attribute or property that provides the unique id of the user instance
        """
        return self.ID

    @property
    def rolenames(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``rolenames`` instance
        attribute or property that provides a list of strings that describe the roles
        attached to the user instance
        """
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``password`` instance
        attribute or property that provides the hashed password assigned to the user
        instance
        """
        return self.senha

    @classmethod
    def lookup(cls, username):
        """
        *Required Method*

        flask-praetorian requires that the user class implements a ``lookup()``
        class method that takes a single ``username`` argument and returns a user
        instance if there is one that matches or ``None`` if there is not.
        """
        return User.query.filter_by(email=username).one_or_none()

    @classmethod
    def identify(cls, id):
        """
        *Required Method*

        flask-praetorian requires that the user class implements an ``identify()``
        class method that takes a single ``id`` argument and returns user instance if
        there is one that matches or ``None`` if there is not.
        """
        return User.query.get(id)

    def is_valid(self):
        return self.is_active
    
    def as_dict(self): # Não usa a senha no dic, uma vez que ela está em bytes e não é serializável
        return {
            'UserID' : self.ID,
            'nome'   : self.nome,
            'email'  : self.email
        }