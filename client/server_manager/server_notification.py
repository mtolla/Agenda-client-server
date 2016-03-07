# Librerie server
from flask import Flask
from flask import request
import json

notification = Flask(__name__)
notification.run(host=data.ip, port=data.port, debug=True)


@notification.route("/")
def notification():
    act = json.loads(request.form['user'])
    print act