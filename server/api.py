# coding=utf-8
# Importo librerie

# Importo dbManager
from dbManager import ClassDbManager
# Importo loginManager
from loginManager import ClassLoginManager
# Importo backgroundThread
from PyQt4 import QtCore
import time


class Api():
    def __init__(self):
        # Creazione oggetti db,login Manager
        self.dbManager = ClassDbManager()
        self.loginManager = ClassLoginManager()
        # Variabili cotrollo login
        self.usrMaxLen = 10
        self.pswMaxLen = 10
        # Creazione thread controllo token
        token_thread = TokenThread(self)
        QtCore.QThreadPool.globalInstance().start(token_thread)

    # Login con user, password
    def do_login(self, user, password):
        if self.valid_credentials(user, password):
            return self.loginManager.do_login(user, password)

    # Login con token
    def do_login_token(self, token):
        return self.loginManager.do_login_token(token)

    # Controllo credenziali
    def valid_credentials(self, user, psw):
        if len(user) <= self.usrMaxLen and len(psw) <= self.pswMaxLen:
            return True
        else:
            return False


# Classe Thread controllo token
class TokenThread(QtCore.QRunnable):
    def __init__(self):
        QtCore.QRunnable.__init__(self)
        self.loginManager = ClassLoginManager()
        self.sleep_time = 36000  # 10 Minuti

    def run(self):
        while True:
            self.loginManager.check_life_token()
            time.sleep(self.sleep_time)
