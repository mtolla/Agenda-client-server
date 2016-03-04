from client.gui.agenda_view import *


class AgendaManager(QtGui.QApplication):
    def __init__(self, server_manager):
        QtGui.QApplication.__init__(self, sys.argv)

        self.server_manager = server_manager

        self.info_agenda = server_manager.info_agenda()

        self.agenda = Agenda(self.info_agenda)

        self.agenda.show()

