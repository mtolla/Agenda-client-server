from PyQt4 import QtGui, QtCore
from client.local.file_location import *


class Activity(QtGui.QDialog):
    def __init__(self, data):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle('ManageIT')
        self.setWindowIcon(QtGui.QIcon(MANAGE_IT))

        self.data = data

        #self.height_extend = 10 + 24 + 10 + 180 + 10
        #self.width_extend = 50
        #self.height = 26 + 10 + 190 + 10 + 7 + 50 + 10 + 25 + 10
        #self.width = 363
        #self.setFixedSize(QtCore.QSize(self.width, self.height))
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
                  |                         | lbl_description  | txt_description   |
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

        # Definizione degli oggetti dei dati: | lbl_name         | txt_name        |
        #                                     | lbl_start        | dtm_start       |
        #                                     | lbl_end          | dtm_end         |
        #                                     | lbl_description  | txt_description |
        #                                     | lbl_type         | cmb_type        |
        #                                     | lbl_location     | cmb_location    |
        #                                     | lbl_group        | cmb_group       |
        #                                     | lbl_participants | +
        #                                                  +-------+
        #                                                  +-> scrl_participants -> vrt_participants(lyt_participants) |
        self.lbl_name = QtGui.QLabel("Nome :", self.gdr_data)

        self.txt_name = QtGui.QLineEdit(self.gdr_data)
        self.txt_name.setText(self.data['information']['activity']['name'])

        self.lbl_start = QtGui.QLabel("Inizio :", self.gdr_data)

        self.dtm_start = QtGui.QDateTimeEdit(self.gdr_data)
        self.dtm_start.setDateTime(QtCore.QDateTime(
            self.data['information']['activity']['date']['year'],
            self.data['information']['activity']['date']['month'],
            self.data['information']['activity']['date']['day'],
            self.data['information']['activity']['date']['hour'],
            self.data['information']['activity']['date']['minute']
        ))
        self.dtm_start.setDisplayFormat("dd MMMM yyyy - hh:mm")

        self.lbl_end = QtGui.QLabel("Fine :", self.gdr_data)

        self.dtm_end = QtGui.QDateTimeEdit(self.gdr_data)
        self.dtm_end.setDateTime(self.dtm_start.dateTime().addSecs(
            60 * self.data['information']['activity']['duration']
        ))
        self.dtm_end.setDisplayFormat("dd MMMM yyyy - hh:mm")

        self.lbl_description = QtGui.QLabel("Descrizione :", self.gdr_data)

        self.txt_description = QtGui.QTextEdit(self.gdr_data)
        self.txt_description.setText(self.data['information']['activity']['description'])

        self.lbl_type_lbl = QtGui.QLabel("Tipo :", self.gdr_data)

        self.lbl_type = QtGui.QLabel(self.gdr_data)
        self.lbl_type.setText(self.data['type'])
        self.lbl_type.setStyleSheet("qproperty-alignment: 'AlignLeft | AlignVCenter';")

        self.lbl_location = QtGui.QLabel("Luogo :", self.gdr_data)

        self.cmb_location = QtGui.QComboBox(self.gdr_data)
        self.cmb_location.addItem(self.data['information']['location'])

        self.lyt_participants = QtGui.QVBoxLayout()

        # Aggiunta degli oggeti nel lyt_data
        self.lyt_data.addWidget(self.lbl_name, 0, 0)
        self.lyt_data.addWidget(self.txt_name, 0, 1)
        self.lyt_data.addWidget(self.lbl_start, 1, 0)
        self.lyt_data.addWidget(self.dtm_start, 1, 1)
        self.lyt_data.addWidget(self.lbl_end, 2, 0)
        self.lyt_data.addWidget(self.dtm_end, 2, 1)
        self.lyt_data.addWidget(self.lbl_description, 3, 0)
        self.lyt_data.addWidget(self.txt_description, 3, 1)
        self.lyt_data.addWidget(self.lbl_type_lbl, 4, 0)
        self.lyt_data.addWidget(self.lbl_type, 4, 1)
        self.lyt_data.addWidget(self.lbl_location, 5, 0)
        self.lyt_data.addWidget(self.cmb_location, 5, 1)

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
        self.lbl_group = QtGui.QLabel("Gruppo :", self.gdr_data)

        self.cmb_group = QtGui.QComboBox(self.gdr_data)
        self.cmb_group.addItem(self.data['information']['group'])

        self.lbl_participants = QtGui.QLabel("Partecipanti :", self.gdr_data)

        # Creazione del contenitore della vrt_participants: scrl_participants
        self.scrl_participants = QtGui.QScrollArea(self.gdr_data)
        self.scrl_participants.setBackgroundRole(QtGui.QPalette.NoRole)
        self.scrl_participants.setObjectName("scrl_participants")

        # Creazione del contenitore dei partecipanti e il suo layout: vrt_participants(lyt_participants)
        self.vrt_participants = QtGui.QWidget(self.scrl_participants)

        # Aggiungiamo i contenitori nel vrtComandi
        self.chk_participants = []
        i = 0
        for _id, name in self.data['information']['participants'].items():
            self.chk_participants.append(QtGui.QCheckBox(name, self.vrt_participants))
            self.chk_participants[i].setObjectName(str(_id))
            self.chk_participants[i].setChecked(True)
            self.lyt_participants.addWidget(self.chk_participants[i])
            i += 1

        # Settiamo il layout del vrtComandi
        self.vrt_participants.setLayout(self.lyt_participants)

        # Aggiungiamo il vrtComandi nel scrlComandi
        self.scrl_participants.setWidget(self.vrt_participants)

        self.lyt_data.addWidget(self.lbl_group, 6, 0)
        self.lyt_data.addWidget(self.cmb_group, 6, 1)
        self.lyt_data.addWidget(self.lbl_participants, 7, 0)
        self.lyt_data.addWidget(self.scrl_participants, 7, 1)
        '''
        self.lyt_page.addWidget(self.scrl_participants)

        self.setLayout(self.lyt_page)
        self.setCentralWidget(self)
        '''
        #self.setFixedSize(QtCore.QSize(self.width + self.width_extend, self.height + self.height_extend))
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
