from client.interface.server_request_interface import ServerRequestInterface


class ServerGetRequest(ServerRequestInterface):
    def __init__(self, server_url):
        ServerRequestInterface.__init__(self)

        self.server_url = server_url
