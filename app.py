from flask import Flask, render_template
import sqlite3
import os
import air_quality
import speed_test
import weather
import logging
import json
#from influx_utils import extInflux
#from flask_sqlalchemy import SQLAlchemy
import logging
import traceback

app = Flask(__name__)
#db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(filename='demo.log', level=logging.DEBUG)

dbFile = 'db\database.db'

app._useInflux = False

os.environ["influxdbhost"] = "192.168.103.111"
os.environ["influxdbport"] = "8086"
os.environ["influxdbusername"] = "test"
os.environ["influxdbpass"] = "test"
os.environ["influxdbdatabase"] = "HomeStatus"

#if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=os.getenv('PORT'))

@app.route('/')
def index():
    app.logger.error("home page accessed")

    db = sqlite3.connect(dbFile)
    cur = db.execute('select * from apps')
    data = cur.fetchall()

    return render_template("index.html", data=data, environ=os.environ)


@app.route('/env')
def env():
    return render_template("env.html", environ=os.environ)


@app.route('/log')
def log():
    #app.logger.
    db = sqlite3.connect(dbFile)
    cur = db.execute('select * from logs limit 1000')
    data = cur.fetchall()
    
    return render_template("log.html", data=data)

@app.route('/db')
def db():
    db = sqlite3.connect(dbFile)
    cur = db.execute('SELECT     name FROM     sqlite_master ')
    data = cur.fetchall()

    return render_template("db.html", data=data, influxdb=get_influxdb())


@app.route('/run/<plugin_name>')
def run(plugin_name):
    #data = "HomeAdmin"
    
    module = __import__(plugin_name)
    class_ = getattr(module, plugin_name)
    instance = class_()

    json_data={"fail"}

    if(plugin_name=="air_quality"):
        json_data=instance.run("22553")
    if(plugin_name=="weather"):
        json_data=instance.run("60564","key")
    if(plugin_name=="speed_test"):
        json_data=instance.run()

    #influxreturn = influx_utils.sendToInflux(json_data)
    json_formatted=json.dumps(json_data, indent=2)
    return render_template("run.html", json_data=json_formatted)


@app.route('/admin')
def admin():
    data = "HomeAdmin"
    return render_template("admin.html", data=data)


def get_db():
    db = getattr(app, '_database', None)
    if db is None:
        db = app._database = sqlite3.connect(dbFile)
    return db


def get_influxdb():
    db = getattr(app, '_influxdb', None)
    app._useInflux = False
    if db is None:
        db = app._influxdb = extInflux(os.environ["influxdbhost"], os.environ["influxdbport"],
                                       os.environ["influxdbusername"], os.environ["influxdbpass"], os.environ["influxdbdatabase"])

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
    conn = sqlite3.connect(dbFile)
    print("Opened SQLite database successfully")

    sql_file = open('static/schema.sql')
    sql_as_string = sql_file.read()
    conn.executescript(sql_as_string)
    print("Table created successfully")
    conn.close()


init_local_db()
