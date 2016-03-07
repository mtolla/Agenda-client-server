from client.gui.group_view import *


class GroupManager:
    def __init__(self, agenda_manager):
        self.agenda_manager = agenda_manager

    def exec_(self, data):
        data['functions'] = self

        self.group = Group(data)

        self.group.extend()

        self.group.add_buttons("creation", True)

        self.group.checked_participants()

        self.groups_id_father(data['project'], data['ID'])
        #self.group.add_participants()

        self.group.exec_()

    def get_remain_participants(self, _id, already_participants):
        participants = self.agenda_manager.get_participants(_id)

        for key in already_participants.keys():
            participants.pop(key)

        return participants

    def groups_id_father(self, prj, _id):
        print self.agenda_manager.groups_id_father(prj, _id)
