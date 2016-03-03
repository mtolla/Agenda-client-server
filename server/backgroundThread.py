# -*- coding: utf-8 -*-
# Librerie underground Task
from PyQt4 import QtCore
import time


# Classe Thread controllo token
class TokenThread(QtCore.QRunnable):
    def __init__(self, login_manager):
        QtCore.QRunnable.__init__(self)
        self.login_manager = login_manager

    def run(self):
        while True:
            self.login_manager.check_life_token()
            time.sleep(self.login_manager.next_token_expire())


# Classe Thread controllo della Queue
class SignalThread(QtCore.QRunnable):
    def __init__(self, signal_queue):
        QtCore.QRunnable.__init__(self)
        self.sleep_time = 60  # 1 Minuti
        self.signal_queue = signal_queue

    def run(self):
        while True:
            self.signal_queue.check_activity()
            self.signal_queue.send()
            self.signal_queue.clean_queue()
            time.sleep(self.sleep_time)

