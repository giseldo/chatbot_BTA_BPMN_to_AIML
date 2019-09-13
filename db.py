import sqlite3
import datetime


def inserir(sessionid, entrada, saida):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()
    datetime_object = datetime.datetime.now()
    cursor.execute("insert into log values (?, ?, ?, ?)", (sessionid, entrada, saida, datetime_object))
    conn.commit()
    conn.close()