# Librerie server
from flask import Flask
from flask import request
# Importo classe Api
from api import Api
# Conversione Stringhe -> Dizionari
import ast

index = Flask(__name__)
api = Api()


@index.route("/")
def hello():
    return api.home()


@index.route("/Tolla")
def tolla():
    return api.error(False)


@index.route("/OMGTOLLA")
def omg_tolla():
    return api.omg_tolla()


@index.route('/login/token', methods=['POST'])
def do_login():
    dict_login = ast.literal_eval(request.form['dict_login'])
    usr = dict_login['username']
    psw = dict_login['password']
    ip = request.form['ip']
    if usr and psw:
        response = api.do_login(usr, psw, ip)
        if response:
            return response
        return 0


@index.route('/login', methods=['POST'])
def do_login_token():
    token = request.form['token']
    ip = request.form['ip']
    if token:
        return api.do_login_token(token, ip)


@index.route('/logout/<token>/<ip>', methods=['GET'])
def do_logut(token, ip):
    if api.check_token(token, ip):
        return api.do_logout(token)
    return False, 401


@index.route('/project/<int:id_proj>/<token>/<ip>', methods=['GET'])
def project(id_proj, token, ip):
    if api.check_token(token, ip):
        return api.project(token, id_proj)
    return False, 401


@index.route('/project/<int:id_proj>/holidays/<int:day>/<int:month>/<int:year>/<token>/<ip>', methods=['GET'])
def get_holidays_day(id_proj, day, month, year, token, ip):
    if api.check_token(token, ip):
        return api.get_holidays_day(id_proj, day, month, year)
    return False, 401


@index.route('/insert/activity/', methods=['POST'])
def insert_activity():
    dict_app = ast.literal_eval(request.form['dict_activity'])
    if api.check_token(dict_app['token'], dict_app['ip']):
        return api.insert_activity(dict_app['activity'])
    return False, 401


@index.route('/insert/holiday/', methods=['POST'])
def insert_holiday():
    dict_app = ast.literal_eval(request.form['dict_holiday'])
    if api.check_token(dict_app['token'], dict_app['ip']):
        return api.insert_holiday(dict_app['holiday'], dict_app['token'])
    return False, 401


@index.route('/projects/<token>/<ip>', methods=['GET'])
def get_user_project(token, ip):
    if api.check_token(token, ip):
        return api.get_user_project(token)
    return False, 401


@index.route('/project/<int:id_proj>/activities/<int:day>/<int:month>/<int:year>/<token>/<ip>', methods=['GET'])
def get_activity_day(id_proj, day, month, year, token, ip):
    if api.check_token(token, ip):
        return api.get_activity_day(id_proj, day, month, year)
    return False, 401


@index.route('/activity/<int:id_act>/<token>/<ip>', methods=['GET'])
def get_activity_info(id_act, token, ip):
    if api.check_token(token, ip):
        return api.get_activity_info(id_act, token)
    return False, 401


@index.route('/locations/<token>/<ip>', methods=['GET'])
def get_locations(token, ip):
    if api.check_token(token, ip):
        return api.get_locations()
    return False, 401


@index.route('/project/<int:id_proj>/groups/teamleader/<token>/<ip>', methods=['GET'])
def get_teamleader_groups(id_proj, token, ip):
    if api.check_token(token, ip):
        return api.get_teamleader_groups(id_proj, token)
    return False, 401


@index.route('/group/<int:id_group>/participants/<token>/<ip>', methods=['GET'])
def get_participants_from_group(id_group, token, ip):
    if api.check_token(token, ip):
        return api.get_participants_from_group(id_group)
    return False, 401


@index.route('/project/<int:id_proj>/participants/<token>/<ip>', methods=['GET'])
def get_participants_from_proj(id_proj, token, ip):
    if api.check_token(token, ip):
        return api.get_participants_from_proj(id_proj)
    return False, 401


@index.route('/groups/<int:id_group>/participant/level/<token>/<ip>', methods=['GET'])
def get_participants_name_lvl_group(id_group, token, ip):
    if api.check_token(token, ip):
        return api.get_participants_name_lvl_group(id_group)
    return False, 401


