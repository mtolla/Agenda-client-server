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
        token_thread = TokenThread()
        QtCore.QThreadPool.globalInstance().start(token_thread)

    # Login con user, password
    def do_login(self, user, password):
        #if self.valid_credentials(user, password):
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

    def badass_function(self, token, id_proj):
        # Dato token e id progetto restituire:
        #   - L'oggetto del progetto
        #   - eMail project manager
        #   - T/F se è almeno teamleader in un gruppo
        #   - Tutti id e nomi attività del progetto
        # Dizionario di ritorno
        dict_return = dict()
        dict_return['project'] = self.dbManager.get_proj_from_id_proj(id_proj)
        dict_return['email'] = self.dbManager.get_pjmanager_email(id_proj)
        id_user = self.loginManager.from_token_get_id(token)
        dict_return['isteamleader'] = self.dbManager.is_teamleader(id_user)
        dict_return['activities'] = self.dbManager.get_activities_from_proj(id_proj)
        return dict_return

    def test(self):
        return self.loginManager.user_token


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
