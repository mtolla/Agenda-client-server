from popup import *


class Page(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle('ManageIT')
        self.setWindowIcon(QtGui.QIcon(MANAGE_IT))

        # ------------------------------------- Menu bar -------------------------------------

        close = QtGui.QAction(QtGui.QIcon(QUIT), "Quit", self)
        close.setShortcut("Ctrl+Q")
        close.setStatusTip("Close application")
        self.connect(close, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

        sep = QtGui.QAction(self)
        sep.setSeparator(True)

        info = QtGui.QAction(QtGui.QIcon(INFO), "About", self)
        info.setShortcut("Ctrl+I")
        info.setStatusTip("Show information")
        self.connect(info, QtCore.SIGNAL('triggered()'), self.about)

        self.statusBar().show()

        menu = self.menuBar()
        self.m_file = menu.addMenu('&File')
        self.m_file.addAction(close)
        self.m_file.addAction(sep)
        self.m_file.addAction(info)

    @staticmethod
    def about():
        Popup("Copyright 2016 @ TeamIT").exec_()
