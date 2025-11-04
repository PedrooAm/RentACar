import sqlite3

conn = sqlite3.connect("RentACar.sqlite")
cursor = conn.cursor()

# Apaga a tabela antiga se existir
cursor.execute("DROP TABLE IF EXISTS users")

# Cria a nova tabela users (só com username e password)
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("TA FETO!")

