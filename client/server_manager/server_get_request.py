from client.interface.server_request_interface import ServerRequestInterface
import requests


class ServerGetRequest(ServerRequestInterface):
    def __init__(self, server_url, client_url, token):
        ServerRequestInterface.__init__(self)

        self.request = requests

        self.request_url = {
            'projects': server_url + "/projects",
            'project_id': server_url + "/project/<int:id>",
            'activities_day': server_url + "/activities/<int:day>",
            'activity_id': server_url + "/activity/<int:id>",
            'locations': server_url + "/locations",
            'groups_teamleader': server_url + "/groups/teamleader",
            'groups_id_participant': server_url + "/groups/<int:id>/participant",
            'project_id_participant': server_url + "/project/<int:id>/participant",
            'project_id_groups': server_url + "/project/<int:id>/groups",
            'groups_id_participant_level': server_url + "/groups/<int:id>/participant/level",
            'project_id_not_participant': server_url + "/project/<int:id>/not/participant",
            'participants': server_url + "/participants",
            'groups_id_father': server_url + "/groups/<int:id>/father",
            'holiday_id>': server_url + "/holiday/<int:id>",
            'token_ip': "/" + token + "/" + client_url,
            'id': "<int:id>",
            'day': "<int:day>"
        }

    @staticmethod
    def get_response(response):
        if response['status_code'] == 200:
            return response['_content']

        return False

    def projects(self):
        response = self.request.get(self.request_url['projects']).__dict__

        return self.get_response(response)

    def project_id(self, _id):
        response = self.request.get(self.request_url['project_id'].replace(self.request_url['id'], _id)).__dict__

        return self.get_response(response)

    def activities_day(self, day):
        response = self.request.get(self.request_url['activities_day'].replace(self.request_url['day'], day)).__dict__

        return self.get_response(response)

    def activity_id(self, _id):
        response = self.request.get(self.request_url['activity_id'].replace(self.request_url['id'], _id)).__dict__

        return self.get_response(response)

    def locations(self):
        response = self.request.get(self.request_url['locations']).__dict__

        return self.get_response(response)

    def groups_teamleader(self):
        response = self.request.get(self.request_url['groups_teamleader']).__dict__

        return self.get_response(response)

    def groups_id_participant(self, _id):
        response = self.request.get(self.request_url['groups_id_participant'].replace(self.request_url['id'], _id)).__dict__

        return self.get_response(response)

    def project_id_participant(self, _id):
        response = self.request.get(self.request_url['project_id_participant'].replace(self.request_url['id'], _id)).__dict__

        return self.get_response(response)

    def project_id_groups(self, _id):
        response = self.request.get(self.request_url['project_id_groups'].replace(self.request_url['id'], _id)).__dict__

        return self.get_response(response)

    def groups_id_participant_level(self, _id):
        response = self.request.get(self.request_url['groups_id_participant_level'].replace(self.request_url['id'], _id)).__dict__

        return self.get_response(response)

    def project_id_not_participant(self, _id):
        response = self.request.get(self.request_url['project_id_not_participant'].replace(self.request_url['id'], _id)).__dict__

        return self.get_response(response)

    def participants(self):
        response = self.request.get(self.request_url['participants']).__dict__

        return self.get_response(response)

    def groups_id_father(self, _id):
        response = self.request.get(self.request_url['groups_id_father'].replace(self.request_url['id'], _id)).__dict__

        return self.get_response(response)

    def holiday_id(self, _id):
        response = self.request.get(self.request_url['holiday_id'].replace(self.request_url['id'], _id)).__dict__

        return self.get_response(response)

