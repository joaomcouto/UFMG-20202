from project import db

class Recipe(db.Model):
    __tablename__ = 'receitas'
    ReceitaID = db.Column(db.Integer, primary_key=True, nullable=False)
    titulo = db.Column(db.String(20), nullable=False)
    texto = db.Column(db.Text, nullable=False)
    autor = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)

    def get_id(self):
        """Return the id to satisfy Flask-Login's requirements."""
        return self.ReceitaID

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(db.Model):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(20), nullable=False)
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