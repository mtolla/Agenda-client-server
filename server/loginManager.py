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
        # Durata max token: 24 ore = 60 sec * 60 min * 24 h
        self.dur_token = 60 * 60 * 24
        # Oggetto db_manager
        self.db_manager = ClassDbManager()

    def do_login(self, usr, psw):
        if usr in self.user_token:
            self.delete_token(usr, False)
        if self.db_manager.do_login(usr, psw):
            return self.generate_token(usr)
        return False

    def do_login_token(self, token):
        return self.check_token(token)

    def generate_token(self, usr):
        self.user_token[usr] = dict()
        self.user_token[usr]['time'] = time()
                                                                    # Verificare che serva hexdigest
        self.user_token[usr]['token'] = sha512(usr + str(self.user_token[usr]['time'])).hexdigest()
        return self.user_token[usr]['token']

    def logout(self, token):
        return self.delete_token(False, token)

    def delete_token(self, usr, token):
        if token:
            for user in self.user_token:
                if user['token'] == token:
                    return self.user_token.pop(user)
        else:
            return self.user_token.pop(usr)

    def check_token(self, token):
        for users in self.user_token:
            if token == users['token']:
                return True
            else:
                return False

    def check_life_token(self):
        for users in self.user_token:
            if time() - users['time'] >= self.dur_token:
                self.user_token.pop(users)

    def from_token_get_id(self, token):
        for users in self.user_token:
            if token == users['token']:
                return users
