from client.interface.server_request_interface import ServerRequestInterface
import requests
import json


class ServerGetRequest(ServerRequestInterface):
    def __init__(self, server_url, client_url, token):
        ServerRequestInterface.__init__(self)

        self.request = requests

        self.request_url = {
            'projects': server_url + "/projects",
            'project_id': server_url + "/project/<int:prj>",
            'activities_day': server_url + "/project/<int:prj>/activities/<int:day>",
            'activity_id': server_url + "/project/<int:prj>/activity/<int:id>",
            'locations': server_url + "/locations",
            'groups_teamleader': server_url + "/project/<int:prj>/groups/teamleader",
            'group_id_participants': server_url + "/project/<int:prj>/group/<int:id>/participants",
            'project_id_participant': server_url + "/project/<int:prj>/participant",
            'project_id_groups': server_url + "/project/<int:prj>/groups",
            'groups_id_participant_level': server_url + "/project/<int:prj>/groups/<int:id>/participant/level",
            'project_id_not_participant': server_url + "/project/<int:prj>/not/participant",
            'participants': server_url + "/project/<int:prj>/participants",
            'groups_id_father': server_url + "/project/<int:prj>/groups/<int:id>/father",
            'holiday_id': server_url + "/project/<int:prj>/holiday/<int:id>",
            'logout': server_url + "/logout",
            'holidays_day': server_url + "/project/<int:prj>/holidays/<int:day>",
            'token_ip': "/" + token + "/" + client_url,
            'id': "<int:id>",
            'day': "<int:day>",
            'prj': "<int:prj>"
        }

    @staticmethod
    def get_response(response):
        if response['status_code'] == 200:
            return response['_content']

        return False

    def url_generator(self, url, replace=dict()):
        if replace:
            request_url = self.request_url[url]
            for key, value in replace.items():
                request_url = request_url.replace(self.request_url[key], value)
            return request_url + self.request_url['token_ip']
        else:
            return self.request_url[url] + self.request_url['token_ip']

    def projects(self):
        response = self.request.get(self.url_generator('projects')).__dict__

        return self.get_response(response)

    def project_id(self, _id):
        response = self.request.get(self.url_generator('project_id', _id)).__dict__

        return self.get_response(response)

    def activities_day(self, day):
        response = self.request.get(self.url_generator('activities_day', day)).__dict__

        return self.get_response(response)

    def activity_id(self, _id):
        response = self.request.get(self.url_generator('activity_id', _id)).__dict__

        return self.get_response(response)

    def locations(self):
        response = self.request.get(self.url_generator('locations')).__dict__

        return self.get_response(response)

    def groups_teamleader(self, prj):
        response = self.request.get(self.url_generator('groups_teamleader', prj)).__dict__

        return self.get_response(response)

    def group_id_participants(self, _id):
        response = self.request.get(self.url_generator('group_id_participants', _id)).__dict__

        return self.get_response(response)

    def project_id_participant(self, _id):
        response = self.request.get(self.url_generator('project_id_participant', _id)).__dict__

        return self.get_response(response)

    def project_id_groups(self, _id):
        response = self.request.get(self.url_generator('project_id_groups', _id)).__dict__

        return self.get_response(response)

    def groups_id_participant_level(self, _id):
        response = self.request.get(self.url_generator('groups_id_participant_level', _id)).__dict__

        return self.get_response(response)

    def project_id_not_participant(self, _id):
        response = self.request.get(self.url_generator('project_id_not_participant', _id)).__dict__

        return self.get_response(response)

    def participants(self, prj):
        response = self.request.get(self.url_generator('participants', prj)).__dict__

        return self.get_response(response)

    def groups_id_father(self, _id):
        response = self.request.get(self.url_generator('groups_id_father', _id)).__dict__

        return self.get_response(response)

    def holiday_id(self, _id):
        response = self.request.get(self.url_generator('holiday_id', _id)).__dict__

        return self.get_response(response)

    def logout(self):
        response = self.request.get(self.url_generator('logout')).__dict__

        return self.get_response(response)

    def holidays_day(self, day):
        response = self.request.get(self.url_generator('holidays_day', day)).__dict__

        return self.get_response(response)

