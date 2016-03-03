# -*- coding: utf-8 -*-
# Importo librerie

# Importo db_manager
from dbManager import ClassDbManager
# Importo login_manager
from loginManager import ClassLoginManager
# Importo backgroundThread
from PyQt4 import QtCore
import json  # DA ELIMINARE FINITI I TEST
# Thread
from backgroundThread import TokenThread, SignalThread
# Notification Queue
from signalQueue import ClassSignalQueue


class Api:
    def __init__(self):
        # Creazione oggetti db,login Manager
        self.db_manager = ClassDbManager()
        self.login_manager = ClassLoginManager()
        # Creazione thread controllo token
        token_thread = TokenThread(self.login_manager)
        QtCore.QThreadPool.globalInstance().start(token_thread)
        # Creazione gestione coda notifiche
        self.signal_queue = ClassSignalQueue(self.login_manager, self.db_manager)
        # Creazione thread controllo queue
        signal_thread = SignalThread(self.signal_queue)
        QtCore.QThreadPool.globalInstance().start(signal_thread)

    # Login con user, password
    def do_login(self, user, password, ip):
        # if self.valid_credentials(user, password):
        return self.login_manager.do_login(user, password, ip)

    # Login con token
    def do_login_token(self, token, ip, ):
        if self.login_manager.do_login_token(token, ip):
            return "OK", 200
        else:
            return "Unauthorized", 401

    def badass_function(self, token, id_proj):
        # Dato token e id progetto restituire:
        #   - L'oggetto del progetto
        #   - eMail project manager
        #   - T/F se è almeno teamleader in un gruppo
        #   - Tutte attività del progetto dell'utente (attività da singolo(group = NULL))
        #   - Vacanze del progetto
        # Dizionario di ritorno
        dict_return = dict()
        dict_return['project'] = self.get_project(id_proj)
        dict_return['email'] = self.get_pjmanager_mail(id_proj)
        dict_return['isteamleader'] = self.get_is_teamleader(token)
        dict_return['activities'] = self.get_activities_project(id_proj)
        dict_return['holidays'] = self.get_holidays_proj(id_proj)
        return dict_return

    def get_activity(self, id_att):
        # Dato id attività restituire:
        #   - Attività
        #   - Gruppo se è un attività di gruppo
        dict_return = dict()
        dict_return['activity'] = self.db_manager.get_activity_from_id_act(id_att)
        dict_return['group'] = self.db_manager.get_group_name_from_group(dict_return['activity']['group'])
        return dict_return

    def get_partecipants_group(self, id_group):
        return self.db_manager.get_participants_from_group(id_group)

    def get_name_projects(self, list_id_proj):
        return self.db_manager.get_name_from_id_projects(list_id_proj)

    def get_project(self, id_proj):
        return self.db_manager.get_proj_from_id_proj(id_proj)

    def get_pjmanager_mail(self, id_proj):
        return self.db_manager.get_pjmanager_email(id_proj)

    def get_is_teamleader(self, token):
        id_user = self.login_manager.from_token_get_user(token)
        return self.db_manager.is_teamleader(id_user)

    def get_activities_project(self, id_proj):
        return self.db_manager.get_activities_from_proj(id_proj)

    def get_holidays_proj(self, id_proj):
        return self.db_manager.get_holidays_from_proj(id_proj)

    def get_group_name(self, id_group):
        return self.db_manager.get_group_name_from_group(id_group)

    def error(self, app):
        return self.db_manager.error(app)

    def test(self):
        return json.dumps(self.login_manager.user_token)
