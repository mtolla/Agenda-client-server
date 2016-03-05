# -*- coding: utf-8 -*-
# Classe per la gestione delle notifiche
# Notifiche prestabilite: mezzora, un ora e il giorno prima
import requests


class ClassSignalQueue:
    def __init__(self, login_manager, db_manager):
        # Liste è un dizionario (act,user)
        self.modified_queue = []
        self.mod_error_queue = []
        self.activity_queue = []
        self.act_error_queue = []
        self.login_manager = login_manager
        self.db_manager = db_manager

    def add_to_modified(self, id_act):
        app_list = self.db_manager.get_users_from_activity(id_act)
        for item in app_list:
            item['action'] = "update"
            self.modified_queue.append(item)

    def add_to_activity(self, app_list):
        for item in app_list:
            item['action'] = "reminder"
            self.modified_queue.append(item)

    def check_activity(self):
        app_list = self.db_manager.check_activity()
        if app_list:
            self.add_to_activity(app_list)

    def clean_queue(self):
        pass

    # Id, nome/tempo che manca 24 = giorno,1 = ora,30 = minuti
    # Effettua 5 tentativi, al sesto mette la richiesta nella coda di errore
    def send(self):
        for user in self.modified_queue:
            try:
                requests.post(self.login_manager.from_user_get_ip(user['user']), data={user['act']})
            except Exception:
                if user['attempt'] < 5:
                    user['attempt'] += 1
                else:
                    self.mod_error_queue.append(user)

        for user in self.activity_queue:
            try:
                requests.post(self.login_manager.from_user_get_ip(user['user']), data={user['act']})
            except Exception:
                if user['attempt'] < 5:
                    user['attempt'] += 1
                else:
                    self.act_error_queue.append(user)

    # Funzione che dal login di un utente ritorno le cose che mancano
    def send_user_logged(self, id_user):
        list_return = []
        for user in range(0, len(self.mod_error_queue), 1):
            if self.mod_error_queue[user]['user'] == id_user:
                list_return.append(self.mod_error_queue.pop(user))
        for user in range(0, len(self.act_error_queue), 1):
            if self.act_error_queue[user]['user'] == id_user:
                list_return.append(self.act_error_queue.pop(user))
        return list_return
