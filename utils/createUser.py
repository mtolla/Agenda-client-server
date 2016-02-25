from createUserUI import *
import json
import hashlib
from pprint import pprint

class CreateUser(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.create)
        self.connect(self.ui.actionQuit, QtCore.SIGNAL("triggered()"), QtCore.SLOT("close()"))
    def create(self):
        self.output = dict()
        self.username = self.ui.usernameEdit.text()
        # Encoding password with a secure one-way encryption algorithm
        self.password = hashlib.sha512(self.ui.passwordEdit.text()).hexdigest()
        self.name = self.ui.nameEdit.text()
        self.surname = self.ui.surnameEdit.text()

        # Load json user data
        with open("../database/user.json") as datafile:
            userdata = json.load(datafile)
        datafile.close()

        # Load Last +1 index
        last = str(userdata.keys().__len__())
        print last

        userdata[last] = dict()
        userdata[last]["username"] = str(self.username)
        userdata[last]["name"] = str(self.name)
        userdata[last]["surname"] = str(self.surname)
        userdata[last]["password"] = self.password
        userdata[last]["group"] = dict()
        userdata[last]["holiday"] = dict()
        pprint(userdata)

        with open("../database/user.json", "w") as datafile:
            json.dump(userdata, datafile)
        datafile.close()
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = CreateUser()
    main.show()
    sys.exit(app.exec_())
