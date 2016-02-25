import json
from datetime import datetime
from hashlib import sha512

"""
Funzioni e cosa devono ricevere:

- do_login(utente, password): riceve utente e password e genera il token, false se fallisce
- generate_token(utente): riceve il nome utente e crea il token
- logout(token): riceve il token e lo elimina, chiama delete_token()
- delete_token(token): elimina il token che riceve
- check_token(token): riceve un token e risponde True o False
"""

class ClassLoginManager:
    def __init__(self):
        # Legge il file utenti.json
        login_file = open("./utenti.json", "r")
        # Lo trasforma in un dizionario
        self.login_dict = json.loads(login_file.read())
        # Dizionario di token
        self.user_token = dict()

    def do_login(self, usr, psw):
        if not self.user_token.has_key(usr):
            for user in self.login_dict.iteritems():
                if user['id'] == usr and user['password'] == psw:
                    return self.generate_token(usr)
                else:
                    return False

    def do_login_token (self, token):
        return self.check_token(token)

    def generate_token(self, usr):
        self.user_token[usr] = dict()
        self.user_token[usr]['time'] = datetime.now().time()
        self.user_token[usr]['token'] = sha512(usr + str(self.user_token[usr]['time'])).hexdigest()
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

    ##def check_life_token(self,token):
      #  for users in self.user_token:
       #     if users['token'] == token:
         #       datetime.timedelta(users['time'],datetime.now().time())

