from client.gui.agenda_view import *
from activity_manager import ActivityManager
import json


class AgendaManager:
    def __init__(self):
        self.activity_manager = ActivityManager()

    def show(self):
        self.agenda.show()

    def set_server_manager(self, server_manager):
        self.server_manager = server_manager
        self.info_agenda = server_manager.info_agenda()

        self.agenda = Agenda(self.info_agenda, self)

    def change_day(self, data):
        self.agenda.lbl_day.setText(str(data.day()))
        self.agenda.lbl_month.setText(QtCore.QDate.longMonthName(data.month()))
        self.agenda.lbl_year.setText(str(data.year()))

        new_list = self.server_manager.activities_day(
            str(data.day()) + "/" + str(data.month()) + "/" + str(data.year())
        )

        z = self.server_manager.holidays_day(
            str(data.day()) + "/" + str(data.month()) + "/" + str(data.year())
        )
        print z

        self.agenda.set_list_activities(new_list)

    def logout(self):
        if self.server_manager.logout() == "True":
            local_save = open(LOCAL_SAVE)
            variable = json.load(local_save)
            local_save.close()

            variable['token'] = False

            local_save = open(LOCAL_SAVE, "w")
            json.dump(variable, local_save)
            local_save.close()

            self.agenda.setHidden(True)

    def exec_activity_view(self, _id=False, _type="single"):
        data = dict()
        if _id:
            data['modality'] = "view"
            informations = self.server_manager.activity_id(_id)
        else:
            data['modality'] = "create"
            data['type'] = _type
            data['information'] = None

        self.activity_manager.exec_(data)

    def create_holiday(self):
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    def create_single_activity(self):
        self.exec_activity_view()

    def create_group_activity(self):
        self.exec_activity_view()

    def create_group(self):
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    def modify_group(self):
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    def create_project(self):
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    def modify_role(self):
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    def modify_project(self):
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    def create_activity_project(self):
        self.exec_activity_view()
