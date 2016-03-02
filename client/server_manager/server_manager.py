# -*- coding: utf-8 -*-
from login_gateway import LoginGateway
from server_request_handler import ServerRequestHandler


class ServerManager:
    def __init__(self):
        self.server_url = "http://127.0.0.1:5000"

        self.client_url = "127.0.0.1:5001"

        self.login_gateway = LoginGateway(self.server_url, self.client_url)

        self.server_request_handler = ServerRequestHandler(self.server_url, self.client_url)

    def get_token(self, user):
        """
        Dato l'utente richiama il login_gateway per ricevere il token
        :param user: dizionario uresrname, password
        :return: token or False
        """
        return self.login_gateway.get_token(user)

    def do_login(self, token):
        """
        Dato il token richiama il login_gateway per controllarne la validità
        :param token: string
        :return: True or False
        """
        self.server_request_handler.set_token(token)

        return self.login_gateway.do_login(token)
