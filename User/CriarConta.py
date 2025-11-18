import sqlite3
import re

class Conta:
    @staticmethod
    def conectar_bd():
        conn = sqlite3.connect('Bd/RentACar.db')
        return conn


    @staticmethod
    def validar_email(email: str) -> bool:
        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email) is not None


    @staticmethod
    def validar_password(password: str) -> bool:
        return len(password) >= 6


    @staticmethod
    def criar_conta() -> dict:
        print("\n=== Criar Conta ===")

        nome = input("Nome completo: ").strip()

        email = input("Email: ").strip()
        while not Conta.validar_email(email):
            print("Email inválido. Tenta novamente.")
            email = input("Email: ").strip()

        password = input("Password (mín. 6 caracteres): ").strip()
        while not Conta.validar_password(password):
            print("Password demasiado curta.")
            password = input("Password: ").strip()

        conn = Conta.conectar_bd()
        cursor = conn.cursor()

        resultado = {}
        try:
            cursor.execute("""
                INSERT INTO users (nome, email, password, is_admin)
                VALUES (?, ?, ?, 0)
                """, (nome, email, password))
            conn.commit()
            print("\nConta criada com sucesso!")
            resultado = {"nome": nome, "email": email}
        except sqlite3.IntegrityError as e:
            print(f"Erro: {e}")
            print("Pode ser que o email já exista na base de dados.")
        finally:
            conn.close()

        input("Pressione ENTER para voltar ao menu...")
        return resultado




