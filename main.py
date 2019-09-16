from flask import Flask, render_template, request, session
from flask_session import Session
from random import *
import db
from botty import botty
from werkzeug.wsgi import responder

app = Flask(__name__)
app.secret_key = 'any random string'
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)
b = botty() 

@app.route("/")
def index():
    sessionid = randint(1000,10000)
    session['sessionid'] = sessionid
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    entrada = request.args.get('msg')
    sessionid = session.get('sessionid')
    print(entrada)
    print(sessionid)
    print("isto e um teste")
    saida = b.responder_novo(entrada, sessionid)
    saida = ""
    if saida == "":
        saida = "Nao entendi."
    return str(saida)


@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/process',methods=['POST'])
def process():
    user_input=request.form['user_input']
    sessionid = session.get('sessionid')
    bot_response = b.respond(user_input, sessionid)
    return render_template('index_novo.html', user_input=user_input, bot_response=bot_response)



if __name__ == "__main__":
    app.run()