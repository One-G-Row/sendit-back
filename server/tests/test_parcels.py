import pytest
from app import app, db
from models import Parcel, User, Destination
from flask_jwt_extended import create_access_token

def test_create_parcel(test_client, init_database):
    response = test_client.post('/parcels', json={
        'parcel_item': 'Test Parcel',
        'parcel_description': 'This is a test parcel',
        'parcel_weight': 2.0,
        'parcel_cost': 10.0,
        'destination_id': 1
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Parcel created successfully'

def test_get_parcel(test_client, init_database):
    response = test_client.get('/parcels/1')
    assert response.status_code == 200
    assert response.json['parcel_item'] == 'Test Parcel'

def test_update_parcel(test_client, init_database):
    response = test_client.put('/parcels/1', json={'parcel_item': 'Updated Parcel'})
    assert response.status_code == 200
    assert response.json['message'] == 'Parcel updated successfully'

def test_delete_parcel(test_client, init_database):
    response = test_client.delete('/parcels/1')
    assert response.status_code == 200
    assert response.json['message'] == 'Parcel deleted successfully'
