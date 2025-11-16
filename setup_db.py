import sqlite3

def setup_db():
    # Conectar ao banco de dados SQLite (ele será criado se não existir)
    conn = sqlite3.connect('RentACar.sqlite')
    cursor = conn.cursor()

    # Criar a tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('admin', 'user')) DEFAULT 'user'
    );
    ''')

    # Criar a tabela de carros
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marca TEXT NOT NULL,
        modelo TEXT NOT NULL,
        matricula TEXT NOT NULL UNIQUE
    );
    ''')

    # Inserir um admin padrão, caso ainda não tenha
    cursor.execute('''
    INSERT OR IGNORE INTO users (username, password, role)
    VALUES ('admin', 'admin123', 'admin');
    ''')

    # Inserir carros de exemplo
    carros_exemplo = [
        ('Fiat', 'Punto', 'AB-123-CD'),
        ('Volkswagen', 'Golf', 'XY-456-ZZ'),
        ('BMW', 'X5', 'LM-789-PO'),
        ('Audi', 'A3', 'GH-101-QW'),
        ('Toyota', 'Corolla', 'JK-202-RT')
    ]

    cursor.executemany('''
    INSERT OR IGNORE INTO cars (marca, modelo, matricula)
    VALUES (?, ?, ?);
    ''', carros_exemplo)

    # Commit e fechar conexão
    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_db()
