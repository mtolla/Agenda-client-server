from client.interface.login_server_interface import LoginServerInterface
from server_post_request import ServerPostRequest


class LoginGateway(LoginServerInterface):
    def __init__(self, server_url):
        LoginServerInterface.__init__(self)

        self.server_url = server_url

        self.server_post_request = ServerPostRequest(server_url)

    def get_token(self, user):
        return self.server_post_request.get_token(user)

    def do_login(self):
        pass
