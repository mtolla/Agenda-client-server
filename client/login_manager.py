from gui.login_view import *
from login_interface import *
from server_manager import *
from agenda_manager import *
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
        self.user['user'] = str(self.login.txt_user.text())
        self.user['password'] = self.credential_digest()

        self.variable['token'] = self.server_manager.get_token(self.user)

        if self.variable['token']:
            self.exec_agenda_manager()

    def exec_agenda_manager(self):
        if self.server_manager.do_login(self.variable['token']):
            agenda_manager = AgendaManager(self.server_manager, self.variable['token'])
            agenda_manager.exec_()

    def exec_(self):
        if not self.variable['token']:
            self.login.show()
        else:
            self.exec_agenda_manager()

    def credential_digest(self):
        return hashlib.sha512(self.login.txt_password.text()).hexdigest()


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = LoginManager()
    main.exec_()
    sys.exit(app.exec_())
