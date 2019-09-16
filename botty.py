import aiml
import os

class botty():
    kernel = None
    def __init__(self):
        self.kernel = aiml.Kernel()
        if os.path.isfile("bot_brain.brn"):
            self.kernel.bootstrap(brainFile="bot_brain.brn")
        else:
            self.kernel.bootstrap(learnFiles="aiml/config.xml", commands="CEREBRO")
            self.kernel.saveBrain("bot_brain.brn")

    def responder_novo(entrada_, sessionid_):
        return self.kernel.respond(input_= entrada_, sessionID = sessionid_)