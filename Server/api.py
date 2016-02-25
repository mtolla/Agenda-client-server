# Importo librerie
import datetime
from time import time
#Librerie server
from flask import Flask
from flask import request
#Librerie underground Task


# Importo dbManager
from dbManager import ClassDbManager
# Importo loginManager
from loginManager import ClassLoginManager


api = Flask(__name__)
api.debug = True
link = '<img src="https://goo.gl/dmr6pW">'
dbManager = ClassDbManager()
loginManager = ClassLoginManager()


#############################
# Variabili cotrollo login   #
#############################
usrMaxLen = 10
pswMaxLen = 10


#############################

@api.route("/")
def hello():
    return 'Welcome to TollaServer 0.1'

@api.route("/Tolla")
def tolla():
    return link


@api.route("/ping")
def ping():
    return True


@api.route('/login', methods=['POST'])
def do_login():
    user = request.form['username']
    password = request.form['password']
    if valid_credentials(user, password):
        return loginManager.do_login(user, password)

@app.route('/login/<token>', methods=['POST'])
def do_login_token():
    return loginManager.do_login_token(request.form['token'])

def valid_credentials(user, psw):
    if len(user) <= usrMaxLen and len(psw) <= pswMaxLen:
        return True
    else:
        return False



#################################
# Background work






























if __name__ == "__main__":
    api.run()
