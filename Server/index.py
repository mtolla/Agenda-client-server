# Librerie server
from flask import Flask
from flask import request
# Importo classe Api
from api import Api

index = Flask(__name__)
index.debug = True
api = Api()
link = '<img src="https://goo.gl/dmr6pW">'

@index.route("/")
def hello():
    return 'Welcome to TollaServer 0.1'

@index.route("/Tolla")
def tolla():
    return link


@index.route("/ping")
def ping():
    return True

@index.route("/testbg")
def testbg():
    return api.test_bg()

@index.route('/login', methods=['POST'])
def do_login():
    api.do_login(request.form['username'], request.form['password'])

@index.route('/login/<token>', methods=['POST'])
def do_login_token(self):
    return api.do_login_token(request.form['token'])


if __name__ == "__main__":
    index.run()