"""Integration tests for AfriBnB API"""
import pytest
import json
from app import app, db, User, Place, Review, Amenity


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


def test_health_check(client):
    """Test health endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'


def test_register_user(client):
    """Test user registration"""
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'first_name': 'John',
        'last_name': 'Doe'
    })
    
    assert response.status_code == 201
    assert response.json['user']['email'] == 'test@example.com'
    assert 'access_token' in response.json


def test_register_duplicate_email(client):
    """Test duplicate email registration"""
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password456'
    })
    
    assert response.status_code == 409


def test_login_user(client):
    """Test user login"""
    # Register first
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    # Login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_login_invalid_password(client):
    """Test login with invalid password"""
    client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401


def test_create_place(client):
    """Test creating a place"""
    # Register and login
    register_response = client.post('/api/auth/register', json={
        'email': 'owner@example.com',
        'password': 'password123'
    })
    token = register_response.json['access_token']
    
    # Create place
    response = client.post('/api/places', json={
        'name': 'Beautiful Apartment',
        'description': 'Cozy apartment in the city',
        'address': '123 Main St',
        'city': 'New York',
        'country': 'USA',
        'price_per_night': 150.0,
        'rooms': 2,
        'bathrooms': 1,
        'max_guests': 4
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 201
    assert response.json['place']['name'] == 'Beautiful Apartment'
    assert response.json['place']['price_per_night'] == 150.0


def test_get_places(client):
    """Test getting all places"""
    response = client.get('/api/places')
    
    assert response.status_code == 200
    assert 'places' in response.json
    assert 'total' in response.json


def test_create_review(client):
    """Test creating a review"""
    # Create users
    owner_response = client.post('/api/auth/register', json={
        'email': 'owner@example.com',
        'password': 'password123'
    })
    owner_token = owner_response.json['access_token']
    
    reviewer_response = client.post('/api/auth/register', json={
        'email': 'reviewer@example.com',
        'password': 'password123'
    })
    reviewer_token = reviewer_response.json['access_token']
    
    # Create place
    place_response = client.post('/api/places', json={
        'name': 'Test Place',
        'price_per_night': 100.0
    }, headers={
        'Authorization': f'Bearer {owner_token}'
    })
    place_id = place_response.json['place']['id']
    
    # Create review
    response = client.post(f'/api/places/{place_id}/reviews', json={
        'rating': 5,
        'comment': 'Great place! Highly recommended.'
    }, headers={
        'Authorization': f'Bearer {reviewer_token}'
    })
    
    assert response.status_code == 201
    assert response.json['review']['rating'] == 5


def test_get_place_reviews(client):
    """Test getting reviews for a place"""
    # Setup
    owner_response = client.post('/api/auth/register', json={
        'email': 'owner@example.com',
        'password': 'password123'
    })
    owner_token = owner_response.json['access_token']
    
    place_response = client.post('/api/places', json={
        'name': 'Test Place',
        'price_per_night': 100.0
    }, headers={
        'Authorization': f'Bearer {owner_token}'
    })
    place_id = place_response.json['place']['id']
    
    # Get reviews
    response = client.get(f'/api/places/{place_id}/reviews')
    
    assert response.status_code == 200
    assert 'reviews' in response.json


def test_update_place(client):
    """Test updating a place"""
    # Register and create place
    register_response = client.post('/api/auth/register', json={
        'email': 'owner@example.com',
        'password': 'password123'
    })
    token = register_response.json['access_token']
    
    place_response = client.post('/api/places', json={
        'name': 'Original Name',
        'price_per_night': 100.0
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    place_id = place_response.json['place']['id']
    
    # Update place
    response = client.put(f'/api/places/{place_id}', json={
        'name': 'Updated Name',
        'price_per_night': 150.0
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200
    assert response.json['place']['name'] == 'Updated Name'
    assert response.json['place']['price_per_night'] == 150.0


def test_delete_place(client):
    """Test deleting a place"""
    # Register and create place
    register_response = client.post('/api/auth/register', json={
        'email': 'owner@example.com',
        'password': 'password123'
    })
    token = register_response.json['access_token']
    
    place_response = client.post('/api/places', json={
        'name': 'Test Place',
        'price_per_night': 100.0
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    place_id = place_response.json['place']['id']
    
    # Delete place
    response = client.delete(f'/api/places/{place_id}', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200
    
    # Verify deletion
    verify_response = client.get(f'/api/places/{place_id}')
    assert verify_response.status_code == 404


def test_amenities(client):
    """Test amenity CRUD"""
    register_response = client.post('/api/auth/register', json={
        'email': 'admin@example.com',
        'password': 'password123'
    })
    token = register_response.json['access_token']
    
    # Create amenity
    response = client.post('/api/amenities', json={
        'name': 'WiFi'
    }, headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 201
    
    # Get amenities
    response = client.get('/api/amenities')
    assert response.status_code == 200
    assert response.json['count'] >= 1


def test_unauthorized_access(client):
    """Test unauthorized place update"""
    # User 1 creates place
    user1_response = client.post('/api/auth/register', json={
        'email': 'user1@example.com',
        'password': 'password123'
    })
    user1_token = user1_response.json['access_token']
    
    place_response = client.post('/api/places', json={
        'name': 'User 1 Place',
        'price_per_night': 100.0
    }, headers={
        'Authorization': f'Bearer {user1_token}'
    })
    place_id = place_response.json['place']['id']
    
    # User 2 tries to update user 1's place
    user2_response = client.post('/api/auth/register', json={
        'email': 'user2@example.com',
        'password': 'password123'
    })
    user2_token = user2_response.json['access_token']
    
    response = client.put(f'/api/places/{place_id}', json={
        'name': 'Hacked Name'
    }, headers={
        'Authorization': f'Bearer {user2_token}'
    })
    
    assert response.status_code == 403


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
