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
            self.info_agenda['project']['ID'],
            str(data.day()) + "/" + str(data.month()) + "/" + str(data.year())
        )

        # ------------ Holidays -------------
        new_list_holiday = self.server_manager.holidays_day(
            self.info_agenda['project']['ID'],
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
            data['informations'] = self.server_manager.activity_id(_id)
            data['type'] = data['informations']['activity']['type']
            data['informations']['participants'] = self.sort_participants(data['informations']['participants'])
            data['creator'] = {
                str(data['informations']['activity']['creator']):
                data['informations']['participants'][str(data['informations']['activity']['creator'])]
            }
        else:
            group = False
            groups = False
            participants = {}
            if self.info_agenda['level'] == "teamleader" and _type == "group":
                groups = self.server_manager.groups_teamleader(self.info_agenda['project']['ID'])

                group = groups[0].values()[0]

                data['groups'] = groups

            if groups:
                participants = self.server_manager.group_id_participants(groups[0].keys()[0])
                participants = self.sort_participants(self.reformat_participants(participants))
            elif _type == "project":
                group = self.info_agenda['project']['group']
                participants = self.server_manager.group_id_participants(self.info_agenda['project']['group'])
                participants = self.sort_participants(self.reformat_participants(participants))

            location = self.server_manager.locations()

            data['creator'] = self.info_agenda['user']
            data['modality'] = "create"
            data['type'] = _type
            data['informations'] = {
                'group': group,
                'participants': participants,
                'location': location[0].values()[0],
                'activity': {
                    'name': "",
                    'project': self.info_agenda['project']['ID'],
                    'duration': 60,
                    'participants': [],
                    'location': [],
                    'date': {
                        'year': QtCore.QDate.currentDate().year(),
                        'month': QtCore.QDate.currentDate().month(),
                        'day': QtCore.QDate.currentDate().day(),
                        'hour': QtCore.QTime.currentTime().hour(),
                        'minute': QtCore.QTime.currentTime().minute()
                    },
                    'type': _type,
                    'ID': None,
                    'description': ""
                }
            }

        self.activity_manager.exec_(data)

    def create_holiday(self):
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    def create_single_activity(self):
        self.exec_activity_view()

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

    @staticmethod
    def reformat_participants(participants):
        dict_app = {}
        for participant in participants:
            for _id, name in participant.items():
                dict_app[_id] = name
        return dict_app

    @staticmethod
    def sort_participants(participants):
        new_participants = dict()

        for key in sorted(
            participants,
            key=lambda k: participants.keys()):
            new_participants[key] = participants[key]

        return new_participants

