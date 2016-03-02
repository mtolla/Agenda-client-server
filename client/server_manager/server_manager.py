# -*- coding: utf-8 -*-
from login_gateway import LoginGateway
from server_request_handler import ServerRequestHandler
from client.local.file_location import *
import json


class ServerManager:
    def __init__(self):
        self.local_save = open(LOCAL_SAVE)
        self.variable = json.load(self.local_save)
        self.local_save.close()

        self.server_url = self.variable['server_url']

        self.client_url = self.variable['client_url']

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
