# -*- coding: utf-8 -*-
import json
import sys


class ClassDbManager:
    def __init__(self):
        # Dizionario del db
        self.db_file = {'user': sys.path[1] + '/database/user.json',
                   'project': sys.path[1] + '/database/project.json',
                   'location': sys.path[1] + '/database/location.json',
                   'group': sys.path[1] + '/database/group.json',
                   'activity': sys.path[1] + '/database/activity.json'}
        # Legge il file utenti.json
        login_file = open("../Database/user.json", "r")
        # Lo trasforma in un dizionario
        self.login_dict = json.loads(login_file)


    def dologin(self, usr, psw):
        for user in self.login_dict.iteritems():
            if user['id'] == usr and user['password'] == psw:
                return True
            else:
                return False

    def select(self, diz_cond):
        # Select * from table where cond
        # diz_cond : field, table, where

        f = open(self.db_file[diz_cond['table']], "r")
        diz_app = json.loads(f)
        #for row in diz_app:
            #if eval(diz_cond['where']):







    def insert(self, diz_cond):
        """
        Insert
        """
        pass

    def delete(self, diz_cond):
        """
        Delete
        """
        pass
