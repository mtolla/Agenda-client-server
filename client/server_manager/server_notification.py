# Librerie server
from flask import Flask
from flask import request
import json
from data import data

requests = Flask(__name__)
data = data()
requests.run(host=data.ip, port=data.port, debug=True)


@requests.route("/")
def notification():
    act = json.loads(request.form['user'])
    print act