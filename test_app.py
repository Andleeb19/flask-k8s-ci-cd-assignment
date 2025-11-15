"""
Unit tests for Flask application
Tests the add_numbers function and Flask endpoints
"""
import pytest
from app import app, add_numbers


def test_add_numbers():
    """Test the add_numbers function"""
    assert add_numbers(2, 3) == 5
    assert add_numbers(0, 0) == 0
    assert add_numbers(-1, 1) == 0
    assert add_numbers(10, 20) == 30


def test_add_numbers_negative():
    """Test add_numbers with negative numbers"""
    assert add_numbers(-5, -3) == -8
    assert add_numbers(-10, 5) == -5


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_hello_endpoint(client):
    """Test the main hello endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data
    assert data['status'] == 'running'


def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'


def test_info_endpoint(client):
    """Test the info endpoint"""
    response = client.get('/info')
    assert response.status_code == 200
    data = response.get_json()
    assert 'app_name' in data
    assert 'python_version' in data
