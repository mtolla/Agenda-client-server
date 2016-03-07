from client.gui.holiday_view import *


class HolidayManager:
    def __init__(self, agenda_manager):
        self.agenda_manager = agenda_manager

    def exec_(self, data):
        data['functions'] = self

        self.holiday = Holiday(data)

        if data['modality'] == "view":
            self.holiday.add_buttons(data['modality'], data['modify'])
        else:
            self.holiday.add_buttons(data['modality'], False)

        if data['modality'] == "view":
            self.holiday.set_enabled_view(False)

        self.holiday.exec_()