@index.route('/project/<int:id_proj>/not/participant/<token>/<ip>', methods=['GET'])
def get_not_participants_from_proj(id_proj, token, ip):
    if api.check_token(token, ip):
        return api.get_not_participants_from_proj(id_proj)
    return False, 401


@index.route('/project/<int:id_proj>/participants/<token>/<ip>', methods=['GET'])
def everybody(id_proj, token, ip):
    if api.check_token(token, ip):
        return api.everybody(id_proj)
    return False, 401


@index.route('/groups/<int:id_group>/father/<token>/<ip>', methods=['GET'])
def user_father_group(id_group, token, ip):
    if api.check_token(token, ip):
        return api.user_father_group(id_group)
    return False, 401


@index.route('/holiday/<int:id_usr>/<token>/<ip>', methods=['GET'])
def user_holiday(id_usr, token, ip):
    if api.check_token(token, ip):
        return api.user_holiday(id_usr)
    return False, 401

@index.route('/insert/activity', methods=['POST'])
def insert_activity():
    dict_app = ast.literal_eval(request.form['dict_activity'])
    if api.check_token(dict_app['token'], dict_app['ip']):
        return api.insert_activity(dict_app['activity'])
    return False, 401
@index.route('/insert/holiday', methods=['POST'])
def insert_holiday():
    dict_app = ast.literal_eval(request.form['dict_holiday'])
    if api.check_token(dict_app['token'], dict_app['ip']):
        return api.insert_holiday(dict_app['holiday'], dict_app['token'])
    return False, 401
@index.route('/modify/activity', methods=['POST'])
def modify_activity():
    dict_app = ast.literal_eval(request.form['dict_activity'])
    if api.check_token(dict_app['token'], dict_app['ip']):
        return api.modify_activity(dict_app['old'], dict_app['new'])
    return False, 401
@index.route('/modify/holiday', methods=['POST'])
def modify_holiday():
    dict_app = ast.literal_eval(request.form['dict_holiday'])
    if api.check_token(dict_app['token'], dict_app['ip']):
        return api.modify_holiday(dict_app['old'], dict_app['new'])
    return False, 401
@index.route('/modify/group', methods=['POST'])
def modify_group():
    dict_app = ast.literal_eval(request.form['dict_group'])
    if api.check_token(dict_app['token'], dict_app['ip']):
        return api.modify_group(dict_app['new'])
    return False, 401
@index.route('/modify/level', methods=['POST'])
def modify_level():
    dict_app = ast.literal_eval(request.form['dict_level'])
    if api.check_token(dict_app['token'], dict_app['ip']):
        return api.modify_level(dict_app['user'], dict_app['group'], dict_app['level'])
    return False, 401
@index.route('/modify/project', methods=['POST'])
def modify_project():
    dict_app = ast.literal_eval(request.form['dict_activity'])
    if api.check_token(dict_app['token'], dict_app['ip']):
        return api.modify_project(dict_app['new'])
    return False, 401
@index.route('/delete/activity/<int:id_act>/token/<token>/ip/<ip>', methods=['GET'])
def delete_activity(id_act, token, ip):
    if api.check_token(token, ip):
        return api.delete_activity(id_act)
    return False, 401
@index.route('/delete/holiday/<int:id_hol>/token/<token>/ip/<ip>', methods=['GET'])
def delete_holiday(id_hol, token, ip):
    if api.check_token(token, ip):
        return api.delete_holiday(id_hol)
    return False, 401
@index.route('/delete/group/<int:id_group>/token/<token>/ip/<ip>', methods=['GET'])
def delete_group(id_group, token, ip):
    if api.check_token(token, ip):
        return api.delete_group(id_group)
    return False, 401
@index.route('/delete/project/<int:id_proj>/token/<token>/ip/<ip>', methods=['GET'])
def delete_project(id_proj, token, ip):
    if api.check_token(token, ip):
        return api.delete_project(id_proj)
    return False, 401
@index.route('/create/group', methods=['POST'])
@index.route('/create/project', methods=['POST'])




@index.errorhandler(404)
def page_not_found(app):
    return api.error(True), 404



if __name__ == "__main__":
    # index.run(host='127.0.0.1', port=5000, debug=True)
    index.run(debug=True)
