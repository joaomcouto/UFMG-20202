import sqlite3

conn = sqlite3.connect('users.db')
print("conectado")
conn.close()
