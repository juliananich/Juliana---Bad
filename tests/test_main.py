import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_valid_discount(client):
    """Test a normal 10% discount on a 100.00 item."""
    rv = client.get('/calculate_total?price=100&discount=10')
    assert rv.status_code == 200
    assert rv.get_json() == {"final_price": 90.0}

def test_negative_discount(client):
    """Test that negative discounts are properly rejected."""
    rv = client.get('/calculate_total?price=100&discount=-20')
    assert rv.status_code == 400

def test_excessive_discount_bug(client):
    """
    Test that a discount over 100% is rejected. 
    EXPECTED TO FAIL because the validation logic in main.py is flawed.
    """
    rv = client.get('/calculate_total?price=100&discount=150')
    # We expect the API to return a 400 Bad Request error.
    # The buggy app will return 200 OK and a price of -50.0.
    assert rv.status_code == 400
    