# -*- coding: utf-8 -*-
import json
import sys
import datetime


class ClassDbManager:
    def __init__(self):
        # Dizionario del db
        self.db_file = {'user': sys.path[1] + '/database/user.json',
                        'project': sys.path[1] + '/database/project.json',
                        'location': sys.path[1] + '/database/location.json',
                        'group': sys.path[1] + '/database/group.json',
                        'activity': sys.path[1] + '/database/activity.json'}
        self.er = '<img src="https://goo.gl/'
        # Liste di dizionari ordinate con le attività di oggi e domani
        self.today_act = []
        self.tomorrow_act = []
        # Data di default, viene modificata al primo avvio di check_today_tomorrow_act()
        self.last_check = {'day': 12, 'month': 11, 'year': 1955, 'hour': 06, 'minute': 38}
        # Inizializzo login_manager

    def do_login(self, usr, psw):
        f = open(self.db_file['user'], "r")
        # Dizionario di appoggio
        list_app = json.load(f)
        for user in list_app:
            if user['username'] == usr and user['password'] == psw:
                return True
        return False

    def get_activity_from_id_act(self, id_att):
        # Da una id di una attività restituire gli attributi
        # Seleziono da activity l'attività con id passato
        # diz_cond : field, table, where
        f = open(self.db_file['activity'], "r")
        # Dizionario di appoggio
        list_app = json.load(f)
        for row in list_app:
            if row['ID'] == id_att:
                return row
        return False

    def get_participants_from_group(self, id_group):
        # Da una id di un gruppo restituire id partecipanti
        # Seleziono da utenti tutti quelli che tra i gruppi hanno quello passato
        f = open(self.db_file['user'], "r")
        # Dizionario di appoggio
        list_app = json.load(f)
        # Dizionario di ritorno
        list_return = []
        for row in list_app:
            for group in row['groups']:
                if group['ID'] == id_group:
                    list_return.append(row)
                    break
        return list_return

    def get_name_from_id_projects(self, list_id_proj):
        # Da una lista di id progetti restituire id e nome
        # Seleziono da progetti quelli che mi servono e li passo
        f = open(self.db_file['project'], "r")
        # Dizionario di appoggio
        list_app = json.load(f)
        # Dizionario di ritorno
        dict_return = dict()
        for proj in list_id_proj:
            for row in list_app:
                if row['ID'] == proj:
                    dict_return = {'ID': row['ID'], 'name': row['name']}
                    break
        return dict_return

    def get_proj_from_id_proj(self, id_proj):
        # Da id del progetto restituire tutto
        # Seleziono il progetto che mi serve e lo restituisco
        f = open(self.db_file['project'], "r")
        # Dizionario di appoggio
        list_app = json.load(f)
        for row in list_app:
            if row['ID'] == id_proj:
                return row
        return False

    def get_pjmanager_email(self, id_proj):
        # Da id del progetto restituisco la mail del project manager
        # Seleziono il progetto, ricavo id del PM, lo cerco tra gli utenti e restituisco la mail
        fproj = open(self.db_file['project'], "r")
        fuser = open(self.db_file['user'], "r")
        list_app_proj = json.load(fproj)
        list_app_user = json.load(fuser)
        app = 0
        for row in list_app_proj:
            if row['ID'] == id_proj:
                app = row['projectManager']
                break
        for row in list_app_user:
            if row['ID'] == app:
                return row['email']
        return False

    def is_teamleader(self, id_user):
        # Dall'user id trovo se è un teamleader
        # Ricevo l'ID dal login_manager e lo ricerco nel database utenti
        # Apro il file che mi serve
        f = open(self.db_file['user'], "r")
        list_app = json.load(f)
        for row in list_app:
            if row['ID'] == id_user:
                return self.is_teamleader_check(row)
        return False

    @staticmethod
    def is_teamleader_check(row):
        # Funzione di supporto per non far piangere sonarqube
        for group in row['groups']:
            if group['level'] == 'teamleader':
                return True
        return False

    def get_activities_from_proj(self, id_proj):
        # Da un id progetto trovo tutte le attività
        # Cerco in activity tutte quelle con id progetto uguale a quello richiesto
        f = open(self.db_file['activity'], "r")
        list_app = json.load(f)
        list_return = []
        for row in list_app:
            if row['project'] == id_proj:
                list_return.append(row)
        return list_return

    def get_holidays_from_proj(self, id_proj):
        # Da un id di un progetto restituisco tutte le vacanze degli utenti
        # Cerco l'id del gruppo dal progetto, lo confronto nella tabella user
        fproj = open(self.db_file['project'], "r")
        fuser = open(self.db_file['user'], "r")
        list_app_proj = json.load(fproj)
        list_app_user = json.load(fuser)
        dict_return = dict()
        app = 0
        for row in list_app_proj:
            if row['ID'] == id_proj:
                app = row['groups']
                break
        for row in list_app_user:
            for group in row['groups']:
                if group['ID'] == app:
                    dict_return[row['ID']] = row['holiday']
        return dict_return

    def get_group_name_from_group(self, id_group):
        # Da un id di un gruppo restituice il nome
        f = open(self.db_file['group'], "r")
        list_app = json.load(f)
        for row in list_app:
            if row['ID'] == id_group:
                return row['name']
        return False

    def get_users_from_activity(self, id_act):
        # Da una id di una attività restituire id, user, tentativi
        # Seleziono da activity l'attività con id passato
        # diz_cond : field, table, where
        f = open(self.db_file['activity'], "r")
        list_return = []
        dict_app = dict()
        # Lista di appoggio
        list_app = json.load(f)
        for row in list_app:
            if row['ID'] == id_act:
                for user in row['participants']:
                    dict_app['act'] = id_act
                    dict_app['user'] = user
                    list_return.append(dict_app)
                return list_return

    def check_activity(self):
        # Controllo tutte le attività e restituisco quelle con scadenza = 1 ora, 30 min, 24 ore
        actual_time = self.time_now()
        # Controllo scadenza ora e 30 min
        list_return = self.secondary_hour_check_activity(actual_time)
        list_app = self.secondary_day_check_activity(actual_time)
        list_return[len(list_app):] = list_app[:]
        return list_return

    def secondary_hour_check_activity(self, actual_time):
        list_return = []
        for act in self.today_act:
            # Controllo ora
            if act['date']['hour'] == actual_time['hour'] and act['date']['minute'] == actual_time['minute']:
                list_app = self.secondary_check_activity(act, 1)
                list_return[len(list_app):] = list_app[:]
            # Controllo 30 min
            # Se l'ora è la stessa basta controllare la differenza tra i minuti
            # Se l'ora è maggiore di uno controllo la differenza tra i minuti
            # ma quelli dell'attività vanno incrementati di 60
            if (act['date']['hour'] == actual_time['hour'] and (
                        act['date']['minute'] - actual_time['minute']) == 30) or (
                                act['date']['hour'] - 1 == actual_time['hour'] and (
                                    act['date']['minute'] + 60 - actual_time['minute']) == 30):
                list_app = self.secondary_check_activity(act, 30)
                list_return[len(list_app):] = list_app[:]
        return list_return

    def secondary_day_check_activity(self, actual_time):
        list_return = []
        # Controllo scadenza 24 h
        for act in self.tomorrow_act:
            if act['date']['hour'] == actual_time['hour'] and act['date']['minute'] == actual_time['minute']:
                list_app = self.secondary_check_activity(act, 24)
                list_return[len(list_app):] = list_app[:]
        return list_return

    def secondary_check_activity(self, act, time):
        dict_app = dict()
        list_return = []
        list_app = self.get_users_from_activity(act)
        for user in list_app:
            dict_app['act'] = user['act']
            dict_app['user'] = user['user']
            dict_app['attempt'] = 1
            dict_app['date'] = time
            list_return.append(dict_app)
        return list_return

    def check_today_tomorrow_act(self):
        # Controllo tutte le attività di oggi e domani
        f = open(self.db_file['activity'], "r")
        # Lista di appoggio
        list_app = json.load(f)
        # Orario attuale
        actual_time = self.time_now()
        # Se l'ultima volta che è stato aggiornato è oggi non esegue il controllo
        if self.last_check['day'] == actual_time['day'] or self.last_check['month'] == actual_time['month'] or \
                        self.last_check['hour'] == actual_time['hour']:
            return
        for row in list_app:
            if row['date']['year'] == actual_time['year'] and row['date']['month'] == actual_time['month']:
                if row['date']['day'] == actual_time['day']:
                    dict_app = {row['ID']: row['date']}
                    self.insert_to_today_act(dict_app)
                # +1 per il giorno dopo
                if row['date']['day'] == actual_time['day'] + 1:
                    dict_app = {row['ID']: row['date']}
                    self.insert_to_tom_act(dict_app)
        self.last_check = actual_time

    def insert_to_today_act(self, item):
        app_list = []
        if not self.today_act:
            return self.today_act.append(item)
        for act in range(0, len(self.today_act)):
            if self.today_act[act]['date']['hour'] < item['hour']:
                app_list.append(self.today_act[act])
            if self.today_act[act]['date']['hour'] == item['hour']:
                if self.today_act[act]['date']['minute'] < item['minute']:
                    app_list.append(self.today_act[act])
                if self.today_act[act]['date']['minute'] >= item['minute']:
                    app_list.append(item)
                    app_list[act + 1:] = self.today_act[act:]
            if self.today_act[act]['date']['hour'] > item['hour']:
                app_list.append(item)
                app_list[act + 1:] = self.today_act[act:]
        self.today_act = app_list

    def insert_to_tom_act(self, item):
        app_list = []
        if not self.tomorrow_act:
            return self.tomorrow_act.append(item)
        for act in range(0, len(self.tomorrow_act)):
            if self.tomorrow_act[act]['date']['hour'] < item['hour']:
                app_list.append(self.tomorrow_act[act])
            if self.tomorrow_act[act]['date']['hour'] == item['hour']:
                if self.tomorrow_act[act]['date']['minute'] < item['minute']:
                    app_list.append(self.tomorrow_act[act])
                if self.tomorrow_act[act]['date']['minute'] >= item['minute']:
                    app_list.append(item)
                    app_list[act + 1:] = self.tomorrow_act[act:]
                    break
            if self.tomorrow_act[act]['date']['hour'] > item['hour']:
                app_list.append(item)
                app_list[act + 1:] = self.tomorrow_act[act:]
                break
        self.tomorrow_act = app_list

    def from_user_get_id(self, user):
        # Dal nome utente restituisco id
        f = open(self.db_file['user'], "r")
        list_app = json.load(f)
        for row in list_app:
            if row['username'] == user:
                return row['ID']
        return False

    def error(self, app):
        if app:
            return self.er + '5UL9yj">'
        else:
            return self.er + 'dmr6pW">'

    @staticmethod
    def time_now():
        # Ricevo la data di oggi
        app = datetime.datetime.today()
        # Assegno i valori alla lista actual_time
        actual_time = dict()
        actual_time['day'] = int(app.strftime("%d"))
        actual_time['month'] = int(app.strftime("%m"))
        actual_time['year'] = int(app.strftime("%Y"))
        actual_time['hour'] = int(app.strftime("%H"))
        actual_time['minute'] = int(app.strftime("%M"))
        return actual_time
