import requests


class AuthAPI:

    def __init__(self):

        self.base_url = "https://practice.expandtesting.com/notes/api"

    def login(self, email, password):

        payload = {
            "email": email,
            "password": password
        }

        response = requests.post(
            f"{self.base_url}/users/login",
            json=payload
        )

        return response

    def get_token(self, email, password):

        response = self.login(
            email,
            password
        )

        response_json = response.json()

        token = response_json.get("data", {}).get("token")

        return token