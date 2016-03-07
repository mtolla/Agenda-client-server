from PyQt4 import QtGui, QtCore
from client.local.file_location import *
from popup import Popup


class Dialog(QtGui.QDialog):
    def __init__(self, data):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle('ManageIT')
        self.setWindowIcon(QtGui.QIcon(MANAGE_IT))

        self.data = data

        self.index_group = 0
        self.index_location = 0
        self.setStyleSheet(
            '''
                * {
                    font-size: 15px;
                }

                #hrz_button {
                    min-height: 50px;
                    max-height: 50px;
                }

                QLabel {
                    qproperty-alignment: 'AlignRight | AlignCenter';
                }
            '''
        )

        # ------------------------------------- Pagina -------------------------------------
        '''
        lyt_page -+-> gdr_data(lyt_data) -> | lbl_creator_lbl  | lbl_creator       |
                  |                         | lbl_name         | txt_name          |
                  |                         | lbl_start        | dtm_start         |
                  |                         | lbl_end          | dtm_end           |
                  +-> hrz_button(lyt_button) -> cmd_modify | cmd_ok || cmd_creator | cmd_annul
        '''
        # Creazione del layout della pagina: lyt_page
        self.lyt_page = QtGui.QVBoxLayout()

        # Creazione del contenitore dei dati e del suo layout: gdr_data(lyt_data)
        self.gdr_data = QtGui.QWidget(self)
        self.gdr_data.setObjectName("gdr_data")

        self.lyt_data = QtGui.QGridLayout()

        # Definizione degli oggetti dei dati: | lbl_creator_lbl  | lbl_creator     |
        #                                     | lbl_name         | txt_name        |
        #                                     | lbl_start        | dtm_start       |
        #                                     | lbl_end          | dtm_end         |
        self.lbl_creator_lbl = QtGui.QLabel("Creatore :", self.gdr_data)

        self.lbl_creator = QtGui.QLabel(self.data['creator'].values()[0], self.gdr_data)
        self.lbl_creator.setStyleSheet("qproperty-alignment: 'AlignLeft | AlignVCenter';")

        self.lbl_name = QtGui.QLabel("Nome :", self.gdr_data)

        self.txt_name = QtGui.QLineEdit(self.gdr_data)

        self.lbl_start = QtGui.QLabel("Inizio :", self.gdr_data)

        self.dtm_start = QtGui.QDateTimeEdit(self.gdr_data)

        self.lbl_end = QtGui.QLabel("Fine :", self.gdr_data)

        self.dtm_end = QtGui.QDateTimeEdit(self.gdr_data)

        # Aggiunta degli oggeti nel lyt_data
        self.lyt_data.addWidget(self.lbl_creator_lbl, 0, 0)
        self.lyt_data.addWidget(self.lbl_creator, 0, 1)
        self.lyt_data.addWidget(self.lbl_name, 1, 0)
        self.lyt_data.addWidget(self.txt_name, 1, 1)
        self.lyt_data.addWidget(self.lbl_start, 2, 0)
        self.lyt_data.addWidget(self.dtm_start, 2, 1)
        self.lyt_data.addWidget(self.lbl_end, 3, 0)
        self.lyt_data.addWidget(self.dtm_end, 3, 1)

        # Set layout del gdr_data
        self.gdr_data.setLayout(self.lyt_data)

        # Creazione del contenitore del bottone e del suo layout: hrz_button(lyt_button)
        self.hrz_button = QtGui.QWidget(self)
        self.hrz_button.setObjectName("hrz_button")

        self.lyt_button = QtGui.QHBoxLayout()

        # Set layout del hrz_button
        self.hrz_button.setLayout(self.lyt_button)

        # Aggiungiamo la tabella e il contenitore dei bottoni
        self.lyt_page.addWidget(self.gdr_data)
        self.lyt_page.addWidget(self.hrz_button)

        # Settiamo il layout della pagina
        self.setLayout(self.lyt_page)

    def add_buttons(self, modality, modify):
        if modality == "view":
            if modify:
                # Definizione dell'oggetto del bottone: cmd_modify
                self.cmd_modify = QtGui.QPushButton("Modifica", self.hrz_button)
                self.cmd_modify.setStatusTip("Modifica")
                self.connect(self.cmd_modify, QtCore.SIGNAL("clicked()"), self.switch_to_create)

                # Aggiunta degli oggeti nel lyt_button
                self.lyt_button.addWidget(self.cmd_modify)

                # Definizione dell'oggetto del bottone: cmd_eliminate
                self.cmd_delete = QtGui.QPushButton("Elimina", self.hrz_button)
                self.cmd_delete.setStatusTip("Elimina")
                self.connect(self.cmd_delete, QtCore.SIGNAL("clicked()"), self.delete)

                # Aggiunta degli oggeti nel lyt_button
                self.lyt_button.addWidget(self.cmd_delete)

            # Definizione dell'oggetto del bottone: cmd_ok
            self.cmd_ok = QtGui.QPushButton("Ok", self.hrz_button)
            self.cmd_ok.setStatusTip("Ok")
            self.connect(self.cmd_ok, QtCore.SIGNAL("clicked()"), self.close)

            # Aggiunta degli oggeti nel lyt_button
            self.lyt_button.addWidget(self.cmd_ok)
        else:
            self.add_create_buttons()

    def switch_to_create(self):
        pass

    def add_create_buttons(self):
        # Definizione dell'oggetto del bottone: cmd_creator
        self.cmd_creator = QtGui.QPushButton("Crea", self.hrz_button)
        self.cmd_creator.setStatusTip("Crea")
        self.connect(self.cmd_creator, QtCore.SIGNAL("clicked()"), self.insert)

        # Aggiunta degli oggeti nel lyt_button
        self.lyt_button.addWidget(self.cmd_creator)

        # Definizione dell'oggetto del bottone: cmd_annul
        self.cmd_annul = QtGui.QPushButton("Annulla", self.hrz_button)
        self.cmd_annul.setStatusTip("Annulla")
        self.connect(self.cmd_annul, QtCore.SIGNAL("clicked()"), self.close)

        # Aggiunta degli oggeti nel lyt_button
        self.lyt_button.addWidget(self.cmd_annul)

    def set_enabled_view(self, enabled=True):
        pass

    @staticmethod
    def get_date(dtm):
        pass

    def set_time(self, start, end):
        pass

    def set_name(self):
        name = str(self.txt_name.text())
        if name != "":
            return name
        else:
            Popup("Inserire nome!", ALERT).exec_()
            return False

    @staticmethod
    def delete():
        pass

    def insert(self):
        pass

