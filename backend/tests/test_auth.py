import json
from datetime import datetime, timedelta

import jwt
import pytest
from app import create_app
from models.user import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'test-secret-key'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create test user
            hashed_password = generate_password_hash('testpassword')
            user = User(username='testuser', email='test@example.com', password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_register_success(client):
    """Test successful user registration"""
    data = {
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'validpassword123'
    }
    response = client.post('/api/auth/register',
                          data=json.dumps(data),
                          content_type='application/json')

    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['username'] == 'newuser'
    assert 'password_hash' not in response.json

def test_register_missing_fields(client):
    """Test registration with missing required fields"""
    data = {'username': 'incomplete'}
    response = client.post('/api/auth/register',
                          data=json.dumps(data),
                          content_type='application/json')

    assert response.status_code == 400
    assert 'error' in response.json

def test_register_duplicate_email(client):
    """Test registration with duplicate email"""
    data = {
        'username': 'duplicate',
        'email': 'test@example.com',  # Already exists from fixture
        'password': 'somepassword'
    }
    response = client.post('/api/auth/register',
                          data=json.dumps(data),
                          content_type='application/json')

    assert response.status_code == 409
    assert 'email' in response.json['error'].lower()

def test_login_success(client):
    """Test successful login"""
    data = {
        'email': 'test@example.com',
        'password': 'testpassword'
    }
    response = client.post('/api/auth/login',
                          data=json.dumps(data),
                          content_type='application/json')

    assert response.status_code == 200
    assert 'token' in response.json
    assert 'expires' in response.json

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    data = {
        'email': 'test@example.com',
        'password': 'wrongpassword'
    }
    response = client.post('/api/auth/login',
                          data=json.dumps(data),
                          content_type='application/json')

    assert response.status_code == 401
    assert 'invalid' in response.json['error'].lower()

def test_login_nonexistent_user(client):
    """Test login with non-existent user"""
    data = {
        'email': 'nonexistent@example.com',
        'password': 'somepassword'
    }
    response = client.post('/api/auth/login',
                          data=json.dumps(data),
                          content_type='application/json')

    assert response.status_code == 401
    assert 'invalid' in response.json['error'].lower()

def test_protected_route_with_valid_token(client):
    """Test accessing protected route with valid token"""
    # First login to get token
    login_data = {
        'email': 'test@example.com',
        'password': 'testpassword'
    }
    login_response = client.post('/api/auth/login',
                                data=json.dumps(login_data),
                                content_type='application/json')
    token = login_response.json['token']

    # Access protected route
    response = client.get('/api/auth/protected',
                         headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    assert 'message' in response.json
    assert 'testuser' in response.json['message']

def test_protected_route_without_token(client):
    """Test accessing protected route without token"""
    response = client.get('/api/auth/protected')

    assert response.status_code == 401
    assert 'missing' in response.json['error'].lower()

def test_protected_route_with_invalid_token(client):
    """Test accessing protected route with invalid token"""
    response = client.get('/api/auth/protected',
                         headers={'Authorization': 'Bearer invalidtoken'})

    assert response.status_code == 401
    assert 'invalid' in response.json['error'].lower()

def test_token_expiration(client):
    """Test that token expires after expiration time"""
    # Create a token that expires immediately
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        expired_token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() - timedelta(seconds=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')

    # Try to use expired token
    response = client.get('/api/auth/protected',
                         headers={'Authorization': f'Bearer {expired_token}'})

    assert response.status_code == 401
    assert 'expired' in response.json['error'].lower()
