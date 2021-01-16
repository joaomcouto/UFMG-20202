import sqlite3

connection = sqlite3.connect('MyRecipes.db')
cursor = connection.cursor()

lista = [
    ('Pedro', 'pedro@gmail.com', '123.qwe'),
    ('Vinicius', 'vinicius@gmail.com', '123.qwe'),
    ('Vitor', 'vitor@gmail.com', '123.qwe')
]

cursor.executemany("""
INSERT INTO users (nome, email, senha)
VALUES (?,?,?)
""", lista)

connection.commit()

connection.close()