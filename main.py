import json
import requests

from flask import Flask, render_template, request, session
from flask_session import Session
from random import *
import db
from botty import Botty
from werkzeug.wsgi import responder

app = Flask(__name__)
app.secret_key = 'any random string'


@app.route("/")
def index():
    sessionid = randint(1000,10000)
    session['sessionid'] = sessionid
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    entrada = request.args.get('msg')
    sessionid = session.get('sessionid')
    response = requests.get("http://127.0.0.1:8989/api/rest/v1.0/ask?question={}&userid=root".format(entrada))
    comments = json.loads(response.content)

    for resultados, y in comments[0].items():
        saida = y["answer"]

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


if __name__ == "__main__":
    app.run()