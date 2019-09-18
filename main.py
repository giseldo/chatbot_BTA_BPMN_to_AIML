from programy.clients.restful.client import RestBotClient
from flask import Flask, jsonify, request, make_response, abort, Response, render_template

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


app = Flask(__name__)

REST_CLIENT = None

print("Initiating Flask REST Service...")

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

if __name__ == '__main__':
    app.run()
