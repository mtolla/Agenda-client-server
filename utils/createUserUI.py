# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'crateUser.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromutf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromutf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class UiMainWindow(object):
    def setupui(self, main_window):
        main_window.setObjectName(_fromutf8("MainWindow"))
        main_window.resize(385, 335)
        self.centralwidget = QtGui.QWidget(main_window)
        self.centralwidget.setObjectName(_fromutf8("centralwidget"))
        self.grid_layout_widget = QtGui.QWidget(self.centralwidget)
        self.grid_layout_widget.setGeometry(QtCore.QRect(0, 0, 381, 211))
        self.grid_layout_widget.setObjectName(_fromutf8("gridLayoutWidget"))
        self.grid_layout = QtGui.QGridLayout(self.grid_layout_widget)
        self.grid_layout.setHorizontalSpacing(99)
        self.grid_layout.setObjectName(_fromutf8("gridLayout"))

        self.username_edit = QtGui.QLineEdit(self.grid_layout_widget)
        self.username_edit.setText(_fromutf8(""))
        self.username_edit.setEchoMode(QtGui.QLineEdit.Normal)
        self.username_edit.setObjectName(_fromutf8("usernameEdit"))
        self.grid_layout.addWidget(self.username_edit, 0, 1, 1, 1)

        self.password_label = QtGui.QLabel(self.grid_layout_widget)
        self.password_label.setObjectName(_fromutf8("password_label"))
        self.grid_layout.addWidget(self.password_label, 1, 0, 1, 1)

        self.name_label = QtGui.QLabel(self.grid_layout_widget)
        self.name_label.setObjectName(_fromutf8("name_label"))
        self.grid_layout.addWidget(self.name_label, 3, 0, 1, 1)

        self.surname_label = QtGui.QLabel(self.grid_layout_widget)
        self.surname_label.setObjectName(_fromutf8("surname_label"))
        self.grid_layout.addWidget(self.surname_label, 4, 0, 1, 1)

        self.username_label = QtGui.QLabel(self.grid_layout_widget)
        self.username_label.setObjectName(_fromutf8("username_label"))
        self.grid_layout.addWidget(self.username_label, 0, 0, 1, 1)

        self.password_edit = QtGui.QLineEdit(self.grid_layout_widget)
        self.password_edit.setText(_fromutf8(""))
        self.password_edit.setEchoMode(QtGui.QLineEdit.Password)
        self.password_edit.setObjectName(_fromutf8("password_edit"))

        self.email_edit = QtGui.QLineEdit(self.grid_layout_widget)
        self.email_edit.setText(_fromutf8(""))
        self.email_edit.setObjectName(_fromutf8("email_edit"))
        self.grid_layout.addWidget(self.email_edit, 2, 1, 1, 1)

        self.name_edit = QtGui.QLineEdit(self.grid_layout_widget)
        self.name_edit.setObjectName(_fromutf8("name_edit"))
        self.grid_layout.addWidget(self.name_edit, 3, 1, 1, 1)

        self.surname_edit = QtGui.QLineEdit(self.grid_layout_widget)
        self.surname_edit.setObjectName(_fromutf8("surname_edit"))
        self.grid_layout.addWidget(self.surname_edit, 4, 1, 1, 1)

        self.grid_layout.addWidget(self.password_edit, 1, 1, 1, 1)
        self.email_label = QtGui.QLabel(self.grid_layout_widget)
        self.email_label.setObjectName(_fromutf8("email_label"))
        self.grid_layout.addWidget(self.email_label, 2, 0, 1, 1)

        self.push_button = QtGui.QPushButton(self.centralwidget)
        self.push_button.setGeometry(QtCore.QRect(140, 230, 88, 34))
        self.push_button.setObjectName(_fromutf8("push_button"))
        main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(main_window)
        self.statusbar.setObjectName(_fromutf8("statusbar"))
        main_window.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 385, 30))
        self.menubar.setObjectName(_fromutf8("menubar"))
        self.menu_file = QtGui.QMenu(self.menubar)
        self.menu_file.setObjectName(_fromutf8("menu_file"))
        main_window.setMenuBar(self.menubar)
        self.action_quit = QtGui.QAction(main_window)
        self.action_quit.setObjectName(_fromutf8("action_quit"))
        self.menu_file.addAction(self.action_quit)
        self.menubar.addAction(self.menu_file.menuAction())

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        main_window.setWindowTitle(_translate("Create New User", "Create New User", None))
        self.username_label.setText(_translate("MainWindow", "Username", None))
        self.password_label.setText(_translate("MainWindow", "Password", None))
        self.email_label.setText(_translate("MainWindow", "Email", None))
        self.name_label.setText(_translate("MainWindow", "Name", None))
        self.surname_label.setText(_translate("MainWindow", "Surname", None))
        self.push_button.setText(_translate("MainWindow", "Create", None))
        self.menu_file.setTitle(_translate("MainWindow", "Fi&le", None))
        self.action_quit.setText(_translate("MainWindow", "Quit", None))


