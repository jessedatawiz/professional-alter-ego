import requests


class PushoverClient:

    URL = "https://api.pushover.net/1/messages.json"

    def __init__(self, token, user):
        self.token = token
        self.user = user

    def send(self, message):
        requests.post(
            self.URL,
            data={"token": self.token, "user": self.user, "message": message},
        )
