import aiml
import os


kernel = aiml.Kernel()
if os.path.isfile("bot_brain.brn"):
    kernel.bootstrap(brainFile="bot_brain.brn")
else:
    kernel.bootstrap(learnFiles="aiml/config.xml", commands="CEREBRO")
    kernel.saveBrain("bot_brain.brn")


def respond(entrada, sessionid):
    return kernel.respond(entrada, sessionid)