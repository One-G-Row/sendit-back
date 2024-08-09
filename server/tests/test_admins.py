import pytest
from server.app import app, db, bcrypt
from models import Admin, Parcel,User, Destination
from flask_jwt_extended import create_access_token

def test_admin_register(test_client, init_database):
    response = test_client.post('/admin/register', json={
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@example.com',
        'password': 'adminpassword'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Admin created successfully'

def test_admin_login(test_client, init_database):
    test_client.post('/admin/register', json={
        'first_name': 'Admin',
        'last_name': 'User',
        'email': 'admin@example.com',
        'password': 'adminpassword'
    })
    response = test_client.post('/admin/login', json={
        'email': 'admin@example.com',
        'password': 'adminpassword'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
