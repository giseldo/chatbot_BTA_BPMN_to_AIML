"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import uuid
import datetime

from programy.utils.logging.ylogger import YLogger

from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from flask import abort
from flask import current_app

from programy.clients.restful.flask.client import FlaskRestBotClient
from programy.clients.restful.flask.webchat.config import WebChatConfiguration
from programy.clients.render.html import HtmlRenderer
from programy.clients.restful.auth import RestAuthorizationHandler

class MockArgumentsGiseldo(object):

    def __init__(self,
                    bot_root = ".",
                    logging = None,
                    config  = 'config/config.webchat.yaml',
                    cformat = "yaml",
                    noloop = False,
                    substitutions=None
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


class WebChatBotClient(FlaskRestBotClient):

    def __init__(self, argument_parser=None):
        c = MockArgumentParserGiseldo()
        FlaskRestBotClient.__init__(self, "WebChat", c)
        self._authorization = RestAuthorizationHandler.load_authorisation(self)

    def get_client_configuration(self):
        return WebChatConfiguration()

    def get_default_renderer(self):
        return HtmlRenderer()

    def unauthorised_access_response(self, error_code=401):
        return make_response(jsonify({'error': 'Unauthorized access'}), error_code)

    def get_question(self, request):
        if 'question' in request.args:
            return request.args['question']
        return None

    def get_userid(self, request):
        userid = request.cookies.get(self.configuration.client_configuration.cookie_id)
        if userid is None:
            userid = str(uuid.uuid4().hex)
            YLogger.debug(self, "Setting userid cookie to :%s" % userid)
        else:
            YLogger.debug(self, "Found userid cookie : %s" % userid)
        return userid

    def get_userid_cookie_expirary_date(self, duration):
        expire_date = datetime.datetime.now()
        expire_date = expire_date + datetime.timedelta(days=duration)
        return expire_date

    def create_success_response_data(self, question, answer):
        return {"question": question, "answer": answer}

    def get_default_response(self, client_context):
        return client_context.bot.default_response

    def create_error_response_data(self, client_context, question, error):
        return {"question": question,
                "answer": self.get_default_response(client_context),
                "error": error
                }

    def create_response(self, response_data, userid, userid_expire_date):
        response = jsonify({'response': response_data})
        response.set_cookie(self.configuration.client_configuration.cookie_id, userid, expires=userid_expire_date)
        return response

    def get_answer(self, client_context, question):
        if question == 'YINITIALQUESTION':
            answer = client_context.bot.get_initial_question(client_context)
        else:
            self._questions += 1
            answer = client_context.bot.ask_question(client_context, question, responselogger=self)
        return answer

    def receive_message(self, request):

        if self._authorization is not None:
            if self._authorization.authorise(request) is False:
                abort(403)

        if self._api_keys is not None:
            if self._api_keys.use_api_keys():
                if self._api_keys.verify_api_key_usage(request) is False:
                    abort(403)

        question = self.get_question(request)
        if question is None:
            YLogger.error(self, "'question' missing from request")
            abort(400)

        userid = self.get_userid(request)

        userid_expire_date = self.get_userid_cookie_expirary_date(self.configuration.client_configuration.cookie_expires)

        client_context = self.create_client_context(userid)
        try:
            answer = self.get_answer(client_context, question)
            answer = answer.replace('\n', '').strip()
            rendered = self._renderer.render(client_context, answer)
            response_data = self.create_success_response_data(question, rendered)
            # response_data = {'question': 'YINITIALQUESTION',
            #                  'answer': ['Olá, meu nome é Tips, em que posso ajudá-lo?', 'foi agora']}
        except Exception as excep:
            YLogger.exception(self, "Failed receving message", excep)
            response_data = self.create_error_response_data(client_context, question, str(excep))

        return self.create_response(response_data, userid, userid_expire_date)


app = Flask(__name__)

WEB_CLIENT = WebChatBotClient()


@app.route('/')
def index():
    return current_app.send_static_file('webchat.html')


@app.route(WEB_CLIENT.configuration.client_configuration.api, methods=['GET'])
def receive_message():
    try:
        return WEB_CLIENT.receive_message(request)
    except Exception as e:
        print("Error receiving webchat message", e)
        YLogger.exception(None, "Web client error", e)
        return "500"


if __name__ == '__main__':
    app.run(host='127.0.0.1')
