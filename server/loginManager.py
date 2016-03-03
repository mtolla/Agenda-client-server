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
        # Durata max token: 24 ore = 60 sec * 60 min * 24 h * 1000 msec
        # self.token_exp = 60 * 60 * 24
        self.token_exp = 5  # Durata test
        # Oggetto db_manager
        self.db_manager = ClassDbManager()

    def do_login(self, usr, psw, ip):
        id_usr = self.db_manager.from_user_get_id(usr)
        if usr in self.user_token:
            self.delete_token(id_usr, False)
        if self.db_manager.do_login(usr, psw):
            app = self.generate_token(id_usr, psw, ip)
            print self.next_token_expire()
            return app
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
            print actual_time
            print users['exp']
            if actual_time == users['exp']:
                self.user_token.pop(key)

    def from_token_get_user(self, token):
        for key, users in self.user_token.items():
            if token == users['token']:
                return key

    def from_user_get_ip(self, id_usr):
        return self.user_token[id_usr]['ip']

    def next_token_expire(self):
        # Ora impostata di default
        next_exp = {"year": 9999, "minute": 99, "day": 99, "hour": 99, "month": 99}
        print self.user_token
        for key, token in self.user_token.items():
            if not next_exp or self.app_next_token_expire(next_exp, token):
                print token
                next_exp = token['exp']
        return next_exp

    @staticmethod
    def app_next_token_expire(next_exp, token):
        minor = True
        for item in range(0, len(token)):
            if next_exp[item] - token['exp'][item] < 0:
                minor = False
                break
        return minor
