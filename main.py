from flask import Flask, render_template, request, session
from flask_session import Session
from random import *
import botty
import db


app = Flask(__name__)
app.secret_key = 'any random string'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)


@app.route("/")
def home():
    sessionid = randint(1000,10000)
    session['sessionid'] = sessionid
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    entrada = request.args.get('msg')
    sessionid = session.get('sessionid')
    saida = botty.respond(entrada, sessionid)
    db.inserir(sessionid, entrada, saida)
    if saida == '':
        saida = "Não entendi."
    return str(saida)


if __name__ == "__main__":
    app.run()