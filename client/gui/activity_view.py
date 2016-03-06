from PyQt4 import QtGui, QtCore
from client.local.file_location import *
from client.gui.popup import Popup


class Activity(QtGui.QDialog):
    def __init__(self, data):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle('ManageIT')
        self.setWindowIcon(QtGui.QIcon(MANAGE_IT))

        self.data = data

        # self.height_extend = 10 + 24 + 10 + 180 + 10
        # self.width_extend = 50
        # self.height = 26 + 10 + 190 + 10 + 7 + 50 + 10 + 25 + 10
        # self.width = 363
        # self.setFixedSize(QtCore.QSize(self.width, self.height))
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
                  |                         | lbl_description  | txt_description   |
                  |                         | lbl_type         | cmb_type          |
                  |                         | lbl_group        | cmb_group         |
                  |                         | lbl_participants | scrl_participants |
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
        #                                     | lbl_description  | txt_description |
        #                                     | lbl_type         | cmb_type        |
        #                                     | lbl_location     | cmb_location    |
        #                                     | lbl_group        | cmb_group       |
        #                                     | lbl_participants | +
        #                                                  +-------+
        #                                                  +-> scrl_participants -> vrt_participants(lyt_participants) |
        self.lbl_creator_lbl = QtGui.QLabel("Creatore :", self.gdr_data)

        self.lbl_creator = QtGui.QLabel(self.data['creator'].values()[0], self.gdr_data)
        self.lbl_creator.setStyleSheet("qproperty-alignment: 'AlignLeft | AlignVCenter';")

        self.lbl_name = QtGui.QLabel("Nome :", self.gdr_data)

        self.txt_name = QtGui.QLineEdit(self.gdr_data)
        self.txt_name.setText(self.data['informations']['activity']['name'])

        self.lbl_start = QtGui.QLabel("Inizio :", self.gdr_data)

        self.dtm_start = QtGui.QDateTimeEdit(self.gdr_data)
        self.dtm_start.setDateTime(QtCore.QDateTime(
            self.data['informations']['activity']['date']['year'],
            self.data['informations']['activity']['date']['month'],
            self.data['informations']['activity']['date']['day'],
            self.data['informations']['activity']['date']['hour'],
            self.data['informations']['activity']['date']['minute']
        ))
        self.dtm_start.setDisplayFormat("dd MMMM yyyy - hh:mm")

        self.lbl_end = QtGui.QLabel("Fine :", self.gdr_data)

        self.dtm_end = QtGui.QDateTimeEdit(self.gdr_data)
        self.dtm_end.setDateTime(self.dtm_start.dateTime().addSecs(
            60 * self.data['informations']['activity']['duration']
        ))
        self.dtm_end.setDisplayFormat("dd MMMM yyyy - hh:mm")

        self.lbl_description = QtGui.QLabel("Descrizione :", self.gdr_data)

        self.txt_description = QtGui.QTextEdit(self.gdr_data)
        self.txt_description.setText(self.data['informations']['activity']['description'])

        self.lbl_type_lbl = QtGui.QLabel("Tipo :", self.gdr_data)

        self.lbl_type = QtGui.QLabel(self.gdr_data)
        self.lbl_type.setText(self.data['type'])
        self.lbl_type.setStyleSheet("qproperty-alignment: 'AlignLeft | AlignVCenter';")

        self.lbl_location = QtGui.QLabel("Luogo :", self.gdr_data)

        self.cmb_location = QtGui.QComboBox(self.gdr_data)
        for location in self.data['locations']:
            self.cmb_location.addItem(location.values()[0])

        # Aggiunta degli oggeti nel lyt_data
        self.lyt_data.addWidget(self.lbl_creator_lbl, 0, 0)
        self.lyt_data.addWidget(self.lbl_creator, 0, 1)
        self.lyt_data.addWidget(self.lbl_name, 1, 0)
        self.lyt_data.addWidget(self.txt_name, 1, 1)
        self.lyt_data.addWidget(self.lbl_start, 2, 0)
        self.lyt_data.addWidget(self.dtm_start, 2, 1)
        self.lyt_data.addWidget(self.lbl_end, 3, 0)
        self.lyt_data.addWidget(self.dtm_end, 3, 1)
        self.lyt_data.addWidget(self.lbl_description, 4, 0)
        self.lyt_data.addWidget(self.txt_description, 4, 1)
        self.lyt_data.addWidget(self.lbl_type_lbl, 5, 0)
        self.lyt_data.addWidget(self.lbl_type, 5, 1)
        self.lyt_data.addWidget(self.lbl_location, 6, 0)
        self.lyt_data.addWidget(self.cmb_location, 6, 1)

        # Set layout del gdr_data
        self.gdr_data.setLayout(self.lyt_data)

        # Creazione del contenitore del bottone e del suo layout: hrz_button(lyt_button)
        self.hrz_button = QtGui.QWidget(self)
        self.hrz_button.setObjectName("hrz_button")

        self.lyt_button = QtGui.QHBoxLayout()

        # Set layout del hrz_password
        self.hrz_button.setLayout(self.lyt_button)

        # Aggiungiamo il contenitore e lo scrlMappa
        self.lyt_page.addWidget(self.gdr_data)
        self.lyt_page.addWidget(self.hrz_button)

        # Settiamo il layout della pagina
        self.setLayout(self.lyt_page)

    def extend(self):
        index = 7

        if self.data['type'] == "group":
            self.lbl_group = QtGui.QLabel("Gruppo :", self.gdr_data)

            self.cmb_group = QtGui.QComboBox(self.gdr_data)
            for group in self.data['groups']:
                self.cmb_group.addItem(group.values()[0])
            self.connect(self.cmb_group, QtCore.SIGNAL("currentIndexChanged(int)"), self.change_group)

            self.lyt_data.addWidget(self.lbl_group, index, 0)
            self.lyt_data.addWidget(self.cmb_group, index, 1)

            index += 1

        self.lbl_participants = QtGui.QLabel("Partecipanti :", self.gdr_data)

        # Creazione del contenitore della vrt_participants: scrl_participants
        self.scrl_participants = QtGui.QScrollArea(self.gdr_data)
        self.scrl_participants.setBackgroundRole(QtGui.QPalette.NoRole)
        self.scrl_participants.setObjectName("scrl_participants")

        # Aggiungiamo i contenitori nel vrtComandi
        self.chk_participants = {}
        self.add_participants(self.data['informations']['participants'])

        self.lyt_data.addWidget(self.lbl_participants, index, 0)
        self.lyt_data.addWidget(self.scrl_participants, index, 1)

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

    def add_buttons(self):
        if self.data['modality'] == "view":
            if self.data['informations']['modify']:
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

    def switch_to_create(self):
        self.lyt_button.removeWidget(self.cmd_modify)
        self.lyt_button.removeWidget(self.cmd_delete)
        self.lyt_button.removeWidget(self.cmd_ok)
        self.cmd_modify.deleteLater()
        self.cmd_delete.deleteLater()
        self.cmd_ok.deleteLater()

        self.set_enabled_view()

        if self.data['type'] != "single":
            participants = self.data['functions'].get_remain_participants(
                self.data['informations']['activity']['group'],
                self.data['informations']['participants']
            )
            self.add_participants(participants)

        self.add_create_buttons()

    def set_enabled_view(self, enabled=True):
        self.txt_name.setEnabled(enabled)
        self.dtm_start.setEnabled(enabled)
        self.dtm_end.setEnabled(enabled)
        self.txt_description.setEnabled(enabled)
        self.cmb_location.setEnabled(enabled)

        if self.data['type'] != "single":
            if self.data['type'] == "group":
                self.cmb_group.setEnabled(False)

            self.scrl_participants.setEnabled(enabled)

    def checked_participants(self):
        for chk in self.chk_participants.values():
            chk.setChecked(True)

    def add_participants(self, participants):
        # Creazione del contenitore dei partecipanti e il suo layout: vrt_participants(lyt_participants)
        self.vrt_participants = QtGui.QWidget(self.scrl_participants)

        self.lyt_participants = QtGui.QVBoxLayout()

        for chk_participant in self.chk_participants.values():
            self.lyt_participants.addWidget(chk_participant)

        for _id, name in participants.items():
            self.chk_participants[_id] = QtGui.QCheckBox(name, self.vrt_participants)
            self.chk_participants[_id].setObjectName(str(_id))
            self.lyt_participants.addWidget(self.chk_participants[_id])

        # Settiamo il layout del vrtComandi
        self.vrt_participants.setLayout(self.lyt_participants)

        # Aggiungiamo il vrtComandi nel scrlComandi
        self.scrl_participants.setWidget(self.vrt_participants)

    def change_group(self, index):
        self.data['informations']['participants'] = self.data['functions'].get_remain_participants(
            self.data['groups'][index].keys()[0],
            {}
        )

        self.chk_participants = {}

        self.add_participants(self.data['informations']['participants'])

    def delete(self):
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    def insert(self):
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

