# -*- coding: utf-8 -*-
from client.interface.server_request_interface import ServerRequestInterface
import requests
import json


class ServerPostRequest(ServerRequestInterface):
    def __init__(self, server_url):
        ServerRequestInterface.__init__(self)

        self.server_url = server_url

        self.request = requests

    def get_token(self, user):
        """
        Dato l'utente:
            Se esiste nel database restituisce il token
            Altrimenti restituisce false
        :param user: dizionario uresrname, password
        :return: token or False
        """
        response = self.request.post(self.server_url + "/get_token", data={'dict_login': json.dumps(user)}).__dict__

        if response['status_code'] == 200 and response['_content'] != 0:
            return response['_content']

        return False

    def do_login(self, token):
        """
        Effettua il login con il token:
            Se esite ritorna True
            Altrimenti False
        :param token: string
        :return: True or False
        """
        response = self.request.post(self.server_url + "/login", data={'token': json.dumps(token)}).__dict__

        if response['status_code'] == 200 and response['_content'] != 0:
            return True

        return False
