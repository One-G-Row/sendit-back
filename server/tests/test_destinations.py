import pytest
from flask import json
from config import app, db
from models import Destination
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='module')
def test_client():
    app.config.from_object('config_test.Config')
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
        yield testing_client
        with app.app_context():
            db.drop_all()

@pytest.fixture(scope='module')
def auth_header(test_client):
    access_token = create_access_token(identity=1)  # Mock user ID
    return {'Authorization': f'Bearer {access_token}'}

def test_create_destination(test_client, auth_header):
    response = test_client.post('/destinations', json={
        'name': 'New York',
        'location': 'USA'
    }, headers=auth_header)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Destination created successfully'
