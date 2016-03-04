from client.gui.agenda_view import *


class AgendaManager:
    def __init__(self):
        pass

    def show(self):
        self.agenda.show()

    def set_server_manager(self, server_manager):
        self.server_manager = server_manager
        self.info_agenda = server_manager.info_agenda()

        self.agenda = Agenda(self.info_agenda)


