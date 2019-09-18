

from flask import Flask, render_template, request, session
from random import *
from programy.utils.logging.ylogger import YLogger
from programy.clients.events.client import EventBotClient
from programy.clients.events.console.config import ConsoleConfiguration

app = Flask(__name__)
app.secret_key = 'any random string'


class MockArgumentsGiseldo(object):

    def __init__(self,
                    bot_root = ".",
                    logging = None,
                    config  = 'config.yaml',
                    cformat = "yaml",
                    noloop = False,
                    substitutions='subs.txt'
                ):
        self.bot_root = bot_root
        self.logging = logging
        self.config = config
        self.cformat = cformat
        self.noloop = noloop
        self.substitutions = substitutions


class MockArgumentParserGiseldo(object):

    def add_argument(self, argument, dest=None, action=None, help=None):
        pass

    def parse_args(self):
        return MockArgumentsGiseldo()


class MockClientGiseldo(object):

    def get_description(self):
        return "MockClient"

    def add_client_arguments(self, parser):
        pass

    def parse_args(sel, arguments, parsed_args):
        pass



class ConsoleBotClientGiseldo(EventBotClient):

    def __init__(self, argument_parser=None):
        self.running = False
        c = MockArgumentParserGiseldo()
        EventBotClient.__init__(self, "Console", c)

    def get_client_configuration(self):
        return ConsoleConfiguration()

    def add_client_arguments(self, parser=None):
        return

    def parse_args(self, arguments, parsed_args):
        return

    def get_question(self, client_context, input_func=input):
        ask = "%s " % self.get_client_configuration().prompt
        return input_func(ask)

    def display_startup_messages(self, client_context):
        self.process_response(client_context, client_context.bot.get_version_string(client_context))
        initial_question = client_context.bot.get_initial_question(client_context)
        self._renderer.render(client_context, initial_question)

    def process_question(self, client_context, question):
        self._questions += 1
        return client_context.bot.ask_question(client_context , question, responselogger=self)

    def render_response(self, client_context, response):
        # Calls the renderer which handles RCS context, and then calls back to the client to show response
        self._renderer.render(client_context, response)

    def process_response(self, client_context, response):
        print(response)

    def process_question_answer(self, client_context):
        question = self.get_question(client_context)
        response = self.process_question(client_context, question)
        self.render_response(client_context, response)

    def wait_and_answer(self):
        running = True
        try:
            client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
            self.process_question_answer(client_context)
        except KeyboardInterrupt as keye:
            running = False
            client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
            self._renderer.render(client_context, client_context.bot.get_exit_response(client_context))
        except Exception as excep:
            YLogger.exception(self, "Oops something bad happened !", excep)
        return running

    def prior_to_run_loop(self):
        client_context = self.create_client_context(self._configuration.client_configuration.default_userid)
        self.display_startup_messages(client_context)


my_bot = ConsoleBotClientGiseldo()
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