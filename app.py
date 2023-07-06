from flask import Flask, render_template, request
from logging.config import dictConfig
import sqlite3
import os
import sys
import time

#from utils.influx_utils import extInflux
from utils.influx2_utils import extInflux2

#from flask_sqlalchemy import SQLAlchemy
from utils.plugins import plugins
from utils.settings import settings

#import time
#import atexit

from flask_apscheduler import APScheduler

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "flask.log",
                "formatter": "default",
            },
        },
        "root": {
            "level": "INFO", "handlers": ["console", "file"]
        },
    }
)

app = Flask(__name__)
# db = SQLAlchemy(app)

# logging.basicConfig(filename='app.log', level=logging.INFO)
# logging.basicConfig(level=logging.INFO)

#app._useInflux = False
app._useInflux2 = False

# add in library folders
sys.path.append("plugins")
sys.path.append("utils")

#get env varables, set os vars
values = settings.get_values()
for value in values:
    app.logger.info("Setting: " + value + ":" + values[value])
    os.environ[value] = values[value]
dbFile = os.environ["db_path"] + "/" + os.environ["db_file"]

#start some things
if __name__ == '__main__':
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
    return render_template("log.html")

@app.route('/logstream')
def logstream():
    def generate():
        with open('flask.log') as f:
            while True:
                yield f.read()
                time.sleep(1)

    return app.response_class(generate(), mimetype='text/plain')

@app.route("/db")
def db():

    return render_template("db.html", influxdb2=get_influxdb2())


@app.route("/settings", methods=["POST"])
def save_config():

    print(request.form.get("weather.appid"))
    # your code
    # return a response
    return view_settings()


@app.route("/settings")
def view_settings():
    # db = sqlite3.connect(dbFile)
    # cur = db.execute("SELECT * FROM sqlite_master")
    # data = cur.fetchall()
    settings_data = settings.get_values()

    configs = {}
    for file in os.listdir(os.environ["plugin_path"]):
        if "__" not in file and ".py" in file:
            plugin_name = file.replace(".py", "")
            module = __import__(plugin_name)
            class_ = getattr(module, plugin_name)
            instance = class_()
            configs[plugin_name] = instance.vars
            values = plugins.get_values()

    return render_template("settings.html", data=settings_data, configs=configs, values=values)

@app.route("/scheduler")
def scheduler():
    data = app.apscheduler.get_jobs()
    return render_template("scheduler.html", data=data)

def run_plugin(plugin_name):
    # data = "HomeAdmin"
    json_data = {"fail"}
    try:

        module = __import__(plugin_name)
        class_ = getattr(module, plugin_name)
        instance = class_()
        values = plugins.get_values()

        json_data = instance.run(values[plugin_name])
        # influxreturn = extInflux.sendToInflux(json_data)
        # app.logger.debug(influxreturn)

        influxdb2 = extInflux2(
            os.environ["influxdb2host"],
            os.environ["influxdb2token"],
            os.environ["influxdb2org"],
            os.environ["influxdb2bucket"]
        )
        influxreturn = influxdb2.sendToInflux(json_data[0])
        app.logger.debug(influxreturn)

    except Exception as e:
        app.logger.error(e)
    
    return json_data

#def tick(plugin):
    #run_plugin(plugin)
    #run_plugin("pollution")

def populate_scheduler():
    #scheduler = BackgroundScheduler()
    scheduler = APScheduler()
    scheduler.init_app(app)

    values = plugins.get_values()
    
    for appname in values:
        
        if("interval" in values[appname]):
            scheduler.add_job(func=run_plugin, args=[appname], trigger="interval", seconds=values[appname]["interval"], id=appname)

    #scheduler.add_job(func=run_plugin, args=["air_quality"], trigger="interval", seconds=values["air_quality"]["interval"], id="air quality")
    #scheduler.add_job(func=run_plugin, args=["pollution"], trigger="interval", seconds=values["pollution"]["interval"], id="pollution")

    scheduler.start()

@app.route("/run/<plugin_name>")
def run(plugin_name):
    json_formatted = run_plugin(plugin_name)
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


# def get_influxdb():
#     db = getattr(app, "_influxdb", None)
#     app._useInflux = False
#     if db is None:
#         db = app._influxdb = extInflux(
#             os.environ["influxdbhost"],
#             os.environ["influxdbport"],
#             os.environ["influxdbusername"],
#             os.environ["influxdbpass"],
#             os.environ["influxdbdatabase"],
#         )

#     if db.checkConnectivity():
#         app._useInflux = True
#     return db

def get_influxdb2():
    db = getattr(app, "_influxdb2", None)
    app._useInflux2 = False
    if db is None:
        db = app._influxdb2 = extInflux2(
            os.environ["influxdb2host"],
            os.environ["influxdb2token"],
            os.environ["influxdb2org"],
            os.environ["influxdb2bucket"]
        )

    if db.checkConnectivity():
        app._useInflux2 = True
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# create initial tables
def init_local_db():

    #make sure db dir exits
    if not os.path.exists(dbFile):
        app.logger.info(f"DB file {dbFile} doesn't exist")
        os.makedirs("db")

    conn = sqlite3.connect(dbFile)
    app.logger.info("Opened SQLite database successfully")

    # schema check
    cur = conn.execute('SELECT * FROM sqlite_master WHERE type ="table"')
    rows = cur.fetchall()

    #check if tables exist
    for row in rows:
        if "config" in row:
            app.logger.error("config table good")
        if "apps" in row:
            app.logger.info("apps table good")
        if "logs" in row:
            app.logger.info("apps table good")

    print(rows)

    #load with default schema
    sql_file = open("static/schema.sql")
    sql_as_string = sql_file.read()
    conn.executescript(sql_as_string)
    print("Table created successfully")
    conn.close()


init_local_db()
populate_scheduler()

