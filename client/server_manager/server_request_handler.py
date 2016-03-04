from server_post_request import ServerPostRequest
from server_get_request import ServerGetRequest


class ServerRequestHandler:
    def __init__(self, server_url, client_url):
        self.server_url = server_url

        self.client_url = client_url

    def set_token(self, token):
        self.server_post_request = ServerPostRequest(self.server_url, self.client_url, token)

        self.server_get_request = ServerGetRequest(self.server_url, self.client_url, token)

    # Get method ------------------------------------------------------------------------------------------------------
    def projects(self):
        return self.server_get_request.projects()

    def project_id(self, _id):
        return self.server_get_request.project_id(_id)

    def activities_day(self, day):
        return self.server_get_request.activities_day(day)

    def activity_id(self, _id):
        return self.server_get_request.activity_id(_id)

    def locations(self):
        return self.server_get_request.locations()

    def groups_teamleader(self):
        return self.server_get_request.groups_teamleader()

    def group_id_participants(self, _id):
        return self.server_get_request.group_id_participants(_id)

    def project_id_participant(self, _id):
        return self.server_get_request.project_id_participant(_id)

    def project_id_groups(self, _id):
        return self.server_get_request.project_id_groups(_id)

    def groups_id_participant_level(self, _id):
        return self.server_get_request.groups_id_participant_level(_id)

    def project_id_not_participant(self, _id):
        return self.server_get_request.project_id_not_participant(_id)

    def participants(self):
        return self.server_get_request.participants()

    def groups_id_father(self, _id):
        return self.server_get_request.groups_id_father(_id)

    def holiday_id(self, _id):
        return self.server_get_request.holiday_id(_id)
