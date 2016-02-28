from server_post_request import ServerPostRequest
from server_get_request import ServerGetRequest


class ServerRequestHandler:
    def __init__(self, server_url):
        self.server_url = server_url

        self.server_post_request = ServerPostRequest(server_url)

        self.server_get_request = ServerGetRequest(server_url)
