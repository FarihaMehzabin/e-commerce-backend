import pytest
import json
from ecom_api.services.public_user.user_signup import UserSignupService
from ecom_api.models.data_table_models.public_user.user_signup_result import UserSignupResultDataModel
from flask_api import status


def test_signup_route(client, mocker):
    def mock_user_signup(user):
        return UserSignupResultDataModel(
            user_created=True,
            message="New user signed up! Welcome :)",
            error=False,
            user_id="1"
        )

    mocker.patch.object(UserSignupService, 'user_signup', side_effect=mock_user_signup)


    # Send a POST request to the signup route with JSON data.
    response = client.post(
        "/user-signup",
        json={
            "first_name": "test_name",
            "last_name": "test_name",
            "username": "test_user",
            "password": "secret_password",
        },
    )

    # Check if the response status code is 200 (OK).
    if response.status_code != status.HTTP_200_OK:
        pytest.fail("No response found", pytrace=False)

    # Check if the response JSON data matches the expected data.
    expected_data = {
        "message": "New user signed up! Welcome :)",
        "error": False,
        "user_id": "1",
    }
    
    if json.loads(response.data) != expected_data:
        pytest.fail("Response data doesn't match", pytrace=False)
        
        
def test_signup_route_invalid_input_data(client):
    # Send a POST request to the signup route with invalid/incomplete input data.
    response = client.post(
        "/user-signup",
        json={
            "first_name": "test_name",
            "last_name": "test_name",
            "username": "test_user",
            # "password" field is missing
        },
    )

    # Check if the response status code is 500 (Internal Server Error).
    assert response.status_code == status.HTTP_400_BAD_REQUEST, "Invalid input data was not handled properly"

    # Verify that the response contains the appropriate error message.
    response_data = json.loads(response.data)
    
    print(response.get_data(as_text=True))
    
    expected_error_messages = [
    "Invalid first name.",
    "Invalid last name.",
    "Invalid password. Password must be at least 8 characters.",
    "Invalid user name.",
]

    assert "error" in response_data, "No error field found in the response data"

    assert response_data["error"] in expected_error_messages, "Error message does not match any of the expected values"
    
    
def test_signup_route_empty_request_body(client):
    # Send a POST request to the signup route with an empty request body.
    response = client.post("/user-signup", json={}, content_type="application/json")

    # Check if the response status code is 400 (Bad Request).
    assert response.status_code == status.HTTP_400_BAD_REQUEST, "Empty request body was not handled properly"

    # Verify that the response contains the appropriate error message.
    response_data = json.loads(response.data)
    expected_error_message = "Request body is empty or not in JSON format."

    assert "error" in response_data, "No error field found in the response data"
    assert response_data["error"] == expected_error_message, "Error message does not match the expected value"


