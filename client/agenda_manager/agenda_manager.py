from client.gui.agenda_view import *
import json


class AgendaManager:
    def __init__(self):
        pass

    def show(self):
        self.agenda.show()

    def set_server_manager(self, server_manager):
        self.server_manager = server_manager
        self.info_agenda = server_manager.info_agenda()

        self.agenda = Agenda(self.info_agenda)

        self.agenda.connect(self.agenda.calendar, QtCore.SIGNAL("clicked(QDate)"), self.change_day)
        self.agenda.connect(self.agenda.logout, QtCore.SIGNAL('triggered()'), self.logout)

    def change_day(self, data):
        self.agenda.lbl_day.setText(str(data.day()))
        self.agenda.lbl_month.setText(QtCore.QDate.longMonthName(data.month()))
        self.agenda.lbl_year.setText(str(data.year()))

        new_list = self.server_manager.activities_day(
            str(data.day()) + "/" + str(data.month()) + "/" + str(data.year())
        )

        self.agenda.set_list_activities(new_list)

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
