import pytest
from app import app, db
from models import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_get_user(client):
    # Setup: create a test user
    user = User(email='test@example.com', password='password', first_name='Test', last_name='User')
    db.session.add(user)
    db.session.commit()
    
    # Test: retrieve the user
    response = client.get(f'/users/{user.id}')
    assert response.status_code == 200
    assert response.json['email'] == 'test@example.com'

def test_create_user(client):
    # Test: create a new user with all required fields
    response = client.post('/users', json={
        'email': 'newuser@example.com',
        'password': 'password',
        'first_name': 'New',
        'last_name': 'User'
    })
    assert response.status_code == 201
    assert response.json['email'] == 'newuser@example.com'
