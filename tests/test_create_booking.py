import allure
import pytest

from pydantic import ValidationError
from core.models.booking import BookingResponse


@allure.feature("Test create booking")
@allure.story("Test positive: booking successfully")
def test_create_booking(api_client, generate_random_booking_data):
    response = api_client.create_booking(generate_random_booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

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
        assert (
            response["booking"]["bookingdates"]["checkin"] == generate_random_booking_data["bookingdates"]["checkin"],
            f"The checkin did not match the created data")
        assert (
            response["booking"]["bookingdates"]["checkout"] == generate_random_booking_data["bookingdates"]["checkout"],
            f"The checkout did not match the created data")
        assert (response["booking"]["additionalneeds"] == generate_random_booking_data["additionalneeds"],
                f"The additionalneeds did not match the created data")


@allure.feature("Test create booking")
@allure.story("Negative test: 'additionalneeds' field is missing")
def test_additional_needs_missing(api_client, generate_random_booking_data):
    generate_random_booking_data.pop("additionalneeds")
    response = api_client.create_booking(generate_random_booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

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
        assert (
            response["booking"]["bookingdates"]["checkin"] == generate_random_booking_data["bookingdates"]["checkin"],
            f"The checkin did not match the created data")
        assert (
            response["booking"]["bookingdates"]["checkout"] == generate_random_booking_data["bookingdates"]["checkout"],
            f"The checkout did not match the created data")


@allure.feature("Test create booking")
@allure.story("Negative test: creating the empty booking")
def test_create_empty_booking(api_client):
    with pytest.raises(Exception, match="Internal Server Error"):
        response = api_client.create_booking(dict())
        assert response.status_code == 500, f"Expected status code is 500, but got {response.status_code}"


@allure.feature("Test create booking")
@allure.story("Negative test: incorrect request body")
def test_missed_required_field(api_client, generate_random_booking_data):
    with pytest.raises(Exception, match="Bad Request"):
        response = api_client.create_booking(generate_random_booking_data.pop("firstname"))
        assert response.status_code == 400, f"Expected status code is 400, but got {response.status_code}"


@allure.feature("Test create booking")
@allure.story("Negative test: required field is missing")
def test_missed_required_field(api_client, generate_random_booking_data):
    with pytest.raises(Exception, match="Internal Server Error"):
        generate_random_booking_data.pop("firstname")
        response = api_client.create_booking(generate_random_booking_data)
        assert response.status_code == 500, f"Expected status code is 500, but got {response.status_code}"


@allure.feature("Test create booking")
@allure.story("Negative test: wrong header value")
def test_wrong_header_value(api_client, generate_random_booking_data, set_default_content_type_header):
    api_client.session.headers.update({"Content-Type": "text/xml"})
    with pytest.raises(Exception, match="Bad Request"):
        response = api_client.create_booking(generate_random_booking_data)
        assert response.status_code == 400, f"Expected status code is 400, but got {response.status_code}"


@allure.feature("Test create booking")
@allure.story("Negative test: checkout date is missing")
def test_checkout_date_missing(api_client, generate_booking_data_with_wrong_dates):
    with pytest.raises(Exception, match="Internal Server Error"):
        response = api_client.create_booking(generate_booking_data_with_wrong_dates)
        assert response.status_code == 500, f"Expected status code is 500, but got {response.status_code}"


# Тут баг, но можно исправить со стороны API-клиента (сравнивать даты и отбрасывать 500 код),
# но есть ли в этом смысл, если это уже работа со стороны backend-разраба?
#
# Или сделать через мокирование, если сервер не умеет такое обрабатывать?
@allure.feature("Test create booking")
@allure.story("Negative test: reverse date values")
def test_reverse_dates(api_client, generate_booking_data_with_reverse_dates):
    with pytest.raises(Exception, match="Internal Server Error"):
        response = api_client.create_booking(generate_booking_data_with_reverse_dates)
        assert response.status_code == 500, f"Expected status code is 500, but got {response.status_code}"
