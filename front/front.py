import os
import secrets
import requests

from flask import Flask, render_template, session, request, url_for, abort, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('USER_DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from models import User, create_user


def init_db():
    with app.app_context():
        db.create_all()
        db.session.commit()
        if app.debug:
            if User.query.count() == 0:
                create_user('han@solo.com', 'MillFalcon1', 'XXXXXXXXXXX', profile='JUR')


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(user_id)


@app.before_first_request
def setup_app():
    init_db()


@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        context = {}
        if current_user.profile_type == 'FIS':
            template_name = 'fisica.html'
            resp_a = requests.get('%s%s' % (os.getenv('SERVICE_A_ENDPOINT'), current_user.cpf))
            resp_b = requests.get('%s%s' % (os.getenv('SERVICE_B_ENDPOINT'), current_user.cpf))
            context['servicea'] = resp_a.json()
            context['serviceb'] = resp_b.json()
            if current_user.is_subscriber:
                resp_c = requests.get('%s%s' % (os.getenv('SERVICE_C_ENDPOINT'), 
                                                current_user.cpf))
                context['servicec'] = resp_c.json()
        else:
            template_name = 'juridica.html'
            if request.method == 'POST':
                cpf = request.form.get('cpf')
                resp_pontos = requests.get('%s%s' % (os.getenv('SERVICE_B_ENDPOINT'), cpf))
                context['resultado'] = resp_pontos.json()
        return render_template(template_name, **context)
    else:
        return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter(email == email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
    else:
        flash('Verifique seu e-mail e senha')
    return redirect(url_for('home'))



@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
