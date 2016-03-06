# -*- coding: utf-8 -*-
from utils import populate


class ClassDbHelper:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    ####################################################################################################################
    # Parte di gestione controllo e inserimento nel db
    ####################################################################################################################

    def insert_activity(self, act):
        # act ha dentro {"name": "","project":, "type": "", "creator":,"location":,"group":,"description": "",
        # "participants": [],"date": {"day", "month", "year", "hour", "minute"}, "duration": 2}
        #  Ricevo una attività, controllo che non dia fastidio a nulla, in caso di esito negativo la inserisco
        # Ricevo tutte le attività di quel giorno (ID, name, begin, end)
        day_act = self.db_manager.get_activity_day_all(act['date'])
        day_hol = self.db_manager.get_holidays_day_all(act['date'])
        # Controllo subito se la stanza non è già occupata
        list_occ_room = self.db_manager.room_occupied(day_act, act['date'], act['duration'])
        for acttivity in day_act:
            if acttivity['room'] in list_occ_room:
                return "Error: Stanza occupata"
        # Controllo se è un attività singola
        if act['type'] == 'single':
            ids_act = self.get_activites_rel_al_activity(act['creator'])
            ids_hol = self.get_holidays_rel_alone_activity(act['creator'])
        else:
            ids_act = self.get_activites_rel_activity(act['group'])
            ids_hol = self.get_holidays_rel_activity(act['group'])
        # Faccio un intersezione tra tutte le attività di gruppo e quelle del giorno
        day_act = self.cleaner_list(day_act, ids_act)
        # Faccio una intersezione tra le festività e quelle del giorno
        day_hol = self.cleaner_list(day_hol, ids_hol)
        # Ci sono delle vacanze in quel giorno
        if day_hol:
            return "Error: Esistono delle vacanze"
        data_end = self.db_manager.calc_duration(act['date'], act['duration'])
        list_error = self.is_there_something_activity(act['date'], data_end, day_act)
        if list_error:
            return list_error
        # Implementazione programma teo
        list_act = self.db_manager.open_file('activity')
        act['ID'] = populate.next_index(list_act)
        list_act.append(act)
        return self.db_manager.write_file(act, 'activity')

    @staticmethod
    def cleaner_list(list_res, list_del):
        for app in list_res:
            if not app['ID'] in list_del:
                list_res.remove(app)  ## Controllare
        return list_res

    def insert_holiday(self, hol, id_usr):
        # hol ha dentro {"begin": {"day", "month", "year"}, "end": {"day", "month","year"}, "name"}
        # id_usr mi serve per capire di chi è la vacanza
        #  Ricevo una vacanza, controllo che non dia fastidio a nulla, in caso di esito negativo la inserisco
        ids_act = self.get_activites_rel_holiday(id_usr)
        # Trovo tutte le attività in quel periodo
        days_act = []
        for year in range(hol['begin']['year'], hol['end']['year'], 1):
            for month in range(hol['begin']['month'], hol['end']['month'], 1):
                for day in range(hol['begin']['day'], hol['end']['day'], 1):
                    days_act.append(self.db_manager.get_activity_day_all({'day': day, 'month': month, 'year': year}))
        list_error = self.is_there_something_holiday(id_usr, days_act)
        if list_error:
            return list_error
        # Implementazione programma teo
        return populate.setholidays(id_usr, hol)

    def is_there_something_activity(self, date_star, date_end, day_act):
        # Activity edition
        # Controllo che non ci sia nulla in quella data
        # Mi arrivano:
        #   - due date date_start = {hour, minute, day, month, year} e date_end = {hour, minute}.
        #   - day_act e day_hol, due liste contenenti le attività e vacanze di quel giorno
        # Rispondo se c'è già qualcosa
        # Se è una vacanza devo controllare tutte quelle che iniziano prima e finiscono dopo
        # Se è una attività devo controllare che sia di quel giorno e la data di inizio non si incroci con una delle due
        list_return = []
        for activity in day_act:
            date_end_anct = self.db_manager.calc_duration(activity['date'], activity['duration'])
            if self.is_there_appa(activity, date_star, date_end, date_end_anct) or self.is_there_appb(activity,
                                                                                                      date_star,
                                                                                                      date_end,
                                                                                                      date_end_anct):
                list_return.append({'activity': activity})
        return list_return

    @staticmethod
    def is_there_appa(activity, date_star, date_end, date_end_anct):
        if (activity['date']['hour'] >= date_star['hour'] and activity['date']['hour'] > date_end['hour']) or (
                        activity['date']['hour'] <= date_star['hour'] and date_end_anct['hour'] >= date_end[
                    'hour']) or (
                        date_star['hour'] < date_end_anct['hour'] <= date_end['hour']) or (
                    activity['date']['hour'] == date_star['hour']):
            return True
        return False

    @staticmethod
    def is_there_appb(activity, date_star, date_end, date_end_anct):
        if ((activity['date']['minute'] >= date_star['minute'] and activity['date']['minute'] > date_end['minute']) or (
                        activity['date']['minute'] <= date_star['minute'] and date_end_anct['date']['minute'] >=
                    date_end[
                        'minute']) or (date_star['minute'] < activity['date']['minute'] <= date_end['minute'])):
            return True
        return False

    @staticmethod
    def is_there_something_holiday(id_usr, ids_act):
        # Holiday edition
        # Controllo che non ci sia nulla in quella data e nelle successive
        # Mi arriva una data {day, month, year} e rispondo se c'è già qualcosa
        # Se è una vacanza devo controllare tutte quelle che iniziano prima e finiscono dopo
        # Se è una attività devo controllare che sia di quel giorno e la data di inizio non si incroci con una delle due
        list_return = []
        for activity in ids_act:
            if id_usr in activity['participant']:
                list_return.append(activity)
        return list_return

    def get_activites_rel_al_activity(self, id_usr):
        # Parto da un utente e trovo tutte le attività dei suoi gruppi
        list_group = self.db_manager.from_user_get_groups(id_usr)
        list_app_usr = []
        list_act = []
        for group in list_group:
            set(list_app_usr).union(self.db_manager.from_group_get_users(group))
        for user in list_app_usr:
            set(list_act).union(self.db_manager.from_user_get_acts(user))
        return list_act

    def get_activites_rel_activity(self, id_group):
        # Parto da un gruppo e trovo tutti i gruppi degli utenti con quel gruppo
        # Trovo tutte le attività con quei gruppi
        list_usr = self.db_manager.open_file('user')
        list_group = []
        list_app_usr = []
        list_act = []
        for user in list_usr:
            for group in list_usr['groups']:
                if group['ID'] == id_group:
                    list_group.append(self.db_manager.from_user_get_groups(user['ID']))
                    break
        for group in list_group:
            set(list_app_usr).union(self.db_manager.from_group_get_users(group))
        for user in list_app_usr:
            set(list_act).union(self.db_manager.from_user_get_acts(user))
        return list_act

    def get_holidays_rel_alone_activity(self, id_usr):
        # Parto dall'utente e trovo tutte le sue vacanze
        return self.db_manager.from_user_hol(id_usr)

    def get_holidays_rel_activity(self, id_group):
        # Parto da un gruppo e trovo tutti gli utenti
        # Trovo tutte le vacanze degli utenti
        list_usr = self.db_manager.open_file('user')
        list_app_usr = []
        list_hol = []
        for user in list_usr:
            for group in list_usr['groups']:
                if group['ID'] == id_group:
                    list_app_usr.append(user['ID'])
                    break
        for user in list_app_usr:
            set(list_hol).union(self.db_manager.from_user_hol(user))
        return list_hol

    def get_activites_rel_holiday(self, id_usr):
        # Parto da un utente e trovo tutti i gruppi degli utenti correlati
        # Trovo tutte le attività con gli utenti
        list_group = self.db_manager.from_user_get_groups(id_usr)
        list_app_usr = []
        list_act = []
        for group in list_group:
            set(list_app_usr).union(self.db_manager.from_group_get_users(group))
        for user in list_app_usr:
            set(list_act).union(self.db_manager.from_user_get_acts(user))
        return list_act

    ####################################################################################################################
    # Parte di gestione controllo e modifica/eliminazione nel db
    ####################################################################################################################

    def modify_act(self, old_act, new_act):
        # Ricevo l'attività nuova da modificare e quella vecchia
        self.delete_act(old_act['ID'])
        insert = self.insert_activity(new_act)
        if insert == "OK":
            return True
        self.insert_activity(old_act)
        self.db_manager.modified_act.append(new_act['ID'])

    def modify_hol(self, old_hol, new_hol):
        # Ricevo la vacanza nuova da modificare e quella vecchia
        self.delete_act(old_hol['ID'])
        insert = self.insert_activity(new_hol)
        if insert == "OK":
            return True
        self.insert_activity(old_hol)

    def modify_group(self, new_group):
        list_group = self.db_manager.open_file('group')
        for group in list_group:
            if group['ID'] == new_group['ID']:
                list_group.remove(group)
                list_group.append(new_group)
                return self.db_manager.write_file(list_group, 'group')
        return False

    def modify_level(self, id_usr, id_group, level):
        list_user = self.db_manager.open_file('user')
        for user in list_user:
            if user['ID'] == id_usr:
                user['groups'] = self.db_manager.modify_level_app(id_group, level, user['groups'])
                return self.db_manager.write_file(list_user, 'user')
        return False

    def modify_proj(self, new_proj):
        list_proj = self.db_manager.open_file('project')
        for proj in list_proj:
            if proj['ID'] == new_proj['ID']:
                list_proj.remove(proj)
                list_proj.append(new_proj)
                return self.db_manager.write_file(list_proj, 'proj')
        return False

    def delete_act(self, id_act):
        # Ricevo id_act e la elimino
        list_act = self.db_manager.open_file('activity')
        for activity in list_act:
            if activity['ID'] == id_act:
                list_act.remove(activity)
        return self.db_manager.write_file(list_act, 'activity')

    def delete_hol(self, id_hol):
        # Ricevo id_hol e la elimino, sia da user che da holiday
        list_usr = self.db_manager.open_file('user')
        list_hol = self.db_manager.open_file('holiday')
        for user in list_usr:
            if id_hol in user['holiday']:
                user['holiday'].remove(id_hol)
                break
        for holiday in list_hol:
            if holiday['ID'] == id_hol:
                id_hol.remove(holiday)
        if self.db_manager.write_file(list_usr, 'user') and self.db_manager.write_file(list_hol, 'holiday'):
            return True
        return False

    def delete_group(self, id_group):
        list_group = self.db_manager.open_file('group')
        for group in list_group:
            if group['ID'] == id_group:
                if group['father']:
                    self.delete_subgroup(group['subgroup'])
                    self.delete_act_group(id_group)
                    self.delete_user_group(id_group)
                break
        return self.db_manager.write_file(list_group, 'group')

    def delete_subgroup(self, list_sub):
        for sub in list_sub:
            self.delete_group(sub)

    def delete_act_group(self, id_group):
        list_act = self.db_manager.open_file('activity')
        for activity in list_act:
            if activity['group'] == id_group:
                self.delete_act(activity['ID'])
        return True

    def delete_user_group(self, id_group):
        # Elimino solo il gruppo dall'utente
        list_usr = self.db_manager.open_file('user')
        for user in list_usr:
            if id_group in user['holiday']:
                user['holiday'].remove(id_group)
        return self.db_manager.write_file(list_usr, 'user')

    def delete_proj(self, id_proj):
        # Elimino il progetto e chiamo per eliminare il gruppo padre
        list_proj = self.db_manager.open_file('proj')
        if len(list_proj) == 1:
            return False, 401
        for proj in list_proj:
            if proj['ID'] == id_proj:
                self.delete_group_father(proj['group'])
                list_proj.remove(proj)
                break
        return self.db_manager.write_file(list_proj, 'project')

    def delete_group_father(self, id_group):
        list_group = self.db_manager.open_file('group')
        for group in list_group:
            if group['ID'] == id_group:
                if not group['father']:
                    self.delete_subgroup(group['subgroup'])
                    self.delete_act_group(id_group)
                    self.delete_user_group(id_group)
                break
        return self.db_manager.write_file(list_group, 'group')

    def create_group(self, group):
        pass

    def create_project(self, project):
        pass
