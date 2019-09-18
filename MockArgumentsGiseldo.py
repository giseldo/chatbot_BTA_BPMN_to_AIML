import unittest
import os



from programy.clients.args import ClientArguments
from programy.clients.args import CommandLineClientArguments


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



