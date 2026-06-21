import pytest

from datetime import datetime, timedelta
from faker import Faker

from core.clients.api_client import APIClient


@pytest.fixture(scope="session")
def api_client():
    client = APIClient()
    client.auth()
    return client


@pytest.fixture(scope="function")
def booking_dates():
    today = datetime.today()
    checkin_date = today + timedelta(days=10)
    checkout_date = checkin_date + timedelta(days=5)

    return {
        "checkin": checkin_date.strftime("%Y-%m-%d"),
        "checkout": checkout_date.strftime("%Y-%m-%d")
    }


@pytest.fixture(scope="function")
def generate_random_booking_data(booking_dates: dict):
    faker = Faker()
    firstname = faker.first_name()
    lastname = faker.last_name()
    totalprice = faker.random_number(digits=3)
    depositpaid = faker.boolean()
    additionalneeds = faker.sentence()

    data = {
        "firstname": firstname,
        "lastname": lastname,
        "totalprice": totalprice,
        "depositpaid": depositpaid,
        "bookingdates": booking_dates,
        "additionalneeds": additionalneeds
    }

    return data


@pytest.fixture(scope="function")
def reverse_booking_dates(booking_dates):
    booking_dates["checkin"], booking_dates["checkout"] = booking_dates["checkout"], booking_dates["checkin"]
    return booking_dates


@pytest.fixture(scope="function")
def generate_booking_data_with_reverse_dates(generate_random_booking_data: dict, reverse_booking_dates: dict):
    generate_random_booking_data.update({"bookingdates":  reverse_booking_dates})
    return generate_random_booking_data


@pytest.fixture(scope="function")
def delete_checkout_date(booking_dates: dict):
    booking_dates.pop("checkout")
    return booking_dates


@pytest.fixture(scope="function")
def generate_booking_data_with_wrong_dates(generate_random_booking_data: dict, delete_checkout_date: dict):
    generate_random_booking_data.update({"bookingdates":  delete_checkout_date})
    return generate_random_booking_data


@pytest.fixture(scope="function")
def set_default_content_type_header(api_client):
    yield
    api_client.session.headers["Content-Type"] = "application/json"