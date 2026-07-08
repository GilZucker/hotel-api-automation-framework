import allure
import requests

url = "http://localhost:3000/api/hotels"


@allure.title("Verify First Hotel Name in the List")
def test_check_first_hotel_name():
    """Verify that the full hotel list is retrieved and the first hotel name is correct"""

    # Send GET request to retrieve all hotels
    with allure.step("Send GET request to retrieve all hotels"):
        response = requests.get(url)
    hotels_list = response.json()
    print(hotels_list)
    with allure.step("Verify response status is 200 OK"):
        assert response.status_code == 200
    with allure.step("Verify the first hotel name matches 'Motif Seattle'"):
        assert hotels_list[0]['name'] == "Motif Seattle"

    allure.attach(
        response.text, name="Hotels JSON Response", attachment_type=allure.attachment_type.JSON
    )


@allure.title("Create a New Hotel Successfully")
def test_create_new_hotel():
    # Prepare payload for a new hotel creation
    payload = {
        "name": "Gil Luxury Hotel - Exclusive",
        "city": "Rishon LeZion",
        "hotelRating": 5
    }
    with allure.step("Send POST request to create a new hotel"):
        response = requests.post(url, json=payload)
    with allure.step("Verify response status is 201 Created"):
        assert response.status_code == 201, f"Expected 201 but got {response.status_code}"
    with allure.step("Verify the created hotel name is correct"):
        created_hotel = response.json()
    assert created_hotel['name'] == "Gil Luxury Hotel - Exclusive", "The created hotel name doesn't match!"


def test_edit_existing_hotel():
    # Target specific hotel ID for editing
    hotel_id = "dt1Vsk9"
    target_url = f"{url}/{hotel_id}"

    # Prepare update data payload
    update_data = {"hotelRating": 4}

    # Send PUT request to update hotel rating
    response = requests.put(target_url, json=update_data)

    # Verify that the update request succeeded
    assert (
            response.status_code == 200
    ), f"Expected 200 but got {response.status_code}"

    updated_hotel = response.json()
    assert (
        updated_hotel
    ), "There was an issue updating the current hotel rating"


@allure.title("Delete an Existing Hotel and Verify Removal")
def test_delete_existing_hotel():
    # Target specific hotel ID for deletion
    hotel_id = "AhRWkYS"
    target_url = f"{url}/{hotel_id}"

    # Send DELETE request
    with allure.step(f"Send DELETE request for hotel ID: {hotel_id}"):
        response = requests.delete(target_url)

    # Verify successful deletion status code
    with allure.step("Verify server confirmed deletion with 200 OK"):
        assert (
                response.status_code == 200
        ), f"Expected 200 but got {response.status_code}"

    # Ultimate QA check: try to GET the deleted hotel
    with allure.step("Attempt to GET the deleted hotel to confirm removal"):
        get_response = requests.get(target_url)

    # The server must return 404 Not Found if it was truly deleted
    with allure.step("Verify server returns 404 Not Found"):
        assert (
                get_response.status_code == 404
        ), f"Expected 404 Not Found, but hotel still exists (got {get_response.status_code})"


def test_delete_existing_user():
    users_url = "http://localhost:3000/api/users"
    user_id = "user_999"
    target_url = f"{users_url}/{user_id}"

    # Send DELETE request for the user
    response = requests.delete(target_url)
    assert (
            response.status_code == 200
    ), f"Expected 200 but got {response.status_code}"

    # Verify user deletion by attempting a GET request
    get_response = requests.get(target_url)
    assert (
            get_response.status_code == 404
    ), f"Expected 404, the user does not exist on the list, (got {get_response.status_code})"


def test_create_hotel_with_invalid_stars():
    # Send invalid data payload to verify server validation
    invalid_data = {"name": "Super Luxury Hotel", "stars": 10}
    response = requests.post(url, json=invalid_data)

    assert (
            response.status_code == 400
    ), f"Expected 400 (Bad Request) but got {response.status_code}"


def test_update_existing_hotel():
    hotel_id = "hotel_1"
    update_data = {"name": "Updated Hotel Name", "hotelRating": 4}
    target_url = f"{url}/{hotel_id}"

    # Send PUT request to update existing hotel data
    response = requests.put(target_url, json=update_data)
    assert (
            response.status_code == 200
    ), f"Expected 200, but got {response.status_code}"
