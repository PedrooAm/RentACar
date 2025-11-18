import sqlite3
import re

def conectar_bd():
    conn = sqlite3.connect('RentACar.db')
    return conn


def validar_email(email: str) -> bool:
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None


def validar_password(password: str) -> bool:
    return len(password) >= 6


def criar_conta() -> dict:
    print("\n=== Criar Conta ===")

    nome = input("Nome completo: ").strip()

    email = input("Email: ").strip()
    while not validar_email(email):
        print("Email inválido. Tenta novamente.")
        email = input("Email: ").strip()

    password = input("Password (mín. 6 caracteres): ").strip()
    while not validar_password(password):
        print("Password demasiado curta.")
        password = input("Password: ").strip()

    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (nome, email, password, is_admin)
            VALUES (?, ?, ?, 0)
        """, (nome, email, password))
        conn.commit()
        print("\n Conta criada com sucesso!")
    except sqlite3.IntegrityError as e:
        print(f" Erro: {e}")
        print("Pode ser que o email já exista na base de dados.")
    finally:
        conn.close()

    input("Pressione ENTER para voltar ao menu...")



    
