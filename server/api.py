# -*- coding: utf-8 -*-
# Importo librerie

# Importo db_manager
from dbManager import ClassDbManager
# Importo db_manager helper
from dbHelper import ClassDbHelper
# Importo login_manager
from loginManager import ClassLoginManager
# Importo backgroundThread
from PyQt4 import QtCore
import json  # DA ELIMINARE FINITI I TEST
# Thread
from backgroundThread import TokenThread, SignalThread, JournalThread
# Notification Queue
from signalQueue import ClassSignalQueue


class Api:
    def __init__(self):
        # Creazione oggetti db,login Manager
        self.db_manager = ClassDbManager()
        self.db_helper = ClassDbHelper(self.db_manager)
        self.login_manager = ClassLoginManager()
        # Creazione thread controllo token
        token_thread = TokenThread(self.login_manager, self.db_manager)
        QtCore.QThreadPool.globalInstance().start(token_thread)
        # Creazione gestione coda notifiche
        self.signal_queue = ClassSignalQueue(self.login_manager, self.db_manager)
        # Creazione thread controllo queue
        signal_thread = SignalThread(self.signal_queue)
        QtCore.QThreadPool.globalInstance().start(signal_thread)
        # Creazione thread giornaliero
        journal_thread = JournalThread(self.db_manager)
        QtCore.QThreadPool.globalInstance().start(journal_thread)

    ####################################################################################################################

    # Login con user, password
    def do_login(self, user, password, ip):
        token = self.login_manager.do_login(user, password, ip)
        list_app = self.signal_queue.send_user_logged(self.login_manager.from_token_get_user(token))
        list_return = [token, list_app]
        return json.dumps(list_return)

    # Login con token
    def do_login_token(self, token, ip):
        if self.login_manager.do_login_token(token, ip):
            list_return = self.signal_queue.send_user_logged(self.login_manager.from_token_get_user(token))
            return json.dumps(list_return)
        else:
            return "Unauthorized", 401

    def do_logout(self, token):
        return self.login_manager.delete_token(False, token)

    def home(self):
        return self.db_manager.home()

    def error(self, app):
        return self.db_manager.error(app)

    def omg_tolla(self):
        return self.db_manager.omg_tolla()

    # Query
    def project(self, token, id_proj):
        # Dato token e id progetto restituire:
        #   - L'oggetto del progetto
        #   - eMail project manager
        #   - T/F se è almeno teamleader in un gruppo
        #   - Tutte attività del progetto dell'utente di oggi (attività da singolo(group = NULL))
        #   - Vacanze del progetto
        # Dizionario di ritorno
        dict_return = dict()
        dict_return['project'] = self.db_manager.get_proj_from_id_proj(id_proj)
        dict_return['email'] = self.db_manager.get_pjmanager_email(id_proj)
        dict_return['activities'] = self.db_manager.get_today_activities_from_proj(id_proj)
        dict_return['holidays'] = self.db_manager.get_holidays_from_proj(id_proj)
        dict_return['level'] = self.get_level_usr(token)
        dict_return['user'] = self.db_manager.get_user_name(self.from_token_get_iduser(token))
        return json.dumps(dict_return)

    def get_holidays_day(self, id_proj, day, month, year):
        dict_app = {'day': day, 'month': month, 'year': year}
        return json.dumps(self.db_manager.get_holidays_from_proj(id_proj, dict_app))

    def get_user_project(self, token):
        return json.dumps(self.db_manager.get_proj_from_user(self.login_manager.from_token_get_iduser(token)))

    def get_activity_day(self, id_proj, day, month, year):
        dict_app = {'day': day, 'month': month, 'year': year}
        return json.dumps(self.db_manager.get_activity_day(id_proj, dict_app))

    def get_activity_info(self, id_act, token):
        return json.dumps(self.db_manager.get_activity_info(id_act, self.from_token_get_iduser(token)))

    def get_locations(self):
        return json.dumps(self.db_manager.get_locations())

    def get_teamleader_groups(self, id_proj, token):
        return json.dumps(self.db_manager.get_teamleader_groups(id_proj, self.from_token_get_iduser(token)))

    def get_participants_from_group(self, id_group):
        return json.dumps(self.db_manager.get_participants_from_group(id_group))

    def get_participants_from_proj(self, id_proj):
        return json.dumps(self.db_manager.get_participants_from_proj(id_proj))

    def get_participants_name_lvl_group(self, id_group):
        return json.dumps(self.db_manager.get_participants_name_lvl_group(id_group))

    def get_not_participants_from_proj(self, id_proj):
        return json.dumps(self.db_manager.get_not_participants_from_proj(id_proj))

    def everybody(self, id_proj):
        return json.dumps(self.db_manager.everybody(id_proj))

    def user_father_group(self, id_group):
        return json.dumps(self.db_manager.user_father_group(id_group))

    def user_holiday(self, id_usr):
        return json.dumps(self.db_manager.user_holiday(id_usr))

    def get_level_usr(self, token):
        if self.get_is_projectmanager(token):
            return "projectmanager"
        if self.get_is_teamleader(token):
            return "teamleader"
        return "participant"

    def get_is_projectmanager(self, token):
        return self.db_manager.is_projectmanager(self.login_manager.from_token_get_iduser(token))

    def get_is_teamleader(self, token):
        return self.db_manager.is_teamleader(self.login_manager.from_token_get_iduser(token))

    def from_token_get_iduser(self, token):
        return self.login_manager.from_token_get_iduser(token)

    def check_token(self, token, ip):
        return self.login_manager.check_token(token, ip)

    def insert_activity(self, activity):
        return self.db_helper.insert_activity(json.loads(activity))

    def insert_holiday(self, holiday, token):
        return self.db_helper.insert_holiday(json.loads(holiday), self.from_token_get_iduser(token))

    def modify_activity(self, old, new):
        return self.db_helper.modify_act(old, new)
    
    def modify_holiday(self, old, new):
        return self.db_helper.modify_hol(old, new)
    
    def modify_group(self, new):
        return self.db_helper.modify_group(new)
    
    def modify_level(self, id_usr, id_group, level):
        return self.db_helper.modify_level(id_usr, id_group, level)
    
    def modify_project(self, new):
        return self.db_helper.modify_proj(new)
    
    def delete_activity(self, id):
        return self.db_helper.delete_act(id)

    def delete_holiday(self, id):
        return self.db_helper.delete_hol(id)

    def delete_group(self, id):
        return self.db_helper.delete_group(id)

    def delete_project(self, id):
        return self.db_helper.delete_proj(id)

    def create_group(self, group, token, list_id_usr):
        id_usr = self.from_token_get_iduser(token)
        self.db_helper.create_group(group, id_usr, list_id_usr)
        return True

    def create_project(self, project, group, list_id_usr, token):
        id_usr = self.from_token_get_iduser(token)
        self.db_helper.create_project(project, group, list_id_usr, id_usr)
        return True

        