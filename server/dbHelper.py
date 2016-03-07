# -*- coding: utf-8 -*-
import copy

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
        act_original = copy.deepcopy(act)
        day_act = self.db_manager.get_activity_day_all(act['date'])
        day_hol = self.db_manager.get_holidays_day_all(act['date'])
        # Controllo subito se la stanza non è già occupata
        self.room_occupied(day_act, act['date'], act['duration'])
        list_occ_room = self.room_occupied(day_act, act['date'], act['duration'])
        for activity in day_act:
            if activity['room'] in list_occ_room:
                return False
        # Faccio un intersezione tra tutte le attività di gruppo e quelle del giorno
        day_act = self.cleaner_list(day_act, act['participants'])
        # Faccio una intersezione tra le festività e quelle del giorno
        day_hol = self.cleaner_list(day_hol, act['participants'])
        # Ci sono delle vacanze in quel giorno
        if day_hol:
            return False
        data_end = self.db_manager.calc_duration(act['date'], act['duration'])
        list_error = self.is_there_something_activity(act['date'], data_end, day_act)
        if list_error:
            return False
        # Implementazione programma teo
        list_act = self.db_manager.open_file('activity')
        act_original['ID'] = populate.next_index(list_act)
        list_act.append(act_original)
        self.db_manager.write_file(list_act, 'activity')
        self.db_manager.check_today_tomorrow_act(True)
        return True

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
        # Trovo tutte le attività in quel periodo
        days_act = []
        hol_original = copy.deepcopy(hol)
        for year in range(hol['begin']['year'], hol['end']['year'], 1):
            for month in range(hol['begin']['month'], hol['end']['month'], 1):
                for day in range(hol['begin']['day'], hol['end']['day'], 1):
                    days_act.append(self.db_manager.get_activity_day_all({'day': day, 'month': month, 'year': year}))
        list_error = self.is_there_something_holiday(id_usr, days_act)
        if list_error:
            return list_error
        # Implementazione programma teo
        list_hol = self.db_manager.open_file('holiday')
        hol_original['ID'] = populate.next_index(list_hol)
        list_hol.append(hol_original)
        self.db_manager.write_file(list_hol, 'holiday')
        self.set_user_holiday(id_usr, hol_original['ID'])
        return "OK"

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
            if self.is_there_appa(activity['begin'], date_star, date_end, activity['end']) or self.is_there_appb(
                    activity['begin'],
                    date_star,
                    date_end,
                    activity['end']):
                list_return.append({'activity': activity})
        return list_return

    @staticmethod
    def is_there_appa(ini_es, ini_new, fine_new, fine_es):
        if ini_new['hour'] <= ini_es['hour'] < fine_new['hour'] or ini_es['hour'] <= ini_new['hour'] <= fine_es[
            'hour'] or ini_new['hour'] <= fine_es['hour'] <= fine_new['hour']:
            return True
        return False

    @staticmethod
    def is_there_appb(ini_es, ini_new, fine_new, fine_es):
        if fine_new['hour'] == ini_new['hour'] and (
                                ini_new['minute'] <= ini_es['minute'] < fine_new['minute'] or ini_es['minute'] <=
                        ini_new[
                            'minute'] <= fine_es['minute'] or ini_new['minute'] <= fine_es['minute'] <= fine_new[
                    'minute']):
            return True
        return False

    def room_occupied(self, day_act, begin, dur):
        # Da una lista di attività della giornata, l'ora di inizio e la durata
        # rispondo con le stanze occupate in quel lasso di tempo
        end = self.db_manager.calc_duration(begin, dur)
        list_return = []
        for activity in day_act:
            if self.is_there_appa(activity['begin'], begin, end, activity['end']) or self.is_there_appb(
                    activity['begin'], begin, end, activity['end']):
                list_return.append(activity['room'])
        return list_return

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

    def set_user_holiday(self, id_usr, id_hol):
        list_usr = self.db_manager.open_file('user')
        for user in list_usr:
            if user['ID'] == id_usr:
                user['holiday'].append(id_hol)
                break
        self.db_manager.write_file(list_usr, 'user')

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

    def create_group(self, group, id_usr, list_id_usr):
        # Inserisco in gruppi
        list_group = self.db_manager.open_file('group')
        id = populate.next_index(list_group)
        group['ID'] = id
        list_group.append(group)
        self.db_manager.write_file(group, 'group')
        self.add_group_to_usr(id, list_id_usr, id_usr)

    def add_group_to_usr(self, id, list_id_usr, id_usr):
        list_usr = self.db_manager.open_file('user')
        for user in list_usr:
            if user['ID'] in list_id_usr:
                if user['ID'] == id_usr:
                    user['groups'].append({'ID': id, 'level': 'teamleader'})
                user['groups'].append({'ID': id, 'level': 'participant'})

    def create_project(self, project, group, list_id_usr, id_usr):
        # Inserisco nei progetti
        list_proj = self.db_manager.open_file('project')
        id = populate.next_index(list_proj)
        project['ID'] = id
        list_proj.append(project)
        self.db_manager.write_file(project, 'project')
        self.create_group(group, list_id_usr, id_usr)
