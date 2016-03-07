from client.gui.group_view import *


class GroupManager:
    def __init__(self, agenda_manager):
        self.agenda_manager = agenda_manager

    def exec_(self, data):
        data['functions'] = self

        self.group = Group(data)

        '''
        if data['modality'] == "view":
            self.holiday.add_buttons(data['modality'], data['modify'])
        else:
            self.holiday.add_buttons(data['modality'], False)

        if data['modality'] == "view":
            self.holiday.set_enabled_view(False)
        '''
        self.group.exec_()
