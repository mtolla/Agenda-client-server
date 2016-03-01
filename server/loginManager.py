# -*- coding: utf-8 -*-
from time import time
from hashlib import sha512
# Importo dbManager
from dbManager import ClassDbManager

"""
Funzioni e cosa devono ricevere:

- do_login(utente, password): riceve utente e password e genera il token, false se fallisce
- generate_token(utente): riceve il nome utente e crea il token
- logout(token): riceve il token e lo elimina, chiama delete_token()
- delete_token(token): elimina il token che riceve
- check_token(token): riceve un token e risponde True o False
- check_life_token(token): controlla se il token è scaduto

user_token = {user:{time,token}}
"""


class ClassLoginManager:
    def __init__(self):

        # Dizionario di token
        self.user_token = dict()
        # Durata max token: 24 ore = 60 sec * 60 min * 24 h * 1000 msec
        # self.dur_token = 60 * 60 * 24
        self.dur_token = 5  # Durata test
        # Oggetto db_manager
        self.db_manager = ClassDbManager()

    def do_login(self, usr, psw, ip):
        if usr in self.user_token:
            self.delete_token(usr, False)
        if self.db_manager.do_login(usr, psw):
            return self.generate_token(usr, psw, ip)
        return False

    def do_login_token(self, token, ip):
        return self.check_token(token, ip)

    def generate_token(self, usr, psw, ip):
        self.user_token[usr] = dict()
        self.user_token[usr]['time'] = time()
        self.user_token[usr]['token'] = sha512(usr + psw + str(self.user_token[usr]['time'])).hexdigest()
        self.user_token[usr]['ip'] = ip
        return self.user_token[usr]['token']

    def logout(self, token):
        return self.delete_token(False, token)

    def delete_token(self, usr, token):
        # Con logout elimino passando il token
        # Con login elimino passando user
        if token:
            for key, user in self.user_token.items():
                if user['token'] == token:
                    self.user_token.pop(key)
                    break
        else:
            self.user_token.pop(usr)
        return True

    def check_token(self, token, ip):
        for key, users in self.user_token.items():
            if token == users['token']:
                if ip != users['ip']:
                    users['ip'] = ip
                return True
        return False

    def check_life_token(self):
        for key, users in self.user_token.items():
            if time() - users['time'] >= self.dur_token:
                self.user_token.pop(key)

    def from_token_get_user(self, token):
        for key, users in self.user_token.items():
            if token == users['token']:
                return key

    def from_user_get_ip(self, id):
        return self.user_token[id]['ip']
