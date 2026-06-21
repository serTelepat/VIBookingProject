import allure
import pytest
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
@allure.story("Test creating the empty booking")
def test_create_empty_booking(api_client, generate_random_booking_data):
    with pytest.raises(Exception, match="Internal Server Error"):
        response = api_client.create_booking(dict())
        assert response.status_code == 500, f"Expected status code is 500, but got {response.status_code}"


@allure.feature("Test create booking")
@allure.story("Test required field is missing")
def test_missed_required_field(api_client, generate_random_booking_data):
    with pytest.raises(Exception, match="Bad Request"):
        response = api_client.create_booking(generate_random_booking_data.pop("firstname"))
        assert response.status_code == 400, f"Expected status code is 400, but got {response.status_code}"


@allure.feature("Test create booking")
@allure.story("Test wrong header value")
def test_wrong_header_value(api_client, generate_random_booking_data):
    api_client.session.headers.update({"Content-Type": "text/xml"})
    with pytest.raises(Exception, match="Bad Request"):
        response = api_client.create_booking(generate_random_booking_data)
        assert response.status_code == 400, f"Expected status code is 400, but got {response.status_code}"


