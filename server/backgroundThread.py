# Librerie underground Task
from PyQt4 import QtCore
import time
# Importo loginManager
from loginManager import ClassLoginManager


# Classe Thread controllo token
class TokenThread(QtCore.QRunnable):
    def __init__(self, loginManager):
        QtCore.QRunnable.__init__(self)
        self.sleep_time = 360  # 10 Minuti
        self.loginManager = loginManager

    def run(self):
        while True:
            self.loginManager.check_life_token()
            time.sleep(self.sleep_time)


class SignalThread(QtCore.QRunnable):
    def __init__(self, signal_queue):
        QtCore.QRunnable.__init__(self)
        self.sleep_time = 60  # 1 Minuti
        self.signalQueue = signal_queue

    def run(self):
        while True:
            self.signalQueue.check_activity()
            self.signalQueue.send()
            time.sleep(self.sleep_time)

