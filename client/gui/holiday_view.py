from PyQt4 import QtGui, QtCore
from client.local.file_location import *
from client.abstract.popup import Popup
from client.abstract.dialog import Dialog


class Holiday(Dialog):
    def __init__(self, data):
        Dialog.__init__(self, data)

        self.data = data

        # ------------------------------------- Pagina -------------------------------------
        '''
        lyt_page -+-> gdr_data(lyt_data) -> | lbl_creator_lbl  | lbl_creator       |
                  |                         | lbl_name         | txt_name          |
                  |                         | lbl_start        | dtm_start         |
                  |                         | lbl_end          | dtm_end           |
                  +-> hrz_button(lyt_button) -> cmd_modify | cmd_ok || cmd_creator | cmd_annul
        '''
        self.txt_name.setText(self.data['holiday']['name'])

        self.dtm_start.setDate(QtCore.QDate(
            self.data['holiday']['begin']['year'],
            self.data['holiday']['begin']['month'],
            self.data['holiday']['begin']['day']
        ))
        self.dtm_start.setDisplayFormat("dd MMMM yyyy")

        self.dtm_end.setDate(QtCore.QDate(
            self.data['holiday']['end']['year'],
            self.data['holiday']['end']['month'],
            self.data['holiday']['end']['day']
        ))
        self.dtm_end.setDisplayFormat("dd MMMM yyyy")

    def add_buttons(self, **kwargs):
        modality = self.data['modality']
        modify = self.data['modify']
        Dialog.add_buttons(modality, modify)

    def switch_to_create(self):
        self.lyt_button.removeWidget(self.cmd_modify)
        self.lyt_button.removeWidget(self.cmd_delete)
        self.lyt_button.removeWidget(self.cmd_ok)
        self.cmd_modify.deleteLater()
        self.cmd_delete.deleteLater()
        self.cmd_ok.deleteLater()

        self.set_enabled_view()

        self.add_create_buttons()

    def set_enabled_view(self, enabled=True):
        self.txt_name.setEnabled(enabled)
        self.dtm_start.setEnabled(enabled)
        self.dtm_end.setEnabled(enabled)

    @staticmethod
    def get_date(dtm):
        return {
            'year': QtCore.QDate(dtm.date()).year(),
            'month': QtCore.QDate(dtm.date()).month(),
            'day': QtCore.QDate(dtm.date()).day()
        }

    @staticmethod
    def is_before(start, end):
        if start['year'] < end['year'] or \
                (start['year'] == end['year'] and start['month'] < end['month']) or \
                (start['year'] == end['year'] and start['month'] == end['month'] and start['day'] <= end['day']):
            return True
        return False

    @staticmethod
    def max_one_month(start, end):
        if 30 >= QtCore.QDate(start['year'], start['month'], start['day']).daysTo(
                QtCore.QDate(end['year'], end['month'], end['day'])):
            return True
        return False

    def set_time(self, start, end):
        if self.is_before(start, end):
            if self.max_one_month(start, end):
                self.holday['begin'] = start
                self.holday['end'] = end
                return True
            else:
                Popup("Non puoi fare piu di un mese di vacanza!", ALERT).exec_()
        else:
            Popup("Date invertite!", ALERT).exec_()
        return False

    @staticmethod
    def delete():
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    def insert(self):
        self.holday = dict()

        self.holday['name'] = self.set_name()
        if not self.holday['name']:
            return False

        start = self.get_date(self.dtm_start)
        end = self.get_date(self.dtm_end)
        if not self.set_time(start, end):
            return False

        if self.data['functions'].insert_holiday(self.holday):
            self.close()
        else:
            Popup("Ricontrolla se la tua vacanza non collide con delle tue attivita'!", ALERT).exec_()
