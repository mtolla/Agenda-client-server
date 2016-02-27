from server_post_request import ServerPostRequest
from server_get_request import ServerGetRequest


class ServerRequestHandler:
    def __init__(self):
        self.server_post_request = ServerPostRequest()

        self.server_get_request = ServerGetRequest()
