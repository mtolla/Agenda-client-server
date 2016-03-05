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


@index.route("/ping")
def ping():
    return True


@index.route("/testbg")
def testbg():
    return api.test()


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


###########################################################################
# DA ELIMINARE SERVE PER TEST
@index.route('/login/<user>/<passw>/<ip>', methods=['GET'])
def asd(user, passw, ip):
    if user and passw and ip:
        response = api.do_login(user, passw, ip)
        if response:
            return response
        return 0


@index.route('/testbaf/<int:id_proj>/<token>', methods=['GET'])
def piero(id_proj, token):
    return api.badass_function(token, id_proj)


# Modificata, da testare
@index.route('/project/<int:id_proj>/<token>/<ip>', methods=['GET'])
def project(id_proj, token, ip):
    api.check_token(token, ip)
    return api.project(token, id_proj)


@index.route('/activity/<int:id_att>', methods=['GET'])
def get_activity(id_att):
    return api.get_activity(id_att)


@index.route('/name_projects/<list_id_proj>', methods=['GET'])
def get_name_projects(list_id_proj):
    return api.get_name_projects(list_id_proj)


@index.route('/project/<int:id_proj>', methods=['GET'])
def get_project(id_proj):
    return api.get_project(id_proj)


@index.route('/pjmanager_mail/<int:id_proj>', methods=['GET'])
def get_pjmanager_mail(id_proj):
    return api.get_pjmanager_mail(id_proj)


@index.route('/is_teamleader/<token>', methods=['GET'])
def get_is_teamleader(token):
    if api.get_is_teamleader(token):
        return "True", 200
    else:
        return "False", 404


@index.route('/holidays_proj/<int:id_proj>', methods=['GET'])
def get_holidays_proj(id_proj):
    return api.get_holidays_proj(id_proj)


@index.route('/group_name/<int:id_group>', methods=['GET'])
def get_group_name(id_group):
    return api.get_group_name(id_group)


###########################################################################
# ASSOLUTAMENTE DA TESTARE
@index.route('/projects/<token>/<ip>', methods=['GET'])
def get_user_project(token, ip):
    if api.check_token(token, ip):
        return api.get_user_project(token)
    return False, 401


@index.route('/activities/<int:day>/<int:month>/<int:year>/<token>/<ip>', methods=['GET'])
def get_activity_day(day, month, year, token, ip):
    if api.check_token(token, ip):
        return api.get_activity_day(day, month, year)
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


@index.route('/groups/teamleader/<token>/<ip>', methods=['GET'])
def get_teamleader_groups(token, ip):
    if api.check_token(token, ip):
        return api.get_teamleader_groups(token)
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


@index.route('/participants/<token>/<ip>', methods=['GET'])
def everybody(token, ip):
    if api.check_token(token, ip):
        return api.everybody()
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


@index.errorhandler(404)
def page_not_found(app):
    return api.error(True), 404


if __name__ == "__main__":
    # index.run(host='127.0.0.1', port=5000, debug=True)
    index.run(debug=True)
