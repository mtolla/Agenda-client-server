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
from backgroundThread import TokenThread, SignalThread, JournalThread
# Notification Queue
from signalQueue import ClassSignalQueue


class Api:
    def __init__(self):
        # Creazione oggetti db,login Manager
        self.db_manager = ClassDbManager()
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
    # Login con user, password
    def do_login(self, user, password, ip):
        token = self.login_manager.do_login(user, password, ip)
        list_app = self.signal_queue.send_user_logged(self.login_manager.from_token_get_user(token))
        list_return = [token, list_app]
        return json.dumps(list_return)

    # Login con token
    def do_login_token(self, token, ip, ):
        if self.login_manager.do_login_token(token, ip):
            list_return = self.signal_queue.send_user_logged(self.login_manager.from_token_get_user(token))
            return json.dumps(list_return)
        else:
            return "Unauthorized", 401

    ####################################################################################################################
    # Query
    def badass_function(self, token, id_proj):
        # Dato token e id progetto restituire:
        #   - L'oggetto del progetto
        #   - eMail project manager
        #   - T/F se è almeno teamleader in un gruppo
        #   - Tutte attività del progetto dell'utente di oggi (attività da singolo(group = NULL))
        #   - Vacanze del progetto
        # Dizionario di ritorno
        dict_return = dict()
        dict_return['project'] = self.get_project(id_proj)
        dict_return['email'] = self.get_pjmanager_mail(id_proj)
        dict_return['activities'] = self.get_activities_project_today(id_proj)
        dict_return['holidays'] = self.get_holidays_proj(id_proj)
        dict_return['level'] = self.get_level_usr(token)
        return json.dumps(dict_return)

    def get_activity(self, id_att):
        # Dato id attività restituire:
        #   - Attività
        #   - Gruppo se è un attività di gruppo
        dict_return = dict()
        dict_return['activity'] = self.get_activity_from_id_act(id_att)
        dict_return['group'] = self.get_group_name_from_group(dict_return['activity']['group'])
        return json.dumps(dict_return)


    def get_name_projects(self, list_id_proj):
        return self.db_manager.get_name_from_id_projects(list_id_proj)

    def get_project(self, id_proj):
        return self.db_manager.get_proj_from_id_proj(id_proj)

    def get_pjmanager_mail(self, id_proj):
        return self.db_manager.get_pjmanager_email(id_proj)

    def get_is_teamleader(self, token):
        id_user = self.login_manager.from_token_get_iduser(token)
        return self.db_manager.is_teamleader(id_user)

    def get_is_projectmanager(self, token):
        id_user = self.login_manager.from_token_get_iduser(token)
        return self.db_manager.is_projectmanager(id_user)

    def get_level_usr(self, token):
        if self.get_is_projectmanager(token):
            return "projectmanager"
        if self.get_is_teamleader(token):
            return "teamleader"
        return "participant"

    def get_activities_project_today(self, id_proj):
        return self.db_manager.get_today_activities_from_proj(id_proj)

    def get_holidays_proj(self, id_proj):
        return self.db_manager.get_holidays_from_proj(id_proj)

    def get_group_name(self, id_group):
        return self.db_manager.get_group_name_from_group(id_group)

    def error(self, app):
        return self.db_manager.error(app)

    def test(self):
        return json.dumps(self.login_manager.user_token)

    def get_user_project(self, token):
        return json.dumps(self.db_manager.get_proj_from_user(self.login_manager.from_token_get_iduser(token)))

    def check_token(self, token, ip):
        return self.login_manager.check_token(token, ip)

    def get_activity_day(self, day, month, year):
        dict_app = {'day': day, 'month': month, 'year': year}
        return json.dumps(self.db_manager.get_activity_day(dict_app))

    def get_activity_info(self, id_act, token):
         return json.dumps(self.db_manager.get_activity_info(id_act, self.from_token_get_iduser(token)))

    def get_locations(self):
        return json.dumps(self.db_manager.get_locations())

    def get_teamleader_groups(self, token):
        return json.dumps(self.db_manager.get_teamleader_groups(self.from_token_get_iduser(token)))

    def get_participants_from_proj(self, id_proj):
        return json.dumps(self.db_manager.get_participants_from_proj(id_proj))

    def get_not_participants_from_proj(self, id_proj):
        return json.dumps(self.db_manager.get_not_participants_from_proj(id_proj))

    def get_partecipants_name_lvl_from_group(self, id_group):
        return json.dumps(self.db_manager.get_partecipants_name_lvl_from_group(id_group))

    def everybody(self):
        return json.dumps(self.db_manager.everybody())

    def user_father_group(self, id_group):
        return json.dumps(self.db_manager.user_father_group(id_group))

    def user_holiday(self, id_usr):
        return json.dumps(self.db_manager.user_holiday(id_usr))



















    # Implementazioni per test, se non serviranno più eliminare pure

    def delete_token(self, app, login_app):
        return self.login_manager.delete_token(app, login_app)

    def from_token_get_user(self, token):
        return self.login_manager.from_token_get_user(token)

    def from_token_get_iduser(self, token):
        return self.login_manager.from_token_get_iduser(token)

    def get_activity_from_id_act(self, id_act):
        return self.db_manager.get_activity_from_id_act(id_act)

    def get_participants_from_group(self, id_group):
        return json.dumps(self.db_manager.get_participants_from_group(id_group))

    def get_name_from_id_projects(self, id_proj):
        return self.db_manager.get_name_from_id_projects(id_proj)

    def get_proj_from_id_proj(self, id_proj):
        return self.db_manager.get_proj_from_id_proj(id_proj)

    def get_pjmanager_email(self, id_proj):
        return self.db_manager.get_pjmanager_email(id_proj)

    def is_teamleader(self, id_group):
        return self.db_manager.is_teamleader(id_group)

    def get_holidays_from_proj(self, id_proj):
        return self.db_manager.get_holidays_from_proj(id_proj)

    def get_group_name_from_group(self, id_group):
        return self.db_manager.get_group_name_from_group(id_group)

    def get_proj_from_user(self, id_user):
        return self.db_manager.get_proj_from_user(id_user)

    def get_user_token(self):
        return self.login_manager.user_token
