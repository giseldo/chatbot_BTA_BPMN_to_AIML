from aiml2 import Kernel

kernel = Kernel("config.xml")
contexto = kernel.create_client_context("root")

while True:
    entrada = input("user>>> ")
    saida = kernel.process_question(contexto, entrada)
    print("bot>>> {}".format(saida))