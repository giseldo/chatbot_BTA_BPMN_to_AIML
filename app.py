from flask import Flask, render_template, request
import aiml
from util import quebralinha

app = Flask(__name__)


kernel = aiml.Kernel()
kernel.learn("config.xml")
kernel.respond("CEREBRO")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    saida = kernel.respond(userText)
    return str(saida)


if __name__ == "__main__":
    app.run()