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

    def do_login(self, usr, psw):
        # Dizionario di appoggio
        list_app = self.open_file('user')
        for user in list_app:
            if user['username'] == usr and user['password'] == psw:
                return True
        return False

    def get_activity_from_id_act(self, id_att):
        # Da una id di una attività restituire gli attributi
        # Seleziono da activity l'attività con id passato
        # diz_cond : field, table, where
        # Dizionario di appoggio
        list_app = self.open_file('activity')
        for row in list_app:
            if row['ID'] == id_att:
                return row
        return False

    def get_participants_from_group(self, id_group):
        # Da una id di un gruppo restituire id partecipanti
        # Seleziono da utenti tutti quelli che tra i gruppi hanno quello passato
        # Dizionario di appoggio
        list_app = self.open_file('user')
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
        # Dizionario di appoggio
        list_app = self.open_file('project')
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
        # Dizionario di appoggio
        list_app = self.open_file('project')
        for row in list_app:
            if row['ID'] == id_proj:
                return row
        return False

    def get_pjmanager_email(self, id_proj):
        # Da id del progetto restituisco la mail del project manager
        # Seleziono il progetto, ricavo id del PM, lo cerco tra gli utenti e restituisco la mail
        list_app_proj = self.open_file('project')
        list_app_user = self.open_file('user')
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
        list_app = self.open_file('user')
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

    def is_projectmanager(self, id_user):
        # Dall'user id trovo se è un project manager
        list_app = self.open_file('project')
        for row in list_app:
            if row['projectManager'] == id_user:
                return True
        return False

    def get_activities_from_proj(self, id_proj):
        # Da un id progetto trovo tutte le attività
        # Cerco in activity tutte quelle con id progetto uguale a quello richiesto
        # ID, nome, inizio, fine con ora e minuti delle attività di oggi e nome della stanza
        dict_app = dict()
        hour_app = dict()
        list_return = []
        for row in self.today_act:
            if row['project'] == id_proj:
                dict_app['ID'] = row['ID']
                dict_app['name'] = row['name']
                dict_app['begin'] = {'hour': row['date']['hour'], 'minute': row['date']['minute']}
                hour_app = self.calc_duration(row['date'], row['duration'])
                dict_app['end'] = {'hour': hour_app['hour'], 'minute': hour_app['minute']}
                dict_app['room'] = self.get_room_from_id(dict_app['room'])
                list_return.append(row)
        return list_return

    def get_holidays_from_proj(self, id_proj):
        # Da un id di un progetto restituisco tutte le vacanze degli utenti
        # Cerco l'id del gruppo dal progetto, lo confronto nella tabella user
        list_app_proj = self.open_file('project')
        list_app_user = self.open_file('user')
        dict_return = dict()
        app = 0
        for row in list_app_proj:
            if row['ID'] == id_proj:
                app = row['group']
                break
        for row in list_app_user:
            for group in row['groups']:
                if group['ID'] == app:
                    dict_return[row['ID']] = row['holiday']
        return dict_return

    def get_group_name_from_group(self, id_group):
        # Da un id di un gruppo restituice il nome
        list_app = self.open_file('group')
        for row in list_app:
            if row['ID'] == id_group:
                return row['name']
        return False

    def get_users_from_activity(self, id_act):
        # Da una id di una attività restituire id, user, tentativi
        # Seleziono da activity l'attività con id passato
        # diz_cond : field, table, where
        list_app = self.open_file('activity')
        list_return = []
        dict_app = dict()
        for row in list_app:
            if row['ID'] == id_act:
                for user in row['participants']:
                    dict_app['act'] = id_act
                    dict_app['user'] = user
                    list_return.append(dict_app)
                return list_return
        return False

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
        # Lista di appoggio
        list_app = self.open_file('activity')
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
        list_app = self.open_file('user')
        for row in list_app:
            if row['username'] == user:
                return row['ID']
        return False

    def from_id_get_user(self, id_user):
        # Dal nome utente restituisco id
        list_app = self.open_file('user')
        for row in list_app:
            if row['ID'] == id_user:
                return row['username']
        return False

    def get_proj_from_user(self, id_usr):
        # Prendo tutti i gruppi dell'utente e li confronto con quelli dei progetti
        list_usr = self.open_file('user')
        list_proj = self.open_file('project')
        # Lista di appoggio
        list_app = []
        dict_return = dict()
        for user in list_usr:
            if user['ID'] == id_usr:
                for group in user['groups']:
                    list_app.append(group['ID'])
                break
        for proj in list_proj:
            if proj['group'] in list_app:
                dict_return[proj['ID']] = proj['name']
        return dict_return

        # [i for i in L1 if i in L2]
        # if [i for i in proj['group'] if i in list_app]:

    def calc_duration(self, dict_hour, duration):
        # Funzione che data una data calcola la durata
        # Calcolo della durata in ore con resto
        rest = duration % 60
        n_hour = duration / 60
        dict_hour['hour'] += n_hour
        dict_hour['minutes'] += rest
        return dict_hour

    def get_room_from_id(self, id_room):
        # Dall'id di una stanza restituisco il nome
        list_app = self.open_file('location')
        app_return = ""
        for room in list_app:
            if room['ID'] == id_room:
                app_return += room['building'] + "-" + room['room']
                return app_return
        return False








    def open_file(self, namefile, method = "r"):
        try:
            f = open(self.db_file[namefile], method)
        except IOError:
            return False
        else:
            return json.load(f)



























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
        actual_time['seconds'] = int(app.strftime("%S"))
        return actual_time
