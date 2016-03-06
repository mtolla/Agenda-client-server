from client.gui.activity_view import *


class ActivityManager:
    def __init__(self, agenda_manager):
        self.agenda_manager = agenda_manager

    def exec_(self, data):
        data['functions'] = self

        self.activity = Activity(data)

        if data['type'] != "single":
            self.activity.extend()

        self.activity.add_buttons()

        if data['modality'] == "view":
            self.activity.set_enabled_view(False)

            if data['type'] != "single":
                self.activity.checked_participants()

        self.activity.exec_()

    def get_remain_participants(self, _id, already_participants):
        participants = self.agenda_manager.get_participants(_id)

        for key in already_participants.keys():
            participants.pop(key)

        return participants

