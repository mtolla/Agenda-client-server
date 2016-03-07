# Librerie server
from flask import Flask
from flask import request
import json

notification = Flask(__name__)


@notification.route("/")
def notification():
    act = json.loads(request.form['user'])
    print act