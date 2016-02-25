# coding=utf-8
import json
from time import time
from hashlib import sha512

"""
Funzioni e cosa devono ricevere:

- do_login(utente, password): riceve utente e password e genera il token, false se fallisce
- generate_token(utente): riceve il nome utente e crea il token
- logout(token): riceve il token e lo elimina, chiama delete_token()
- delete_token(token): elimina il token che riceve
- check_token(token): riceve un token e risponde True o False
- check_life_token(token): controlla se il token è scaduto
"""

class ClassLoginManager:
    def __init__(self):
        # Legge il file utenti.json
        login_file = open("../Database/user.json", "r")
        # Lo trasforma in un dizionario
        self.login_dict = json.loads(login_file)
        # Dizionario di token
        self.user_token = dict()
        # Durata max token: 24 ore = 60 sec * 60 min * 24 h
        self.dur_token = 60*60*24

    def do_login(self, usr, psw):
        if not self.user_token.has_key(usr):
            for user in self.login_dict.iteritems():
                if user['id'] == usr and user['password'] == psw:
                    return self.generate_token(usr)
                else:
                    return False

    def do_login_token(self, token):
        return self.check_token(token)

    def generate_token(self, usr):
        self.user_token[usr] = dict()
        self.user_token[usr]['time'] = time()
        self.user_token[usr]['token'] = sha512(usr + str(self.user_token[usr]['time'])).hexdigest() # Verificare che serva hexdigest
        return self.user_token[usr]['token']

    def logout(self, token):
        return self.delete_token(token)

    def delete_token(self, token):
        for users in self.user_token:
            if users['token'] == token:
                return self.user_token.pop(users)

    def check_token(self, token):
        for users in self.user_token:
            if token == users['token']:
                return True
            else: return False

    def check_life_token(self):
        for users in self.user_token:
            if time() - users['time'] >= self.dur_token:
                self.user_token.pop(users)


