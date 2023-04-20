import pytest
from flask_api import status
import json
from ecom_api.models.data_table_models.company.company_login_result import CompanyLoginResultDataModel
from ecom_api.services.company.company_login import CompanyLoginService


def test_successful_login(client, mocker):
    # Mock the comp_login method in CompanyLoginService
    def mock_comp_login(company):
        return CompanyLoginResultDataModel(True, f"Logged in! Welcome :) {company.username}", False, 1)

    mocker.patch.object(CompanyLoginService, 'comp_login', side_effect=mock_comp_login)

    # Test data
    test_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Send a POST request to the login route with the test data
    response = client.post("/company/user/login", json=test_data)

    # Check if the response is successful
    assert response.status_code == 200
    assert json.loads(response.data) == {
        "message": "Logged in! Welcome :) testuser",
        "error": False,
       
    }

def test_invalid_credentials(client, mocker):
    # Mock the comp_login method in CompanyLoginService
    def mock_comp_login(company):
        return CompanyLoginResultDataModel(False, "Invalid Credentials. Please try again.", True, 1)

    mocker.patch.object(CompanyLoginService, 'comp_login', side_effect=mock_comp_login)

    # Test data
    test_data = {
        "username": "wronguser",
        "password": "wrongpassword"
    }

    # Send a POST request to the login route with the test data
    response = client.post("/company/user/login", json=test_data)

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
    response = client.post("/company/user/login", json=test_data)

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
    response = client.post("/company/user/login", json=test_data)

    # Check if the response has a bad request status
    assert response.status_code == 400
    assert json.loads(response.data) == {
        "error": "Invalid username."
    }
    