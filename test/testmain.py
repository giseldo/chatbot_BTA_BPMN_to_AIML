import aiml
import time

kernel = aiml.Kernel()
kernel.learn("aiml/config.xml")
kernel.respond("CEREBRO")

print("bot>>> {}".format("Comece falando: oi."))

while True:
    entrada = input("user>>> ")
    saida = kernel.respond(entrada)
    sentences = quebralinha(saida)
    for s in sentences:
        time.sleep(1)
        print("bot>>> {}".format(s))
