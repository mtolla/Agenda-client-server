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

        new_list_activity = self.server_manager.activities_day(
            str(self.info_agenda['project']['ID']),
            str(data.day()) + "/" + str(data.month()) + "/" + str(data.year())
        )

        # ------------ Holidays -------------
        new_list_holiday = self.server_manager.holidays_day(
            str(self.info_agenda['project']['ID']),
            str(data.day()) + "/" + str(data.month()) + "/" + str(data.year())
        )

        self.agenda.set_list_activities(new_list_activity, new_list_holiday)

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
            for activity in self.info_agenda['activities']:
                if activity["ID"] == _id:
                    data['type'] = self.info_agenda['activities']['type']
            data['information'] = self.server_manager.activity_id(_id)
        else:
            group = False
            participants = []
            if self.info_agenda['level'] == "teamleader" and _type == "group":
                # ------------- non funziona query ----------------------
                '''
                group = self.server_manager.groups_teamleader(self.info_agenda['project']['ID'])
                '''
                group = {7: "AgendaGroup"}

            if group:
                participants = self.server_manager.group_id_participants(group.keys()[0])
            elif _type == "project":
                participants = self.server_manager.group_id_participants(self.info_agenda['project']['group'])

            data['modality'] = "create"
            data['type'] = _type
            data['information'] = {
                "group": group,
                "participants": participants,
                "location": self.server_manager.locations(),
                "activity": {
                    "name": "",
                    "project": self.info_agenda['project']['ID'],
                    "duration": 60,
                    "participants": [],
                    "location": [],
                    "date": {
                        "year": QtCore.QDate.currentDate().year(),
                        "month": QtCore.QDate.currentDate().month(),
                        "day": QtCore.QDate.currentDate().day(),
                        "hour": QtCore.QTime.currentTime().hour(),
                        "minute": QtCore.QTime.currentTime().minute()
                    },
                    "type": _type,
                    "ID": None,
                    "description": ""
                }
            }

        print data
        self.activity_manager.exec_(data)

    def create_holiday(self):
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    def create_single_activity(self):
        self.exec_activity_view(_type="single")

    def create_group_activity(self):
        self.exec_activity_view(_type="group")

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
        self.exec_activity_view(_type="project")
