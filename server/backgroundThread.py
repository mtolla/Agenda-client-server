# -*- coding: utf-8 -*-
# Librerie underground Task
from PyQt4 import QtCore
import time


# Classe Thread controllo token
class TokenThread(QtCore.QRunnable):
    def __init__(self, login_manager, db_manager):
        QtCore.QRunnable.__init__(self)
        self.login_manager = login_manager
        self.db_manager = db_manager

    def run(self):
        while True:
            actual_time = self.db_manager.time_now()
            self.login_manager.check_life_token(actual_time)
            time.sleep(self.how_much_i_can_sleep())
            # time.sleep(152354)

    def how_much_i_can_sleep(self):
        if not self.login_manager.user_token:
            return 5
        next_exp = self.login_manager.next_token_expire()
        actual_time = self.db_manager.time_now()
        sleep_time = 0
        if next_exp['hour'] - actual_time['hour'] < 0:
            return self.i_can_sleep_until_midnight()
        else:
            if next_exp['hour'] - actual_time['hour'] == 0:
                sleep_time = 23 * 3600
            else:
                sleep_time += (next_exp['hour'] - actual_time['hour']) * 3600
            if next_exp['minute'] - actual_time['minute'] < 0:
                return sleep_time
            sleep_time += (next_exp['minute'] - actual_time['minute']) * 60
            return sleep_time

    def i_can_sleep_until_midnight(self):
        actual_time = self.db_manager.time_now()
        sleep_time = (24 - actual_time['hour']) * 3600
        sleep_time += (60 - actual_time['minute']) * 60
        return sleep_time


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

# Classe Thread, lavora giornalmente
class JournalThread(QtCore.QRunnable):
    def __init__(self, db_manager):
        QtCore.QRunnable.__init__(self)
        self.db_manager = db_manager

    def run(self):
        while True:
            self.db_manager.check_today_tomorrow_act()
            time.sleep(self.i_can_sleep_until_midnight())

    def i_can_sleep_until_midnight(self):
        actual_time = self.db_manager.time_now()
        sleep_time = (24 - actual_time['hour']) * 3600
        sleep_time += (60 - actual_time['minute']) * 60
        return sleep_time
