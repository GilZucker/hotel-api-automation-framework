import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    # Return the base URL for the hotel booking API
    return "https://restful-booker.herokuapp.com/booking"


@pytest.fixture
def default_booking_data():
    # Provide a reusable baseline payload template for booking creation/updates
    return {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-08-20", "checkout": "2026-08-30"},
        "additionalneeds": "Breakfast",
    }


@pytest.fixture(scope="session")
def auth_token():
    # Define the authentication endpoint URL
    auth_url = "https://restful-booker.herokuapp.com/auth"

    # Set up the credentials required by the server
    credentials = {"username": "admin", "password": "password123"}

    # Send POST request to authenticate and generate the token
    response = requests.post(auth_url, json=credentials)

    # Extract the token from the JSON response data
    token_data = response.json()

    # Return only the token string value (e.g., "7b9e1a2c3d4e5f6g")
    return token_data["token"]