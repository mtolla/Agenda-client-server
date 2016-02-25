from createUserUI import *

class CreateUser(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.create)
    def create(self):
        #complete

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = CreateUser()
    main.show()
    sys.exit(app.exec_())
