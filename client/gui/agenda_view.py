from page import *


class Agenda(Page):
    def __init__(self):
        Page.__init__(self)

        # ------------------------------------- Pagina -------------------------------------
        # Creazione della pagina e del suo layout: gdr_agenda(lyt_agenda)
        self.gdr_agenda = QtGui.QWidget(self)

        self.lyt_agenda = QtGui.QGridLayout()

        # Set del layout della pagina
        self.gdr_agenda.setLayout(self.lyt_agenda)

        # Set del widget della pagina
        self.setCentralWidget(self.gdr_agenda)
