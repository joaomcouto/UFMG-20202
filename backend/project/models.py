from project import db

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
    autor = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)

    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.ID

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(db.Model):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True, nullable=False)
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
        return self.UserID

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    
    def as_dict(self): # Não usa a senha no dic, uma vez que ela está em bytes e não é serializável
        return {
            'UserID' : self.UserID,
            'nome'   : self.nome,
            'email'  : self.email
        }