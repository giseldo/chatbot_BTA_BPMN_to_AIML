import sqlite3

conn = sqlite3.connect("chatbot.db")

cursor = conn.cursor()

cursor.execute("create table log (sessionid int, entrada varchar(40), saida varchar(400), hora timestamp)")

conn.close()