import os
import tempfile

import pytest

from flask import session
from front import app, init_db
from models import create_user

PESSOA_FISICA_SIMPLES_EMAIL = 'pessoa@fisica.simples'
PESSOA_FISICA_ASSINANTE_EMAIL = 'pessoa@fisica.assinante'
PESSOA_JURIDICA_EMAIL = 'pessoa@juridica'
SENHA = 'senhaParaTeste'

@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_fname
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        init_db()
    
    yield client

    os.close(db_fd)
    os.unlink(db_fname)


def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_nouser(client):
    """Testa um acesso a tela sem usuário logado"""
    rv = client.get('/')
    assert 'Faça login' in rv.data.decode('utf-8')


def test_pessoa_fisica_simples(client):
    """Testa o acesso de uma pessoa física simples"""
    create_user(PESSOA_FISICA_SIMPLES_EMAIL, SENHA, 'XXXXXXXXXXX', 'FIS', False)
    rv = login(client, PESSOA_FISICA_SIMPLES_EMAIL, SENHA)
    assert 'Bem vindo, Han Solo!' in rv.data.decode('utf-8')
    assert 'Nunca venda para ele!' in rv.data.decode('utf-8')
    assert 'Jabba the Hutt' in rv.data.decode('utf-8')
    rv = logout(client)
    assert 'Faça login' in rv.data.decode('utf-8')


def test_pessoa_fisica_assinatura(client):
    """Testa o acesso de uma pessoa física com assinatura"""
    create_user(PESSOA_FISICA_ASSINANTE_EMAIL, SENHA, 'XXXXXXXXXXX', 'FIS', True)
    rv = login(client, PESSOA_FISICA_ASSINANTE_EMAIL, SENHA)
    assert 'Bem vindo, Han Solo!' in rv.data.decode('utf-8')
    assert 'Corporação de Engenharia Corelliana' in rv.data.decode('utf-8')
    assert 'Canto Bight' in rv.data.decode('utf-8')
    rv = logout(client)
    assert 'Faça login' in rv.data.decode('utf-8')


def test_pessoa_juridica_login(client):
    """Testa o acesso de uma pessoa jurídica"""
    create_user(PESSOA_JURIDICA_EMAIL, SENHA, 'XXXXXXXXXXX', 'JUR', False)
    rv = login(client, PESSOA_JURIDICA_EMAIL, SENHA)
    rv = client.get('/')
    assert 'Consulte um CPF' in rv.data.decode('utf-8')
    rv = logout(client)
    assert 'Faça login' in rv.data.decode('utf-8')


def test_pessoa_juridica_consulta(client):
    """Testa o acesso de uma pessoa jurídica consultando um CPF"""
    create_user(PESSOA_JURIDICA_EMAIL, SENHA, 'XXXXXXXXXXX', 'JUR', False)
    login(client, PESSOA_JURIDICA_EMAIL, SENHA)
    rv = client.post('/', data=dict(cpf='XXXXXXXXXXX'))
    assert 'Nunca venda para ele!' in rv.data.decode('utf-8')
    rv = logout(client)
    assert 'Faça login' in rv.data.decode('utf-8')
