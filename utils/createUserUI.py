# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crateUser.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(385, 335)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 381, 211))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setHorizontalSpacing(99)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.surnameEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.surnameEdit.setObjectName(_fromUtf8("surnameEdit"))
        self.gridLayout.addWidget(self.surnameEdit, 3, 1, 1, 1)
        self.usernameEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.usernameEdit.setText(_fromUtf8(""))
        self.usernameEdit.setEchoMode(QtGui.QLineEdit.Normal)
        self.usernameEdit.setObjectName(_fromUtf8("usernameEdit"))
        self.gridLayout.addWidget(self.usernameEdit, 0, 1, 1, 1)
        self.passwordLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.passwordLabel.setObjectName(_fromUtf8("passwordLabel"))
        self.gridLayout.addWidget(self.passwordLabel, 1, 0, 1, 1)
        self.nameLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.gridLayout.addWidget(self.nameLabel, 2, 0, 1, 1)
        self.surnameLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.surnameLabel.setObjectName(_fromUtf8("surnameLabel"))
        self.gridLayout.addWidget(self.surnameLabel, 3, 0, 1, 1)
        self.nameEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.gridLayout.addWidget(self.nameEdit, 2, 1, 1, 1)
        self.usernameLabel = QtGui.QLabel(self.gridLayoutWidget)
        self.usernameLabel.setObjectName(_fromUtf8("usernameLabel"))
        self.gridLayout.addWidget(self.usernameLabel, 0, 0, 1, 1)
        self.passwordEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.passwordEdit.setText(_fromUtf8(""))
        self.passwordEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordEdit.setObjectName(_fromUtf8("passwordEdit"))
        self.gridLayout.addWidget(self.passwordEdit, 1, 1, 1, 1)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 230, 88, 34))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 385, 30))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.passwordLabel.setText(_translate("MainWindow", "Password", None))
        self.nameLabel.setText(_translate("MainWindow", "Name", None))
        self.surnameLabel.setText(_translate("MainWindow", "Surname", None))
        self.usernameLabel.setText(_translate("MainWindow", "Username", None))
        self.pushButton.setText(_translate("MainWindow", "Create", None))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le", None))
        self.actionQuit.setText(_translate("MainWindow", "Quit", None))

