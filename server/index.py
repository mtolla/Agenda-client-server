# Librerie server
from flask import Flask
from flask import request
from flask import render_template
# Importo classe Api
from api import Api
# Conversione Stringhe -> Dizionari
import ast
# Signals
from blinker import Namespace

index = Flask(__name__)
api = Api()

# Creazione signals
signals = Namespace()
message_signals = signals.signal('GET REKT')
#using connect to register a signal callback
#message_signals.connect(function, app)
#send the signal
#message_signals.send(current_app._get_current_object(),email = email)


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


###########################################################################
# DA ELIMINARE SERVE PER TEST
@index.route('/login/<user>/<passw>/<ip>', methods=['GET'])
def asd(user, passw, ip):
    if user and passw and ip:
        response = api.do_login(user, passw, ip)
        if response:
            return response[0]
        return 0


@index.route('/testbaf/<int:id_proj>', methods=['GET'])
def piero(id_proj):
    return api.badass_function(id_proj)


@index.route('/agenda/<token>/<int:id_proj>', methods=['GET'])
def agenda(token, id_proj):
    return api.badass_function(token, id_proj)


@index.route('/activity/<int:id_att>', methods=['GET'])
def get_activity(id_att):
    return api.get_activity(id_att)


@index.route('/partecipants_group/<int:id_group>', methods=['GET'])
def get_partecipants_group(id_group):
    return api.get_partecipants_group(id_group)


###########################################################################
# ASSOLUTAMENTE DA TESTARE
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


@index.route('/activities_project/<int:id_proj>', methods=['GET'])
def get_activities_project(id_proj):
    return api.get_activities_project(id_proj)


@index.route('/holidays_proj/<int:id_proj>', methods=['GET'])
def get_holidays_proj(id_proj):
    return api.get_holidays_proj(id_proj)


@index.route('/group_name/<int:id_group>', methods=['GET'])
def get_group_name(id_group):
    return api.get_group_name(id_group)


@index.errorhandler(404)
def page_not_found(app):
    return api.error(True), 404


if __name__ == "__main__":
    # index.run(host='127.0.0.1', port=5000, debug=True)
    index.run(debug=True)


