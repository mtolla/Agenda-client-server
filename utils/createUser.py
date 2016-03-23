#!/usr/bin/env python2

from createUserUI import *
from populate import *
from client.abstract.page import *

class CreateUser(Page):
    def __init__(self):
        Page.__init__(self)
        self.ui = UiMainWindow()
        self.ui.setupui(self)
        self.connect(self.ui.push_button, QtCore.SIGNAL("clicked()"), self.create)

    @staticmethod
    def popup(message):
        Popup(message, ALERT).exec_()

    def create(self):
        # Recive data from UI
        self.username = str(self.ui.username_edit.text())
        self.password = str(self.ui.password_edit.text())
        self.email = str(self.ui.email_edit.text())
        self.name = str(self.ui.name_edit.text())
        self.surname = str(self.ui.surname_edit.text())
        # Put data into a dict
        if self.username == "" or self.password == "" or self.email == "" or self.name == "" or self.surname == "":
             self.popup("Inserire tutti i campi richiesti")
        else:
            data = populate_user(self.username, self.password,self.email, self.name, self.surname)
            # Write data into database
            add_dict(data, user_file)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = CreateUser()
    main.show()
    sys.exit(app.exec_())
