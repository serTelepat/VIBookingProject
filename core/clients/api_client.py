import requests
import os

from dotenv import load_dotenv
from core.settings.environments import Environment

load_dotenv()


class APIClient:
    """ Class for interacting with the API """
    def __init__(self):
        environment_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environment_str]
        except KeyError as e:
            raise ValueError(f'Environment {environment_str} not supported')

        self.base_url = self.get_base_url(environment)
        self.headers = {
            'Content-Type': 'application/json'
        }

    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif environment == Environment.PRODUCTION:
            return os.getenv('PRODUCTION_BASE_URL')
        else:
            raise ValueError(f'Environment {environment} not supported')

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