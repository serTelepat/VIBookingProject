import requests
import os
import allure

from dotenv import load_dotenv

from core.settings.config import Users, Timeouts
from core.settings.environments import Environment
from core.clients.endpoints import Endpoints

load_dotenv()


class APIClient:
    """ Class for interacting with the API """
    def __init__(self):
        environment_str = os.getenv("ENVIRONMENT")
        try:
            environment = Environment[environment_str]
        except KeyError as e:
            raise ValueError(f"Environment {environment_str} not supported")

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()
        self.session.headers = {
            'Content-Type': 'application/json'
        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv("TEST_BASE_URL")
        elif environment == Environment.PRODUCTION:
            return os.getenv("PRODUCTION_BASE_URL")
        else:
            raise ValueError(f"Environment {environment} not supported")

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, params=params, headers=self.headers)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data_json=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data_json)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def ping(self):
        with allure.step("Ping api client"):
            url = f"{self.base_url}{Endpoints.PING_ENDPOINT}"
            response = self.session.get(url)
            response.raise_for_status()

        with allure.step("Checking status code"):
            assert response.status_code == 201, f"Expected status code is 201, but got {response.status_code}"
        return response.status_code

    def auth(self):
        with allure.step("Getting authenticate"):
            url = f"{self.base_url}{Endpoints.AUTH_ENDPOINT}"
            body_request = {"username": Users.USERNAME, "password": Users.PASSWORD}
            response = self.session.post(url, json=body_request, timeout=Timeouts.TIMEOUT)
            response.raise_for_status()

        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code is 200, but got {response.status_code}"

        token = response.json()["token"]
        with allure.step("Updating headers with authorization"):
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def get_booking_by_id(self, id: int):
        with allure.step("Getting booking by ID"):
            url = f"{self.base_url}{Endpoints.BOOKING_ENDPOINT}/{id}"
            response = self.session.get(url=url)
            response.raise_for_status()

        with allure.step("Checking status code"):
            assert response.status_code == 200, f"Expected status code is 200, but got {response.status_code}"
        return response.json()