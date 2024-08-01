import pytest
from flask import json
from config import app, db 
from models import Parcel, Destination, User, Admin

@pytest.fixture(scope='module')
def test_client():
    app.config.from_object('config_test.Config')
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
        yield testing_client
        with app.app_context():
            db.drop_all()

def test_signup(test_client):
    response = test_client.post('/signup', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data

def test_login_user(test_client):
    test_client.post('/signup', json={
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    response = test_client.post('/loginuser', json={
        'email': 'john.doe@example.com'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'id' in data

def test_login_admin(test_client):
    response = test_client.post('/admin/register', json={
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@example.com',
        'password': 'adminpass'
    })
    assert response.status_code == 201
    response = test_client.post('/admin/login', json={
        'email': 'admin@example.com',
        'password': 'adminpass'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
