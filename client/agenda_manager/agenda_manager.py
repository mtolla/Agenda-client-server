from client.gui.agenda_view import *


class AgendaManager:
    def __init__(self, server_manager):
        self.server_manager = server_manager

        self.agenda = Agenda()

    def exec_(self):
        self.agenda.show()
