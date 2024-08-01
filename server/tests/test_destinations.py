import pytest
from app import app, db
from models import Destination

def test_get_destinations(test_client, init_database):
    response = test_client.get('/destinations')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_create_destination(test_client, init_database):
    response = test_client.post('/destinations', json={
        'name': 'New Destination',
        'location': 'New Location'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Destination created successfully'

def test_update_destination(test_client, init_database):
    response = test_client.put('/destinations/1', json={'name': 'Updated Destination'})
    assert response.status_code == 200
    assert response.json['message'] == 'Destination updated successfully'

def test_delete_destination(test_client, init_database):
    response = test_client.delete('/destinations/1')
    assert response.status_code == 200
    assert response.json['message'] == 'Destination deleted successfully'
