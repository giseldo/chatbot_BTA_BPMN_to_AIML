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
        saida = "Nao entendi."
    return str(saida)

@app.route('/home')
def index():
    return render_template('index_novo.html')

@app.route('/process',methods=['POST'])
def process():
    user_input=request.form['user_input']
    sessionid = session.get('sessionid')
    bot_response = botty.respond(user_input, sessionid)
    return render_template('index_novo.html', user_input=user_input, bot_response=bot_response)



if __name__ == "__main__":
    app.run()