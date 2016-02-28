# -*- coding: utf-8 -*-
from gui.login_view import *
from interface.login_interface import LoginInterface
from server_manager.server_manager import ServerManager
from agenda_manager.agenda_manager import AgendaManager
import hashlib
import json


class LoginManager(LoginInterface):
    def __init__(self):
        LoginInterface.__init__(self)

        self.local_save = open(LOCAL_SAVE)
        self.variable = json.load(self.local_save)
        self.local_save.close()

        self.login = Login()
        self.login.connect(self.login.cmd_login, QtCore.SIGNAL("clicked()"), self.do_login)

        self.user = dict()

        self.server_manager = ServerManager()

    def do_login(self):
        """
        Login con user e id:
            Se le credenziali inserite sono corrette viene restituito il token per effettuare il login
            Altrimenti deve rieffettuare il login con user e password
        """

        if self.credential_digest():
            self.variable['token'] = self.server_manager.get_token(self.user)

            if self.variable['token']:
                self.exec_agenda_manager()
            else:
                Popup("User o password errate", ALERT).exec_()

    def exec_agenda_manager(self):
        """
        Login con token:
            Se il token è valido, l'utente viene portato alla pagina dell'agenda
            Altrimenti deve rieffettuare il login con user e password
        """

        if self.server_manager.do_login(self.variable['token']):
            agenda_manager = AgendaManager(self.server_manager, self.variable['token'])
            agenda_manager.exec_()
        else:
            self.variable['token'] = False
            Popup("Sessione scaduta, rifare il login", ALERT).exec_()
            self.login.show()

    def exec_(self):
        """
        Apertura del programma:
            Se nelle variabili locali non esiste una sessione salvata, l'utente deve effettuare il login con
                user e password
            Altrimenti può effettuare il login diretto con il token salvato
        """

        if not self.variable['token']:
            self.login.show()
        else:
            self.exec_agenda_manager()

    def credential_digest(self):
        """
        Controllo credenziali:
            Se user e password non sono vuoti, cripta la password in sha 512 e ritorna True
            Altrimenti deve reinserire user e password e ritorna False
        :return: True or False
        """

        self.user['username'] = str(self.login.txt_user.text())
        self.user['password'] = str(self.login.txt_password.text())

        if self.user['username'] != "" and self.user['password'] != "":
            self.user['password'] = hashlib.sha512(self.user['password']).hexdigest()
            return True
        else:
            self.user['username'] = ""
            self.user['password'] = ""
            Popup("Inserire user e password", ALERT).exec_()
            return False


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = LoginManager()
    main.exec_()
    sys.exit(app.exec_())
