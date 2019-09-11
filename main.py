from flask import Flask, render_template, request, session

import aiml
from random import *

app = Flask(__name__)
app.secret_key = 'any random string'

kernel = aiml.Kernel()
kernel.learn("aiml/config.xml")
kernel.respond("CEREBRO")


@app.route("/")
def home():
    sessionid = randint(100,1000)
    session['sessionid'] = sessionid
    print("home: {}".format(sessionid))
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    print("userText: {}".format(userText))
    sessionid = session.get('sessionid')
    print("get: {}".format(sessionid))
    saida = kernel.respond(userText, sessionid)
    return str(saida)


if __name__ == "__main__":
    app.run()