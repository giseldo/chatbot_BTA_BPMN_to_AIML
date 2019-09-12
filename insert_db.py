import sqlite3

conn = sqlite3.connect("chatbot.db")

cursor = conn.cursor()

cursor.execute("insert into log values (1, 'oi', 'ola', '2003-06-25')")

conn.commit()

conn.close()