from project import db
import datetime

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
    senha = db.Column(db.Text(20), nullable=False)
    receitas = db.relationship('Recipe', backref='users', lazy=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.ID

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    def as_dict(self): # Não usa a senha no dic, uma vez que ela está em bytes e não é serializável
        return {
            'UserID' : self.ID,
            'nome'   : self.nome,
            'email'  : self.email
        }