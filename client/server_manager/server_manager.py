# -*- coding: utf-8 -*-
from login_gateway import LoginGateway
from server_request_handler import ServerRequestHandler
from client.local.file_location import *
from client.gui.popup import Popup
import json


class ServerManager:
    def __init__(self):
        self.local_save = open(LOCAL_SAVE)
        self.variable = json.load(self.local_save)
        self.local_save.close()

        self.server_url = self.variable['server_url']

        self.client_url = self.variable['client_url']

        self.login_gateway = LoginGateway(self.server_url, self.client_url)

        self.server_request_handler = ServerRequestHandler(self.server_url, self.client_url)

    @staticmethod
    def notify(notifications):
        if not notifications:
            return

        Popup("Ei hai delle notifiche!!!!", NOTIFICATION).exec_()

    def get_token(self, user):
        """
        Dato l'utente richiama il login_gateway per ricevere il token
        :param user: dizionario uresrname, password
        :return: token or False
        """
        contents = json.loads(self.login_gateway.get_token(user))

        self.notify(contents[1])

        return contents[0]

    def do_login(self, token):
        """
        Dato il token richiama il login_gateway per controllarne la validità
        :param token: string
        :return: True or False
        """
        self.server_request_handler.set_token(token)

        return self.login_gateway.do_login(token)

    def info_agenda(self):
        projects = json.loads(self.server_request_handler.projects())

        if projects:
            agenda = json.loads(self.server_request_handler.project_id({
                'prj': projects.keys()[0]
            }))
            if agenda:
                agenda['projects'] = projects
                return agenda
        return False

    def activities_day(self, prj, day):
        return json.loads(self.server_request_handler.activities_day({
            'prj': prj,
            'day': day
        }))

    def activity_id(self, prj, _id):
        return json.loads(self.server_request_handler.activity_id({
            'prj': prj,
            'id': _id
        }))

    def locations(self):
        return self.server_request_handler.locations()

    def groups_teamleader(self, prj):
        return self.server_request_handler.groups_teamleader({
            'prj': prj
        })

    def group_id_participants(self, prj, _id):
        return self.server_request_handler.group_id_participants({
            'prj': prj,
            'id': _id
        })

    def project_id_participant(self, _id):
        return self.server_request_handler.project_id_participant({
            'id': _id
        })

    def project_id_groups(self, _id):
        return self.server_request_handler.project_id_groups({
            'id': _id
        })

    def groups_id_participant_level(self, prj, _id):
        return self.server_request_handler.groups_id_participant_level({
            'prj': prj,
            'id': _id
        })

    def project_id_not_participant(self, _id):
        return self.server_request_handler.project_id_not_participant({
            'id': _id
        })

    def participants(self, prj):
        return self.server_request_handler.participants({
            'prj': prj
        })

    def groups_id_father(self, prj, _id):
        return self.server_request_handler.groups_id_father({
            'prj': prj,
            'id': _id
        })

    def holiday_id(self, prj, _id):
        return self.server_request_handler.holiday_id({
            'prj': prj,
            'id': _id
        })

    def logout(self):
        return self.server_request_handler.logout()

    def holidays_day(self, prj, day):
        return json.loads(self.server_request_handler.holidays_day({
            'prj': prj,
            'day': day
        }))
