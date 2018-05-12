import os
import json
import tempfile

import pytest

from api import app

SERVICEA_RESPONSE = os.path.join(os.path.dirname(__file__), 'service-a.json')
SERVICEB_RESPONSE = os.path.join(os.path.dirname(__file__), 'service-b.json')
SERVICEC_RESPONSE = os.path.join(os.path.dirname(__file__), 'service-c.json')

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_service_a(client):
    """Testa se o serviço A está retornando uma resposta correta"""
    expected_response = json.load(open(SERVICEA_RESPONSE))
    rv = client.get('/servicea/XXXXXXXXXXX')
    generated_response = json.loads(rv.data)
    assert generated_response['cpf'] == expected_response['cpf']
    assert len(generated_response['debts']) == len(expected_response['debts'])


def test_service_b(client):
    """Testa se o serviço A está retornando uma resposta correta"""
    expected_response = json.load(open(SERVICEB_RESPONSE))
    rv = client.get('/serviceb/XXXXXXXXXXX')
    generated_response = json.loads(rv.data)
    assert generated_response['cpf'] == expected_response['cpf']
    assert generated_response['points'] == expected_response['points']


def test_service_c(client):
    """Testa se o serviço A está retornando uma resposta correta"""
    expected_response = json.load(open(SERVICEC_RESPONSE))
    rv = client.get('/servicec/XXXXXXXXXXX')
    generated_response = json.loads(rv.data)
    assert len(generated_response) == len(expected_response)