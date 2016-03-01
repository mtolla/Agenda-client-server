# Classe per la gestione delle notifiche
# Notifiche prestabilite: mezzora, un ora e il giorno prima
import requests


class ClassSignalQueue:
    def __init__(self, login_manager, db_manager):
        # Liste = dict(act,user)
        self.modified_queue = []
        self.mod_error_queue = []
        self.activity_queue = []
        self.act_error_queue = []
        self.loginManager = login_manager
        self.dbManager = db_manager

    def add_to_modified(self, id_act):
        app_list = self.dbManager(id_act)
        for item in app_list:
            self.modified_queue.append(item)

    def add_to_activity(self, id_act):
        app_list = self.dbManager(id_act)
        for item in app_list:
            self.modified_queue.append(item)

    def check_activity(self):

        pass

    def send(self):
        # Scansiono ogni lista, cerco indirizzi ip e invio
        for user in self.mod_error_queue:
            if requests.post(self.loginManager.from_user_get_ip(user['user']), data={user['act']}):
                self.mod_error_queue.remove(user)

        for user in self.modified_queue:
            if not requests.post(self.loginManager.from_user_get_ip(user['user']), data={user['act']}):
                self.mod_error_queue.append(user)

        for user in self.act_error_queue:
            if not requests.post(self.loginManager.from_user_get_ip(user['user']), data={user['act']}):
                self.act_error_queue.remove(user)

        for user in self.activity_queue:
            if not requests.post(self.loginManager.from_user_get_ip(user['user']), data={user['act']}):
                self.activity_queue.append(user)


