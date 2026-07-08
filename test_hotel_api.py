import allure
import requests


@allure.title("Verify Hotel API Status Code and Response Structure")
def test_get_hotel_status_code(base_url):
    # Send GET request to the server
    with allure.step("Send GET request to retrieve all bookings"):
        response = requests.get(base_url)

    # Verify response status code is 200 OK
    with allure.step("Verify response status code is 200 OK"):
        assert (
                response.status_code == 200
        ), f"Expected status 200 but got {response.status_code}"

    # Parse response content to JSON format
    with allure.step("Parse response and verify it is a non-empty list"):
        data = response.json()

    # Verify that the response is a non-empty list
    assert isinstance(data, list), "Expected response to be a list of bookings"
    assert len(data) > 0, "Expected booking list to have at least one item"

    allure.attach(
        response.text,
        name="Bookings List Response",
        attachment_type=allure.attachment_type.JSON,
    )


@allure.title("Verify Specific Booking Data Fields")
def test_get_specific_booking_data(base_url):
    # Send GET request for a specific booking ID
    another_specific_url = base_url + "/10"
    with allure.step("Send GET request for booking ID 10"):
        response = requests.get(another_specific_url)

    assert response.status_code == 200

    # Parse response to a dictionary
    with allure.step("Verify essential fields exist in the response dictionary"):
        booking_detail = response.json()

    # Verify that essential fields exist in the response
    assert "firstname" in booking_detail, "Missing 'firstname' field"
    assert "lastname" in booking_detail, "Missing 'lastname' field"
    assert "totalprice" in booking_detail, "Missing 'totalprice' field"

    allure.attach(
        response.text,
        name="Booking 10 Detail Response",
        attachment_type=allure.attachment_type.JSON,
    )


@allure.title("Verify Data Types of Booking Fields")
def test_booking_data_types(base_url):
    specific_url = base_url + "/10"
    with allure.step("Send GET request for booking ID 10"):
        response = requests.get(specific_url)

    assert response.status_code == 200
    with allure.step("Verify fields data types (firstname=str, totalprice=int)"):
        data_types = response.json()

    # Verify data types of specific fields
    assert isinstance(data_types["firstname"], str), "The data type: 'firstname' is not a string"
    assert isinstance(data_types["totalprice"], int), "The data type: 'totalprice' is not an integer"


@allure.title("Create a New Booking with Custom Data (Gil)")
def test_create_booking_post(base_url, default_booking_data):
    # Prepare payload with custom data
    gil_booking_data = default_booking_data
    gil_booking_data["firstname"] = "Gil"
    gil_booking_data["lastname"] = "Zucker"
    gil_booking_data["totalprice"] = 250
    gil_booking_data["depositpaid"] = True
    gil_booking_data["bookingdates"] = {"checkin": "2026-08-20", "checkout": "2026-08-30"}
    gil_booking_data["additionalneeds"] = "Breakfast"

    # Send POST request to create a new booking
    with allure.step("Send POST request to create booking for Gil"):
        response = requests.post(base_url, json=gil_booking_data)

    assert (
            response.status_code == 200
    ), f"Expected 200 but got {response.status_code}"

    with allure.step("Verify booking creation accuracy and generated ID"):
        response_data = response.json()

    # Verify booking creation and response data accuracy
    assert "bookingid" in response_data, "Server did not return a 'bookingid'"

    assert (
            response_data["booking"]["firstname"] == "Gil"
    ), "The firstname in response does not match"

    assert response_data["booking"]["lastname"] == "Zucker", "The lastname in response does not match"
    assert response_data["booking"]["totalprice"] == 250, "The totalprice in response does not match"
    allure.attach(
        response.text,
        name="Created Booking Response",
        attachment_type=allure.attachment_type.JSON,
    )


