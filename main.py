from flask import Flask, render_template, request, session
from programy.utils.logging.ylogger import YLogger
from programy.clients.events.client import EventBotClient
from programy.clients.events.console.config import ConsoleConfiguration
from flask import Flask, jsonify, request, make_response, abort, Response
from programy.clients.restful.client import RestBotClient

app = Flask(__name__)
app.secret_key = 'any random string'


class MockArgumentsGiseldo(object):

    def __init__(self,
                    bot_root = ".",
                    logging = None,
                    config  = 'config.flask.rest.yaml',
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


class FlaskRestBotClient(RestBotClient):

    def __init__(self, id, argument_parser=None):
        c = MockArgumentParserGiseldo()
        RestBotClient.__init__(self, id, c)
        self.initialise()

    def server_abort(self, message, status_code):
        abort(Response(message), status_code)

    def create_response(self, response_data, status_code, version=1.0):
        if self.configuration.client_configuration.debug is True:
            self.dump_request(response_data)

        if version == 1.0:
            return make_response(jsonify(response_data, status_code))
        elif version == 2.0:
            return make_response(jsonify(response_data), status_code)
        else:
            return make_response('Invalid API version', 400)

    def run(self, flask):

        print("%s Client running on http://%s:%s" % (self.id, self.configuration.client_configuration.host,
                                              self.configuration.client_configuration.port))

        self.startup()

        if self.configuration.client_configuration.debug is True:
            print("%s Client running in debug mode" % self.id)

        if self.configuration.client_configuration.ssl_cert_file is not None and \
                self.configuration.client_configuration.ssl_key_file is not None:
            context = (self.configuration.client_configuration.ssl_cert_file,
                       self.configuration.client_configuration.ssl_key_file)

            print("%s Client running in https mode" % self.id)
            flask.run(host=self.configuration.client_configuration.host,
                      port=self.configuration.client_configuration.port,
                      debug=self.configuration.client_configuration.debug,
                      ssl_context=context)
        else:
            print("%s Client running in http mode, careful now !" % self.id)
            flask.run(host=self.configuration.client_configuration.host,
                      port=self.configuration.client_configuration.port,
                      debug=self.configuration.client_configuration.debug)

        self.shutdown()


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


if __name__ == '__main__':

    REST_CLIENT = None

    print("Initiating Flask REST Service...")
    app = Flask(__name__)


    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route('/api/rest/v1.0/ask', methods=['GET', 'POST'])
    def ask_v1_0():
        response_data, status = REST_CLIENT.process_request(request, version=1.0)
        return REST_CLIENT.create_response(response_data, status, version=1.0)

    @app.route('/api/rest/v2.0/ask', methods=['GET', 'POST'])
    def ask_v2_0():
        response_data, status = REST_CLIENT.process_request(request, version=2.0)
        return REST_CLIENT.create_response(response_data, status, version=2.0)

    print("Loading, please wait...")
    REST_CLIENT = FlaskRestBotClient("flask")
    REST_CLIENT.run(app)
