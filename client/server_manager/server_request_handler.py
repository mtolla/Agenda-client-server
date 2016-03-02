from server_post_request import ServerPostRequest
from server_get_request import ServerGetRequest


class ServerRequestHandler:
    def __init__(self, server_url, client_url):
        self.server_url = server_url

        self.client_url = client_url

    def set_token(self, token):
        self.server_post_request = ServerPostRequest(self.server_url, self.client_url, token)

        self.server_get_request = ServerGetRequest(self.server_url, self.client_url, token)

