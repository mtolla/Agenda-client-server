# -*- coding: utf-8 -*-
import json
import sys
import ast


class ClassDbManager:
    def __init__(self):
        # Dizionario del db
        self.db_file = {'user': sys.path[1] + '/database/user.json',
                   'project': sys.path[1] + '/database/project.json',
                   'location': sys.path[1] + '/database/location.json',
                   'group': sys.path[1] + '/database/group.json',
                   'activity': sys.path[1] + '/database/activity.json'}
        # Inizializzo loginManager


    def do_login(self, usr, psw):
        f = open(self.db_file['user'], "r")
        # Dizionario di appoggio
        list_app = json.load(f)
        for user in list_app:
            if user['username'] == usr and user['password'] == psw:
                return True
        return False

    def get_attributes_from_activity(self, id_att):
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

    def get_name_from_id_projects(self, id_proj):
        # Da una lista di id progetti restituire id e nome
        # Seleziono da progetti quelli che mi servono e li passo
        f = open(self.db_file['project'], "r")
        # Dizionario di appoggio
        list_app = json.load(f)
        # Dizionario di ritorno
        dict_return = dict()
        for proj in id_proj:
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
                print ("ciao")
                return row['email']
        return False

    def is_teamleader(self, id_user):
        # Dall'user id trovo se è un teamleader
        # Ricevo l'ID dal loginManager e lo ricerco nel database utenti
        # Apro il file che mi serve
        f = open(self.db_file['user'], "r")
        list_app = json.load(f)
        for row in list_app:
            if row['ID'] == id_user:
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

    def get_activities_from_id_act(self, id_act):
        # Da un id di una attività restituisco l'attività
        # Cerco in activity quella richiesta
        f = open(self.db_file['activity'], "r")
        list_app = json.load(f)
        for row in list_app:
            if row['ID'] == id_act:
                return row
        return False

    def get_holydays_from_proj(self, id_proj):
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
            for group in row ['groups']:
                if group == app:
                    dict_return[row['ID']] = row['holydays']
        return dict_return

    def get_group_name_from_group(self, id_group):
        f = open(self.db_file['group'], "r")
        list_app = json.load(f)
        for row in list_app:
            if row['ID'] == id_group:
                return row['name']
        return False


