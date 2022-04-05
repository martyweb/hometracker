from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
import os
import sys
import plugins.air_quality as air_quality
import plugins.speed_test as speed_test
import plugins.weather as weather
import logging
import json
from utils.influx_utils import extInflux

# from flask_sqlalchemy import SQLAlchemy
import logging
import traceback
from utils.plugins import plugins

import time
import atexit
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
# db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename='demo.log', level=logging.DEBUG)

app._useInflux = False

# add in library folders
sys.path.append("plugins")
sys.path.append("utils")

# static env varables, eventually dynamic
os.environ["influxdbhost"] = "192.168.103.111"
os.environ["influxdbport"] = "8086"
os.environ["influxdbusername"] = "test"
os.environ["influxdbpass"] = "test"
os.environ["influxdbdatabase"] = "HomeStatus"

os.environ["db_file"] = "database.db"
os.environ["plugin_path"] = "plugins"
os.environ["db_path"] = "db"
dbFile = os.environ["db_path"] + "" + os.environ["db_file"]

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"))


@app.route("/")
def index():
    # app.logger.error("home page accessed")

    db = sqlite3.connect(dbFile)
    cur = db.execute("select * from apps")
    data = cur.fetchall()

    return render_template("index.html", data=data, environ=os.environ)


@app.route("/env")
def env():
    return render_template("env.html", environ=os.environ)


@app.route("/log")
def log():
    # app.logger.
    db = sqlite3.connect(dbFile)
    cur = db.execute("select * from logs limit 1000")
    data = cur.fetchall()

    return render_template("log.html", data=data)


@app.route("/db")
def db():
    db = sqlite3.connect(dbFile)
    cur = db.execute("SELECT     name FROM     sqlite_master ")
    data = cur.fetchall()

    return render_template("db.html", data=data, influxdb=get_influxdb())


@app.route("/settings", methods=["POST"])
def save_config():

    print("----------------")
    print(request.form.get("weather.appid"))
    # your code
    # return a response
    return view_settings()


@app.route("/settings")
def view_settings():
    db = sqlite3.connect(dbFile)
    cur = db.execute("SELECT * FROM sqlite_master")
    data = cur.fetchall()

    configs = {}
    for file in os.listdir(os.environ["plugin_path"]):
        if "__" not in file:
            plugin_name = file.replace(".py", "")
            module = __import__(plugin_name)
            class_ = getattr(module, plugin_name)
            instance = class_()
            configs[plugin_name] = instance.vars
            values = plugins.get_values()

    return render_template("settings.html", data=data, configs=configs, values=values)


def tick():
    print("tick")


@app.route("/scheduler")
def scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(tick, "interval", seconds=3)
    scheduler.start()

    data = apscheduler.job.get_jobs()
    return render_template("scheduler.html", data=data)


@app.route("/run/<plugin_name>")
def run(plugin_name):
    # data = "HomeAdmin"

    module = __import__(plugin_name)
    class_ = getattr(module, plugin_name)
    instance = class_()

    json_data = {"fail"}
    values = plugins.get_values()

    json_data = instance.run(values[plugin_name])

    # influxreturn = influx_utils.sendToInflux(json_data)
    json_formatted = json.dumps(json_data, indent=2)
    return render_template("run.html", json_data=json_formatted)


@app.route("/admin")
def admin():
    data = "HomeAdmin"
    return render_template("admin.html", data=data)


def get_db():
    db = getattr(app, "_database", None)
    if db is None:
        db = app._database = sqlite3.connect(dbFile)
    return db


def get_influxdb():
    db = getattr(app, "_influxdb", None)
    app._useInflux = False
    if db is None:
        db = app._influxdb = extInflux(
            os.environ["influxdbhost"],
            os.environ["influxdbport"],
            os.environ["influxdbusername"],
            os.environ["influxdbpass"],
            os.environ["influxdbdatabase"],
        )

    if db.checkConnectivity():
        app._useInflux = True
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# create initial tables
def init_local_db():

    if not os.path.exists(dbFile):
        print("DB file {{dbFile}} doesn't exist")

    conn = sqlite3.connect(dbFile)
    print("Opened SQLite database successfully")

    # scheme check
    cur = conn.execute('SELECT * FROM sqlite_master WHERE type ="table"')
    rows = cur.fetchall()
    if "config" in rows:
        print("config table good")
    if "apps" in rows:
        print("apps table good")

    print(rows)

    sql_file = open("static/schema.sql")
    sql_as_string = sql_file.read()
    conn.executescript(sql_as_string)
    print("Table created successfully")
    conn.close()


init_local_db()
