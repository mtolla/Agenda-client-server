from PyQt4 import QtGui, QtCore
from client.local.file_location import *
from client.abstract.popup import Popup
from client.abstract.dialog import Dialog


class Activity(Dialog):
    def __init__(self, data):
        Dialog.__init__(self, data)
        '''
        # ------------------------------------- Pagina -------------------------------------

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

        self.txt_name.setText(self.data['informations']['activity']['name'])

        self.dtm_start.setDateTime(QtCore.QDateTime(
            self.data['informations']['activity']['date']['year'],
            self.data['informations']['activity']['date']['month'],
            self.data['informations']['activity']['date']['day'],
            self.data['informations']['activity']['date']['hour'],
            self.data['informations']['activity']['date']['minute']
        ))
        self.dtm_start.setDisplayFormat("dd MMMM yyyy - hh:mm")

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
        self.connect(self.cmb_location, QtCore.SIGNAL("currentIndexChanged(int)"), self.change_location)

        # Aggiunta degli oggeti nel lyt_data
        self.lyt_data.addWidget(self.lbl_description, 4, 0)
        self.lyt_data.addWidget(self.txt_description, 4, 1)
        self.lyt_data.addWidget(self.lbl_type_lbl, 5, 0)
        self.lyt_data.addWidget(self.lbl_type, 5, 1)
        self.lyt_data.addWidget(self.lbl_location, 6, 0)
        self.lyt_data.addWidget(self.cmb_location, 6, 1)

    def add_buttons(self, **kwargs):
        modality = self.data['modality']
        modify = self.data['informations']['modify']
        Dialog.add_buttons(modality, modify)

    def switch_to_create(self):
        self.lyt_button.removeWidget(self.cmd_modify)
        self.lyt_button.removeWidget(self.cmd_delete)
        self.lyt_button.removeWidget(self.cmd_ok)
        self.cmd_modify.deleteLater()
        self.cmd_delete.deleteLater()
        self.cmd_ok.deleteLater()

        self.set_enabled_view()

        if self.data['type'] != "single":
            if self.data['type'] == "project":
                self.data['informations']['participants'].pop(self.data['creator'].keys()[0])

            participants = self.data['functions'].get_remain_participants(
                self.data['informations']['activity']['group'],
                self.data['informations']['participants']
            )

            if self.data['type'] == "project":
                self.data['informations']['participants'].update(self.data['creator'])

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
            if self.data['creator'].has_key(_id):
                self.chk_participants[_id].setEnabled(False)
                self.chk_participants[_id].setChecked(True)
            self.lyt_participants.addWidget(self.chk_participants[_id])

        # Settiamo il layout del vrtComandi
        self.vrt_participants.setLayout(self.lyt_participants)

        # Aggiungiamo il vrtComandi nel scrlComandi
        self.scrl_participants.setWidget(self.vrt_participants)

    def change_group(self, index):
        self.index_group = index

        self.data['informations']['participants'] = self.data['functions'].get_remain_participants(
            self.data['groups'][index].keys()[0],
            {},
            self.data['type']
        )

        self.chk_participants = {}

        self.add_participants(self.data['informations']['participants'])

    def change_location(self, index):
        self.index_location = index

    @staticmethod
    def get_date(dtm):
        return {
            'year': QtCore.QDate(dtm.date()).year(),
            'month': QtCore.QDate(dtm.date()).month(),
            'day': QtCore.QDate(dtm.date()).day(),
            'hour': QtCore.QTime(dtm.time()).hour(),
            'minute': QtCore.QTime(dtm.time()).minute()
        }

    @staticmethod
    def is_before(start, end):
        return start['hour'] < end['hour'] or \
               (start['hour'] == end['hour'] and start['minute'] <= end['minute'])

    @staticmethod
    def get_duration(start, end):
        return (end['hour'] - start['hour']) * 60 + abs(end['minute'] - start['minute'])

    @staticmethod
    def is_same_day(start, end):
        return start['year'] == end['year'] and \
               start['month'] == end['month'] and \
               start['day'] == end['day']

    def set_time(self, start, end):
        if self.is_same_day(start, end):
            if self.is_before(start, end):
                duration = self.get_duration(start, end)
                if duration >= 30:
                    self.activity['date'] = start
                    self.activity['duration'] = self.get_duration(start, end)
                    return True
                else:
                    Popup("Durata di almeno 30 minuti!", ALERT).exec_()
            else:
                Popup("Attenzione agli orari!", ALERT).exec_()
        else:
            Popup("Deve iniziare e finire nello stesso giorno!", ALERT).exec_()
        return False

    def set_description(self):
        description = str(self.txt_description.toPlainText()).strip()
        if description != "":
            self.activity['description'] = description
            return True
        else:
            Popup("Inserire descrizione!", ALERT).exec_()
            return False

    def get_checked(self):
        participants = []
        for _id, chk in self.chk_participants.items():
            if chk.isChecked():
                participants.append(int(_id))
        return participants

    def set_group_project(self):
        if self.data['type'] == "group":
            self.activity['group'] = int(self.data['groups'][self.index_group].keys()[0])
        else:
            self.activity['group'] = self.data['project_group']

        participants = self.get_checked()
        if len(participants) < 2:
            Popup("Almeno 2 partecipanti!", ALERT).exec_()
            return False
        self.activity['participants'] = participants

        return True

    @staticmethod
    def delete():
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    def insert(self):
        self.activity = dict()

        self.activity['name'] = self.set_name()
        start = self.get_date(self.dtm_start)
        end = self.get_date(self.dtm_end)

        if not self.activity['name'] and not self.set_time(start, end) and not self.set_description():
            return False

        self.activity['location'] = int(self.data['locations'][self.index_location].keys()[0])

        self.activity['group'] = 0

        self.activity['participants'] = [int(self.data['creator'].keys()[0])]

        self.activity['creator'] = int(self.data['creator'].keys()[0])

        self.activity['type'] = self.data['type']

        self.activity['project'] = self.data['informations']['activity']['project']

        if self.data['type'] != "single" and not self.set_group_project():
            return False

        if self.data['functions'].insert_activity(self.activity):
            self.close()
        else:
            Popup("Ricontrolla se la tua nuova attivita' non collide con delle altre!", ALERT).exec_()


