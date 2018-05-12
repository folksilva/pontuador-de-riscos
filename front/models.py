from front import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class User(db.Model, UserMixin):
    """
    Modelo de usuário

        - email: Email do usuário, usado para identificação
        - password: Senha do usuário
        - cpf: CPF do usuário
        - is_subscriber: O usuário é assinante?
        - profile_type: O perfil do usuário, opções disponíveis:
            - FIS: Pessoa Física
            - JUR: Pessoa Jurídica
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    cpf = db.Column(db.String(14), unique=True, nullable=True)
    is_subscriber = db.Column(db.Boolean, default=False)
    profile_type = db.Column(db.String(3), default='FIS')


def create_user(email, password, cpf, profile='FIS', is_subscriber=False):
    user = User()
    user.email = email
    user.password = generate_password_hash(password)
    user.cpf = cpf
    user.profile_type = profile
    user.is_subscriber = is_subscriber
    db.session.add(user)
    db.session.commit()


