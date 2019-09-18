import json
import requests

from flask import Flask, render_template, request, session
from flask_session import Session
from random import *
import db
from botty import Botty
from werkzeug.wsgi import responder

from programy.clients.events.console.client import ConsoleBotClient
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.programy import ProgramyConfiguration
from programy.clients.args import CommandLineClientArguments

app = Flask(__name__)
app.secret_key = 'any random string'

class MyEmbeddedBot(ConsoleBotClient):

    def __init__(self, config_filename):
        self._config_filename = config_filename
        ConsoleBotClient.__init__(self, "Console")

    def parse_arguments(self, argument_parser):
        client_args = CommandLineClientArguments(self, parser=None)
        return client_args

    def load_configuration(self, arguments):

        client_config = self.get_client_configuration()
        self._configuration = ProgramyConfiguration(client_config)

        yaml_file = YamlConfigurationFile()
        yaml_file.load_from_file(self._config_filename, client_config, ".")

my_bot = MyEmbeddedBot("config.yaml")
client_context = my_bot.create_client_context("testuser")


@app.route("/")
def index():
    sessionid = randint(1000,10000)
    session['sessionid'] = sessionid
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    entrada = request.args.get('msg')
    sessionid = session.get('sessionid')
    response = my_bot.process_question(client_context, entrada)
    return str(response)


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/process',methods=['POST'])
def process():
    user_input=request.form['user_input']
    sessionid = session.get('sessionid')


if __name__ == "__main__":
    app.run()