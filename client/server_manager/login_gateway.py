from client.interface.login_server_interface import LoginServerInterface
from server_post_request import ServerPostRequest


class LoginGateway(LoginServerInterface):
    def __init__(self):
        LoginServerInterface.__init__(self)

        self.server_post_request = ServerPostRequest()

    def do_login(self):
        pass
