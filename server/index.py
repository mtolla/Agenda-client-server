# Librerie server
from flask import Flask
from flask import request
from flask import render_template
# Importo classe Api
from api import Api
# Conversione Stringhe -> Dizionari
import ast

index = Flask(__name__)
index.debug = True
api = Api()


@index.route("/")
def hello():
    return 'Welcome to TollaServer 0.1'


@index.route("/Tolla")
def tolla():
    return api.error(False)


@index.route("/ping")
def ping():
    return True


@index.route("/testbg")
def testbg():
    return api.test()


@index.route('/login/<token>', methods=['POST'])
def do_login(token):
    dict_login = ast.literal_eval(request.form['dict_login'])
    usr = dict_login['username']
    psw = dict_login['password']
    if usr and psw:
        response = api.do_login(usr, psw)
        if response:
            return response
        return 0


@index.route('/login', methods=['POST'])
def do_login_token():
    token = request.form['token']
    if token:
        return api.do_login_token(token)


"""
Legenda:
/
/agenda : bad_ass_function
"""


@index.route('/agenda/<token>/<id_proj>', methods=['GET'])
def agenda(token, id_proj):
    return api.badass_function(token, id_proj)


@index.route('/activity/<id_att>', methods=['GET'])
def get_activity(id_att):
    return api.get_activity(id_att)


@index.route('/partecipants_group/<id_group>', methods=['GET'])
def get_partecipants_group(id_group):
    return api.get_partecipants_group(id_group)


@index.route('/name_projects/<list_id_proj>', methods=['GET'])
def get_name_projects(list_id_proj):
    return api.get_name_projects(list_id_proj)


@index.route('/project/<id_proj>', methods=['GET'])
def get_project(id_proj):
    return api.get_project(id_proj)


@index.route('/pjmanager_mail/<id_proj>', methods=['GET'])
def get_pjmanager_mail(id_proj):
    return api.get_pjmanager_mail(id_proj)


@index.route('/is_teamleader/<token>', methods=['GET'])
def get_is_teamleader(token):
    if api.get_is_teamleader(token):
        return "True", 200
    else:
        return "False", 404


@index.route('/activities_project/<id_proj>', methods=['GET'])
def get_activities_project(id_proj):
    return api.get_activities_project(id_proj)


@index.route('/holidays_proj/<id_proj>', methods=['GET'])
def get_holidays_proj(id_proj):
    return api.get_holidays_proj(id_proj)


@index.route('/group_name/<id_group>', methods=['GET'])
def get_group_name(id_group):
    return api.get_group_name(id_group)


@index.errorhandler(404)
def page_not_found(app):
    return api.error(True), 404


if __name__ == "__main__":
    index.run()
