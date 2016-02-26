from PyQt4 import QtGui, QtCore
from icon.icon import *


class Popup(QtGui.QDialog):
    def __init__(self, message, icon=False):
        QtGui.QDialog.__init__(self)

        self.setWindowTitle('ManageIT')
        self.setWindowIcon(QtGui.QIcon(MANAGE_IT))
        self.setStyleSheet(
            '''
                * {
                    font-size: 15px;
                }
            '''
        )

        # Creazione della pagina e del suo layout: hrz_page(lyt_page)
        self.hrz_page = QtGui.QWidget(self)

        self.lyt_page = QtGui.QHBoxLayout()

        # Definizione dell'oggetto ico
        if icon:
            self.ico = QtGui.QLabel(self)
            self.ico.setPixmap(QtGui.QIcon(icon).pixmap(QtCore.QSize(24, 24)))

        # Definizione dell'oggetto lbl_about
        self.lbl_about = QtGui.QLabel(message, self)

        # Aggiunta del'icon e del lbl_about nel hrz_page
        if icon:
            self.lyt_page.addWidget(self.ico)
        self.lyt_page.addWidget(self.lbl_about)

        # Set del layout della pagina
        self.setLayout(self.lyt_page)
