from client.abstract.page import *


class Login(Page):
    def __init__(self):
        Page.__init__(self)

        self.setFixedSize(QtCore.QSize(363, 211))
        self.setStyleSheet(
            '''
                * {
                    font-size: 15px;
                }

                QLabel {
                    qproperty-alignment: 'AlignRight | AlignCenter';
                }
            '''
        )

        # ------------------------------------- Pagina -------------------------------------
        '''
        vrt_page(lyt_page) -+-> gdr_data(lyt_data) -> | lbl_user     | txt_user     |
                            |                         | lbl_password | txt_password |
                            +-> hrz_buttons(lyt_buttons) -+-> cmd_login
                                                          +-> cmd_pwd_forget
        '''
        # Creazione della pagina e del suo layout: vrt_page(lyt_page)
        self.vrt_page = QtGui.QWidget(self)

        self.lyt_page = QtGui.QVBoxLayout()

        # Creazione del contenitore dei dati e del suo layout: gdr_data(lyt_data)
        self.gdr_data = QtGui.QWidget(self.vrt_page)

        self.lyt_data = QtGui.QGridLayout()

        # Definizione degli oggetti dei dati: | lbl_user     | txt_user     |
        #                                     | lbl_password | txt_password |
        self.lbl_user = QtGui.QLabel("User :", self.gdr_data)

        self.txt_user = QtGui.QLineEdit(self.gdr_data)

        self.lbl_password = QtGui.QLabel("Password :", self.gdr_data)

        self.txt_password = QtGui.QLineEdit(self.gdr_data)
        self.txt_password.setEchoMode(QtGui.QLineEdit.Password)

        # Aggiunta degli oggeti nel lyt_data
        self.lyt_data.addWidget(self.lbl_user, 0, 0)
        self.lyt_data.addWidget(self.txt_user, 0, 1)
        self.lyt_data.addWidget(self.lbl_password, 1, 0)
        self.lyt_data.addWidget(self.txt_password, 1, 1)

        # Set layout del gdr_data
        self.gdr_data.setLayout(self.lyt_data)

        # Creazione del contenitore dei bottoni e del suo layout: hrz_buttons(lyt_buttons)
        self.hrz_buttons = QtGui.QWidget(self.vrt_page)

        self.lyt_buttons = QtGui.QHBoxLayout()

        # Definizione dei 2 oggetti dei bottoni: cmd_login
        #                                        cmd_pwd_forget
        self.cmd_login = QtGui.QPushButton("LogIn", self.hrz_buttons)
        self.cmd_login.setStatusTip("LogIn")

        self.cmd_pwd_forget = QtGui.QPushButton("Password lost?", self.hrz_buttons)
        self.cmd_pwd_forget.setFlat(True)
        self.cmd_pwd_forget.setStatusTip("Password lost?")
        self.connect(self.cmd_pwd_forget, QtCore.SIGNAL("clicked()"), self.pwd_forget)

        # Aggiunta degli oggeti nel lyt_password
        self.lyt_buttons.addWidget(self.cmd_login)
        self.lyt_buttons.addWidget(self.cmd_pwd_forget)

        # Set layout del hrz_password
        self.hrz_buttons.setLayout(self.lyt_buttons)

        # Aggiunta del gdr_data e l'hrz_buttons nel vrt_page
        self.lyt_page.addWidget(self.gdr_data)
        self.lyt_page.addWidget(self.hrz_buttons)

        # Set del layout della pagina
        self.vrt_page.setLayout(self.lyt_page)

        # Set del widget della pagina
        self.setCentralWidget(self.vrt_page)

    @staticmethod
    def pwd_forget():
        Popup("Per recuperare la password, contattare un amministratore", ALERT).exec_()
