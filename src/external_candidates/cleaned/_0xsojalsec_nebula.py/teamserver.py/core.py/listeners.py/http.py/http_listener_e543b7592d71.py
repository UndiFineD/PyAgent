# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Nebula\teamserver\core\Listeners\HTTP\http_listener.py
import random
import string
import sys

import mongoengine
from database.db import initialize_db
from flask import Flask
from flask_bcrypt import Bcrypt, generate_password_hash
from flask_jwt_extended import JWTManager
from pymongo import ReadPreference
from termcolor import colored
from waitress import serve

from core.Listeners.HTTP.database.models import Listeners, Particles, Tasks


def start_listener(apiHost, apiPort, databaseHost, databasePort, databaseName):
    app = Flask(__name__)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    jwt_token = "".join(
        random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(32)
    )
    app.config["JWT_SECRET_KEY"] = jwt_token

    try:
        app.config["MONGODB_DB"] = databaseName
        app.config["MONGODB_HOST"] = databaseHost
        app.config["MONGODB_PORT"] = databasePort
        app.config["MONGODB_CONNECT"] = False

        initialize_db(app)

        # app.register_blueprint(task_blueprint)

        serve(app, host=apiHost, port=apiPort)
    except Exception as e:
        if e == None or e == "":
            exit()
        else:
            print(colored("[*] {}".format(e), "red"))
            exit()
