# -*- coding: utf-8 -*-
from client.interface.login_server_interface import LoginServerInterface
from server_post_request import ServerPostRequest


class LoginGateway(LoginServerInterface):
    def __init__(self, server_url, client_url):
        LoginServerInterface.__init__(self)

        self.server_url = server_url

        self.server_post_request = ServerPostRequest(server_url, client_url)

    def get_token(self, user):
        """
        Dato l'utente richiama il server_post_request per ricevere il token
        :param user: dizionario uresrname, password
        :return: token or False
        """
        return self.server_post_request.get_token(user)

    def do_login(self, token):
        """
        Dato il token richiama il server_post_request per controllarne la validità
        :param token: string
        :return: True or False
        """
        return self.server_post_request.do_login(token)
