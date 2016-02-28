from client.interface.server_request_interface import ServerRequestInterface
import requests
import json


class ServerPostRequest(ServerRequestInterface):
    def __init__(self, server_url):
        ServerRequestInterface.__init__(self)

        self.server_url = server_url

        self.request = requests

    def get_token(self, user):
        # 127.0.0.1:5000/get_token
        return self.request.post(self.server_url + "/get_token", data={'action': "get_token", 'dict_login': json.dumps(user)})
        # return self.request.post(self.server_url, data={'action': "get_token", 'dict_login': user})

    def do_login(self):
        pass
