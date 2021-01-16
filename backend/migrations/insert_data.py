import sqlite3

connection = sqlite3.connect('MyRecipes.db')
cursor = connection.cursor()

input_name = input('Nome: ')
input_email = input('Email: ')
input_senha = input('Senha: ')

cursor.executemany("""
INSERT INTO users (nome, email, senha)
VALUES (?,?,?)
""", input_name, input_email, input_senha)

connection.commit()
connection.close()