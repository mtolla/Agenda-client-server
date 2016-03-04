# -*- coding: utf-8 -*-
from hashlib import sha512
# Importo db_manager
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
        # Oggetto db_manager
        self.db_manager = ClassDbManager()

    def do_login(self, usr, psw, ip):
        id_usr = self.db_manager.from_user_get_id(usr)
        if usr in self.user_token:
            self.delete_token(id_usr, False)
        if self.db_manager.do_login(usr, psw):
            return self.generate_token(id_usr, psw, ip)
        return False

    def do_login_token(self, token, ip):
        return self.check_token(token, ip)

    def generate_token(self, usr, psw, ip):
        self.user_token[usr] = dict()
        current_time = self.db_manager.time_now()
        self.user_token[usr]['time'] = current_time
        self.user_token[usr]['token'] = sha512(str(usr) + psw + str(self.user_token[usr]['time'])).hexdigest()
        self.user_token[usr]['ip'] = ip
        token_exp = self.db_manager.time_now()
        token_exp['day'] += 1
        self.user_token[usr]['exp'] = token_exp
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

    def check_life_token(self, actual_time):
        for key, users in self.user_token.items():
            if actual_time == users['exp']:
                self.user_token.pop(key)

    def from_token_get_user(self, token):
        for key, users in self.user_token.items():
            if token == users['token']:
                return self.db_manager.from_id_get_user(key)

    def from_user_get_ip(self, id_usr):
        return self.user_token[id_usr]['ip']

    def next_token_expire(self):
        # Ora impostata di default
        next_exp = {"year": 9999, "minute": 99, "day": 99, "hour": 99, "month": 99}
        for key, token in self.user_token.items():
            # Controllo se è minore
            if self.app_next_token_expire(next_exp, token):
                next_exp = token['exp']
        return next_exp

    def app_next_token_expire(self, next_exp, token):
        if next_exp['hour'] - token['exp']['hour'] > 0:
            return True
        if next_exp['hour'] - token['exp']['hour'] == 0:
            if next_exp['minute'] - token['exp']['minute'] > 0:
                return True
        return False
