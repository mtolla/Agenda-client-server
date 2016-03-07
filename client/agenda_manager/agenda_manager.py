from client.gui.agenda_view import *
from activity_manager import ActivityManager
from holiday_manager import HolidayManager
from group_manager import GroupManager
import json


class AgendaManager:
    def __init__(self):
        self.activity_manager = ActivityManager(self)

        self.holiday_manager = HolidayManager(self)

        self.group_manager = GroupManager(self)

    def show(self):
        self.agenda.show()

    def set_server_manager(self, server_manager):
        self.server_manager = server_manager
        self.info_agenda = server_manager.info_agenda()

        self.holidays = self.info_agenda['holidays']

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
        self.holidays = self.server_manager.holidays_day(
            self.info_agenda['project']['ID'],
            str(data.day()) + "/" + str(data.month()) + "/" + str(data.year())
        )

        self.agenda.set_list_activities(new_list_activity, self.holidays)

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

    def exec_holiday_view(self, _id=False):
        data = dict()
        if _id:
            data['modality'] = "view"
            data.update(self.get_holiday(_id))
            data['modify'] = self.info_agenda['user'] == data['creator']
        else:
            data['modality'] = "create"
            data['creator'] = self.info_agenda['user']
            data['holiday'] = {
                'begin': {
                    'month': QtCore.QDate.currentDate().month(),
                    'day': QtCore.QDate.currentDate().day(),
                    'year': QtCore.QDate.currentDate().year()
                },
                'end': {
                    'month': QtCore.QDate.currentDate().month(),
                    'day': QtCore.QDate.currentDate().addDays(1).day(),
                    'year': QtCore.QDate.currentDate().year()
                },
                'name': ""
            }

        self.holiday_manager.exec_(data)

    def exec_activity_view(self, _id=False, _type="single"):
        data = dict()

        data['locations'] = self.server_manager.locations()
        data['project_group'] = self.info_agenda['project']['group']

        if _id:
            data['modality'] = "view"
            data['informations'] = self.server_manager.activity_id(_id)
            data['type'] = data['informations']['activity']['type']
            data['informations']['participants'] = self.sort_participants(data['informations']['participants'])
            data['creator'] = {
                str(data['informations']['activity']['creator']):
                    data['informations']['participants'][str(data['informations']['activity']['creator'])]
            }
            data['groups'] = [{
                str(data['informations']['activity']['group']):
                    data['informations']['group']
            }]
        else:
            group = False
            groups = False
            participants = {}
            if self.info_agenda['level'] == "teamleader" and _type == "group":
                groups = self.groups_teamleader(self.info_agenda['project']['ID'])

                group = groups[0].values()[0]

                data['groups'] = groups

            if groups:
                participants = self.get_participants(groups[0].keys()[0])
            elif _type == "project":
                group = self.info_agenda['project']['group']
                participants = self.get_participants(self.info_agenda['project']['group'])
                for _id, name in self.info_agenda['user'].items():
                    participants[_id] = name

            data['creator'] = self.info_agenda['user']
            data['modality'] = "create"
            data['type'] = _type
            data['informations'] = {
                'group': group,
                'participants': participants,
                'location': data['locations'][0].values()[0],
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
        self.exec_holiday_view()

    def create_single_activity(self):
        self.exec_activity_view()

    def create_group_activity(self):
        self.exec_activity_view(_type="group")

    @staticmethod
    def create_group():
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    def modify_group(self):
        self.group_manager.exec_({
            'type': "group",
            'groups': [],
            'informations': {
                'participants': {}
            }
        })

    @staticmethod
    def create_project():
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    @staticmethod
    def modify_role():
        Popup("Work in progess!!!! Stiamo lavorando per voi", NOTIFICATION).exec_()

    @staticmethod
    def modify_project():
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

    def get_participants(self, _id):
        participants = self.server_manager.group_id_participants(_id)
        participants = self.sort_participants(self.reformat_participants(participants))
        return participants

    def groups_teamleader(self, prj):
        return self.server_manager.groups_teamleader(prj)

    def insert_activity(self, activity):
        return self.server_manager.insert_activity(activity)

    def get_holiday(self, _id):
        for key, holidays in self.holidays.items():
            for holiday in holidays:
                if holiday['ID'] == _id:
                    return {
                        'creator': {
                            str(key): self.server_manager.participant_id(key)
                        },
                        'holiday': holiday
                    }

    def change_project(self, index):
        project_list = self.info_agenda['projects']
        self.info_agenda = self.server_manager.info_agenda(project_list.keys()[index])
        self.info_agenda['projects'] = project_list
        return self.info_agenda

    def insert_holiday(self, holiday):
        return self.server_manager.insert_holiday(holiday)