@allure.title("Create a New Booking with Custom Data (Mika)")
def test_create_mika_booking(base_url, default_booking_data):
    # Prepare payload for Mika's booking
    mika_booking_data = default_booking_data
    mika_booking_data["firstname"] = "Mika"
    mika_booking_data["lastname"] = "Zucker"
    mika_booking_data["totalprice"] = 150
    mika_booking_data["additionalneeds"] = "Ice Cream"

    # Send POST request
    with allure.step("Send POST request to create booking for Mika"):
        response = requests.post(base_url, json=mika_booking_data)

    assert (
            response.status_code == 200
    ), f"Expected 200 but got {response.status_code}"

    with allure.step("Verify Mika's firstname in response"):
        response_data = response.json()

    assert (
            response_data["booking"]["firstname"] == "Mika"
    ), "The firstname in response does not match"


@allure.title("Filter Bookings Dynamically by Firstname")
def test_filter_booking_by_name(base_url, default_booking_data):
    # Define query parameters for filtering
    query_params = {"firstname": "Gil"}

    # Send GET request with query parameter
    with allure.step("Send GET request with firstname filter query parameters"):
        response = requests.get(base_url, params=query_params)

    assert response.status_code == 200

    # Parse filtered data list
    with allure.step("Verify filtered result is a valid non-empty list"):
        filtered_data = response.json()

    print("\nFiltered bookings for Gil:", filtered_data)

    # Verify that the response is a valid, non-empty list
    assert isinstance(filtered_data, list)

    assert len(filtered_data) > 0, "Filtered bookings for Gil not found"

    allure.attach(
        response.text,
        name="Filtered Bookings Response",
        attachment_type=allure.attachment_type.JSON,
    )


@allure.title("Update Existing Booking Using Auth Token")
def test_update_booking_with_auth(base_url, default_booking_data, auth_token):
    # Target booking ID 10 for update
    target_url = base_url + "/10"

    # Prepare updated data payload
    updated_data = default_booking_data
    updated_data["firstname"] = "VIP_Guest"

    # Set authentication token in cookies
    request_cookies = {"token": auth_token}

    with allure.step("Send PUT request with update payload and auth cookies"):
        response = requests.put(target_url, json=updated_data, cookies=request_cookies)

        # Send PUT request with both payload and authentication cookies
        response = requests.put(
            target_url, json=updated_data, cookies=request_cookies
        )

    # Verify that the update request was authorized and succeeded
    with allure.step("Verify authorization succeeded and server returned 200 OK"):
        assert (
                response.status_code == 200
        ), f"Auth failed! Server returned {response.status_code}"

    # Verify that the field was updated successfully on the server
    with allure.step("Verify firstname field was successfully updated to 'VIP_Guest'"):
        response_data = response.json()
    assert response_data["firstname"] == "VIP_Guest"


@allure.title("Delete Booking Using Auth Token")
def test_delete_booking_with_auth(base_url, auth_token):
    # Target booking ID 11 for deletion
    target_url = base_url + "/11"

    # Set the security token in the cookies
    request_cookies = {"token": auth_token}

    # Send the DELETE request
    with allure.step("Send DELETE request with auth cookies"):
        response = requests.delete(target_url, cookies=request_cookies)

    # Verify deletion success (the server returns 201 Created)
    with allure.step("Verify deletion success (Server returns 201 Created)"):
        assert response.status_code == 201, f"Expected 201 but got {response.status_code}"
    print(f"\nBooking 11 deleted successfully. Status: {response.status_code}")


@allure.title("Negative Test: Block Unauthorized Booking Update")
def test_update_booking_without_auth_should_fail(base_url, default_booking_data):
    target_url = base_url + "/10"

    # Prepare updated data payload
    hacker_data = default_booking_data
    hacker_data["firstname"] = "Hacker"

    # Send PUT request without providing the auth cookies
    with allure.step("Send PUT request WITHOUT auth cookies"):
        response = requests.put(target_url, json=hacker_data)

    # Verify that the server blocks the request with 403 Forbidden
    with allure.step("Verify server securely blocks request with 403 Forbidden"):
        assert response.status_code == 403, f"Security breach! Expected 403 but got {response.status_code}"
    print(f"\nSecurity check passed. Server blocked unauthorized PUT with status: {response.status_code}")
