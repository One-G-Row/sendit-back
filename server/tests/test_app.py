import pytest
from flask import json
from config import app, db
from models import User, Admin, Parcel, Destination

@pytest.fixture(scope='module')
def test_client():
    app.config.from_object('config_test.Config')
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
        yield testing_client
        with app.app_context():
            db.drop_all()

def test_home_route(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the SendIT API!' in response.data
