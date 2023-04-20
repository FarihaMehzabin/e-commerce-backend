import pytest
from flask_api import status
import json
from ecom_api.models.data_table_models.public_user.user_login_result import UserLoginResultDataModel
from ecom_api.services.public_user.user_login import UserLoginService


def test_successful_login(client, mocker):
    # Mock the comp_login method in CompanyLoginService
    def mock_user_login(user):
        return UserLoginResultDataModel(True, f"Logged in! Welcome :) {user.username}", False, 1)

    mocker.patch.object(UserLoginService, 'user_login', side_effect=mock_user_login)

    # Test data
    test_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Send a POST request to the login route with the test data
    response = client.post("/user-login", json=test_data)

    # Check if the response is successful
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "message": "Logged in! Welcome :) testuser",
        "error": False,
        
    }

def test_invalid_credentials(client, mocker):
    # Mock the comp_login method in CompanyLoginService
    def mock_user_login(user):
        return UserLoginResultDataModel(False, "Invalid Credentials. Please try again.", True, 1)

    mocker.patch.object(UserLoginService, 'user_login', side_effect=mock_user_login)

    # Test data
    test_data = {
        "username": "wronguser",
        "password": "wrongpassword"
    }

    # Send a POST request to the login route with the test data
    response = client.post("/user-login", json=test_data)

    # Check if the response has an error message
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "message": "Invalid Credentials. Please try again.",
        "error": True,
        
    }

def test_invalid_request_data(client):
    # Test data
    test_data = {
        "username": "t",
        "password": "short"
    }

    # Send a POST request to the login route with the test data
    response = client.post("/user-login", json=test_data)

    # Check if the response has a bad request status
    assert response.status_code == 400
    assert json.loads(response.data) == {
        "error": "Invalid username."
    }
    
def test_incorrect_data_type(client):
    # Test data
    test_data = {
        "username": 123,
        "password": ["not", "a", "string"]
    }

    # Send a POST request to the login route with the test data
    response = client.post("/user-login", json=test_data)

    # Check if the response has a bad request status
    assert response.status_code == 400
    assert json.loads(response.data) == {
        "error": "Invalid username."
    }
    
    