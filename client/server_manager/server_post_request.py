# -*- coding: utf-8 -*-
from client.interface.server_request_interface import ServerRequestInterface
import requests
import json


class ServerPostRequest(ServerRequestInterface):
    def __init__(self, server_url, client_url, token=None):
        ServerRequestInterface.__init__(self)

        self.client_url = client_url

        self.token = token

        self.request = requests

        self.request_url = {
            'get_token': server_url + "/login/token",
            'do_login': server_url + "/login",
            'insert_activity': server_url + "/insert/activity",
            'insert_holiday': server_url + "/insert/holiday"
        }

    @staticmethod
    def get_response(response):
        if response['status_code'] == 200:
            return response['_content']

        return False

    def get_token(self, user):
        """
        Dato l'utente:
            Se esiste nel database restituisce il token
            Altrimenti restituisce false
        :param user: dizionario uresrname, password
        :return: token or False
        """
        response = self.request.post(
            self.request_url['get_token'],
            data={
                'dict_login': json.dumps(user),
                'ip': self.client_url
            }
        ).__dict__

        return self.get_response(response)

    def do_login(self, token):
        """
        Effettua il login con il token:
            Se esite ritorna True
            Altrimenti False
        :param token: string
        :return: True or False
        """
        response = self.request.post(
            self.request_url['do_login'],
            data={
                'token': token,
                'ip': self.client_url
            }
        ).__dict__

        return self.get_response(response)

    def insert_activity(self, activity):
        dict_activity = dict()
        dict_activity['token'] = self.token
        dict_activity['ip'] = self.client_url
        dict_activity['activity'] = activity

        response = self.request.post(
            self.request_url['insert_activity'],
            data={
                'dict_activity': json.dumps(dict_activity)
            }
        ).__dict__

        return self.get_response(response)

    def insert_holiday(self, holiday):
        dict_holiday = dict()
        dict_holiday['token'] = self.token
        dict_holiday['ip'] = self.client_url
        dict_holiday['holiday'] = holiday

        response = self.request.post(
            self.request_url['insert_holiday'],
            data={
                'dict_holiday': json.dumps(dict_holiday)
            }
        ).__dict__

        return self.get_response(response)
