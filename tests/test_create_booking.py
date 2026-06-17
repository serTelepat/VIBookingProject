import allure
import pytest
import requests
import jsonschema

from schemas.booking_schema import BOOKING_SCHEMA


# Не уверен, что код правильный, хотелось бы понять когда использовать Exception, а когда AssertionError при патче в мокировании
# Нейронка говорит, что .raise_for_status() отлавливает ошибки 4XX - 5XX
@allure.feature("Test create booking")
@allure.story("Test booking successfully")
def test_create_booking(api_client, generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data)
    with allure.step("Data validation against a JSON schema"):
        jsonschema.validate(response, BOOKING_SCHEMA)

    with allure.step("Check booking data"):
        assert isinstance(response["bookingid"], int), f"No booking ID has been created"

        assert (response["booking"]["firstname"] == generate_random_booking_data["firstname"],
                f"The firstname did not match the created data")
        assert (response["booking"]["lastname"] == generate_random_booking_data["lastname"],
                f"The lastname did not match the created data")
        assert (response["booking"]["totalprice"] == generate_random_booking_data["totalprice"],
                f"The totalprice did not match the created data")
        assert (response["booking"]["depositpaid"] == generate_random_booking_data["depositpaid"],
                f"The depositpaid did not match the created data")
        assert (response["booking"]["bookingdates"]["checkin"] == generate_random_booking_data["bookingdates"]["checkin"],
                f"The checkin did not match the created data")
        assert (response["booking"]["bookingdates"]["checkout"] == generate_random_booking_data["bookingdates"]["checkout"],
                f"The checkout did not match the created data")
        assert (response["booking"]["additionalneeds"] == generate_random_booking_data["additionalneeds"],
                f"The additionalneeds did not match the created data")


@allure.feature("Test create booking")
@allure.story("Test server unavailability")
def test_create_booking_server_unavailability(api_client, generate_random_booking_data, mocker):
    mocker.patch.object(api_client.session, "post", side_effect=Exception("Server unavailable"))
    with pytest.raises(Exception, match="Server unavailable"):
        api_client.create_booking(generate_random_booking_data)


@allure.feature("Test create booking")
@allure.story("Test server error")
def test_create_booking_server_error(api_client, generate_random_booking_data, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, "post",
                        side_effect=Exception("Expected status code is 200, but got 500"),
                        return_value=mock_response)

    with pytest.raises(Exception, match="Expected status code is 200, but got 500"):
        api_client.create_booking(generate_random_booking_data)


@allure.feature("Test create booking")
@allure.story("Test missing header")
def test_create_booking_missing_header(api_client, generate_random_booking_data, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 418
    mocker.patch.object(api_client.session, "post",
                        side_effect=Exception("I'm a Teapot"),
                        return_value=mock_response)

    with pytest.raises(Exception, match="I'm a Teapot"):
        api_client.create_booking(generate_random_booking_data)


@allure.feature("Test create booking")
@allure.story("Test wrong URL")
def test_create_booking_not_found(api_client, generate_random_booking_data, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, "post",
                        side_effect=Exception("Expected status code is 200, but got 404"),
                        return_value=mock_response)

    with pytest.raises(Exception, match="Expected status code is 200, but got 404"):
        api_client.create_booking(generate_random_booking_data)


@allure.feature("Test create booking")
@allure.story("Test forbidden")
def test_create_booking_forbidden(api_client, generate_random_booking_data, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 403
    mocker.patch.object(api_client.session, "post",
                        side_effect=Exception("Expected status code is 200, but got 403"),
                        return_value=mock_response)

    with pytest.raises(Exception, match="Expected status code is 200, but got 403"):
        api_client.create_booking(generate_random_booking_data)


@allure.feature("Test create booking")
@allure.story("Test timeout")
def test_create_booking_not_found(api_client, generate_random_booking_data, mocker):
    mocker.patch.object(api_client.session, "post", side_effect=requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.create_booking(generate_random_booking_data)