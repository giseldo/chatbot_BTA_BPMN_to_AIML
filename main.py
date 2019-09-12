from flask import Flask, render_template, request, session
from threading import Lock
from flask_session import Session
from random import *
import sqlite3
import aiml
import os
import datetime


app = Flask(__name__)
app.secret_key = 'any random string'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
lock = Lock()

kernel = aiml.Kernel()


@app.route("/")
def home():
    sessionid = randint(1000,10000)
    session['sessionid'] = sessionid
    global kernel
    lock.acquire()
    if os.path.isfile("bot_brain.brn"):
        kernel.bootstrap(brainFile="bot_brain.brn")
    else:
        kernel.bootstrap(learnFiles="aiml/config.xml", commands="CEREBRO")
        kernel.saveBrain("bot_brain.brn")
    lock.release()
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    global kernel
    lock.acquire()
    entrada = request.args.get('msg')
    sessionid = session.get('sessionid')
    saida = kernel.respond(entrada, sessionid)
    lock.release()
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    datetime_object = datetime.datetime.now()
    cursor.execute("insert into log values (?, ?, ?, ?)", (sessionid, entrada, saida, datetime_object))
    conn.commit()
    conn.close()
    if saida == '':
        saida = "Não entendi."
    return str(saida)


if __name__ == "__main__":
    app.run()