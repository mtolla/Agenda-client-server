from PyQt4 import QtGui


class Popup(QtGui.QDialog):
    def __init__(self, message):
        QtGui.QDialog.__init__(self)

        self.setWindowTitle('ManageIT')
        self.setWindowIcon(QtGui.QIcon("./icon/ManageIT.png"))
        self.setStyleSheet(
            '''
                * {
                    font-size: 15px;
                }
            '''
        )

        # Creazione della pagina e del suo layout: vrt_page(lyt_page)
        self.vrt_page = QtGui.QWidget(self)

        self.lyt_page = QtGui.QVBoxLayout()

        # Definizione dell'oggetto lbl_about
        self.lbl_about = QtGui.QLabel(message, self)

        # Aggiungiamo il contenitore e il scrlMappa nel vrt_page
        self.lyt_page.addWidget(self.lbl_about)

        # Settiamo il widget della pagina
        self.setLayout(self.lyt_page)
