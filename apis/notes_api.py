import requests


class NotesAPI:

    BASE_URL = "https://practice.expandtesting.com/notes/api"

    def get_headers(self, token):

        return {
            "x-auth-token": token
        }

    def create_note(self, token, title, description, category="Home"):

        payload = {
            "title": title,
            "description": description,
            "category": category
        }

        response = requests.post(
            f"{self.BASE_URL}/notes",
            headers=self.get_headers(token),
            json=payload
        )

        return response

    def get_notes(self, token):

        response = requests.get(
            f"{self.BASE_URL}/notes",
            headers=self.get_headers(token)
        )

        return response

    def delete_note(self, token, note_id):

        response = requests.delete(
            f"{self.BASE_URL}/notes/{note_id}",
            headers=self.get_headers(token)
        )

        return response

    def get_note_by_id(self, token, note_id):

        response = requests.get(
            f"{self.BASE_URL}/notes/{note_id}",
            headers=self.get_headers(token)
        )

        return response