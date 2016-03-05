from PyQt4 import QtGui, QtCore
from client.local.file_location import *


class Activity(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle('ManageIT')
        self.setWindowIcon(QtGui.QIcon(MANAGE_IT))

        self.height_extend = 10 + 24 + 10 + 180 + 10
        self.width_extend = 50
        self.height = 26 + 10 + 190 + 10 + 7 + 50 + 10 + 25 + 10
        self.width = 363
        self.setFixedSize(QtCore.QSize(self.width, self.height))
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
        lyt_page -+-> gdr_data(lyt_data) -> | lbl_name         | txt_name          |
                  |                         | lbl_start        | dtm_start         |
                  |                         | lbl_end          | dtm_end           |
                  |                         | lbl_type         | cmb_type          |
                  |                         | lbl_group        | cmb_group         |
                  |                         | lbl_participants | scrl_participants |
                  +-> hrz_button(lyt_button) -> cmd_ok
        '''
        # Creazione del layout della pagina: lyt_page
        self.lyt_page = QtGui.QVBoxLayout()

        # Creazione del contenitore dei dati e del suo layout: gdr_data(lyt_data)
        self.gdr_data = QtGui.QWidget(self)
        self.gdr_data.setObjectName("gdr_data")

        self.lyt_data = QtGui.QGridLayout()

        # Definizione degli oggetti dei dati: | lbl_name         | txt_name     |
        #                                     | lbl_start        | dtm_start    |
        #                                     | lbl_end          | dtm_end      |
        #                                     | lbl_type         | cmb_type     |
        #                                     | lbl_location     | cmb_location |
        #                                     | lbl_group        | cmb_group    |
        #                                     | lbl_participants | +
        #                                                  +-------+
        #                                                  +-> scrl_participants -> vrt_participants(lyt_participants) |
        self.lbl_name = QtGui.QLabel("Name :", self.gdr_data)

        self.txt_name = QtGui.QLineEdit(self.gdr_data)

        self.lbl_start = QtGui.QLabel("Start :", self.gdr_data)

        self.dtm_start = QtGui.QDateTimeEdit(self.gdr_data)
        self.dtm_start.setDateTime(QtCore.QDateTime.currentDateTime())

        self.lbl_end = QtGui.QLabel("End :", self.gdr_data)

        self.dtm_end = QtGui.QDateTimeEdit(self.gdr_data)
        self.dtm_end.setDateTime(QtCore.QDateTime.currentDateTime().addDays(1))

        self.lbl_type = QtGui.QLabel("Type :", self.gdr_data)

        self.cmb_type = QtGui.QComboBox(self.gdr_data)
        self.cmb_type.addItem('single')
        self.cmb_type.addItem('group')

        self.lbl_location = QtGui.QLabel("Location :", self.gdr_data)

        self.cmb_location = QtGui.QComboBox(self.gdr_data)

        self.lyt_participants = QtGui.QVBoxLayout()

        # Aggiunta degli oggeti nel lyt_data
        self.lyt_data.addWidget(self.lbl_name, 0, 0)
        self.lyt_data.addWidget(self.txt_name, 0, 1)
        self.lyt_data.addWidget(self.lbl_start, 1, 0)
        self.lyt_data.addWidget(self.dtm_start, 1, 1)
        self.lyt_data.addWidget(self.lbl_end, 2, 0)
        self.lyt_data.addWidget(self.dtm_end, 2, 1)
        self.lyt_data.addWidget(self.lbl_type, 3, 0)
        self.lyt_data.addWidget(self.cmb_type, 3, 1)
        self.lyt_data.addWidget(self.lbl_location, 4, 0)
        self.lyt_data.addWidget(self.cmb_location, 4, 1)

        # Set layout del gdr_data
        self.gdr_data.setLayout(self.lyt_data)

        # Creazione del contenitore del bottone e del suo layout: hrz_button(lyt_button)
        self.hrz_button = QtGui.QWidget(self)
        self.hrz_button.setObjectName("hrz_button")

        self.lyt_button = QtGui.QHBoxLayout()

        # Definizione dell'oggetto del bottone: cmd_ok
        self.cmd_ok = QtGui.QPushButton("Ok", self.hrz_button)
        self.cmd_ok.setStatusTip("Ok")
        self.connect(self.cmd_ok, QtCore.SIGNAL("clicked()"), self.extend_to_group)

        # Aggiunta degli oggeti nel lyt_password
        self.lyt_button.addWidget(self.cmd_ok)

        # Set layout del hrz_password
        self.hrz_button.setLayout(self.lyt_button)

        # Aggiungiamo il contenitore e il scrlMappa nel vrt_page
        self.lyt_page.addWidget(self.gdr_data)
        self.lyt_page.addWidget(self.hrz_button)

        # Settiamo il layout della pagina
        self.setLayout(self.lyt_page)

    def extend_to_group(self):
        self.lbl_group = QtGui.QLabel("Group :", self.gdr_data)

        self.cmb_group = QtGui.QComboBox(self.gdr_data)

        self.lbl_participants = QtGui.QLabel("Participants :", self.gdr_data)

        # Creazione del contenitore della vrt_participants: scrl_participants
        self.scrl_participants = QtGui.QScrollArea(self.gdr_data)
        self.scrl_participants.setBackgroundRole(QtGui.QPalette.NoRole)
        self.scrl_participants.setObjectName("scrl_participants")

        # Creazione del contenitore dei partecipanti e il suo layout: vrt_participants(lyt_participants)
        self.vrt_participants = QtGui.QWidget(self.scrl_participants)

        # Aggiungiamo i contenitori nel vrtComandi
        self.chk = []
        for i in range(0, 10):
            self.chk.append(QtGui.QCheckBox("cacca", self.vrt_participants))
            self.lyt_participants.addWidget(self.chk[i])

        # Settiamo il layout del vrtComandi
        self.vrt_participants.setLayout(self.lyt_participants)

        # Aggiungiamo il vrtComandi nel scrlComandi
        self.scrl_participants.setWidget(self.vrt_participants)

        self.lyt_data.addWidget(self.lbl_group, 5, 0)
        self.lyt_data.addWidget(self.cmb_group, 5, 1)
        self.lyt_data.addWidget(self.lbl_participants, 6, 0)
        self.lyt_data.addWidget(self.scrl_participants, 6, 1)
        '''
        self.lyt_page.addWidget(self.scrl_participants)

        self.setLayout(self.lyt_page)
        self.setCentralWidget(self)
        '''
        self.setFixedSize(QtCore.QSize(self.width + self.width_extend, self.height + self.height_extend))
        self.setStyleSheet(
            '''
                * {
                    font-size: 15px;
                }

                #scrl_participants {
                    min-height: 180px;
                    max-height: 180px;
                }

                QLabel {
                    qproperty-alignment: 'AlignRight | AlignCenter';
                }
            '''
        )
