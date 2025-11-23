import sqlite3
import re

class Conta:

    """Operações relacionadas à criação de contas de utilizador."""

    @staticmethod
    def conectar_bd():

        """Abre uma ligação à base de dados.

        Returns:
            sqlite3.Connection: Conexão à base de dados RentACar.
        """

        conn = sqlite3.connect('Bd/RentACar.db')
        return conn


    @staticmethod
    def validar_email(email: str) -> bool:

        """Valida o formato do email. Args: email (str): Email a ser validado.  Returns: bool: True se o email for válido, False caso contrário."""

        padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(padrao, email) is not None


    @staticmethod
    def validar_password(password: str) -> bool:

        """Valida a password.

        Args:
            password (str): Password a validar.

        Returns:
            bool: True se tiver pelo menos 6 caracteres, False caso contrário.
        """

        return len(password) >= 6


    @staticmethod
    def criar_conta() -> dict:

        """Cria uma nova conta de utilizador na base de dados.

        Pede dados ao utilizador pelo terminal, valida email e password
        e regista o utilizador na tabela `users`.

        Returns:
            dict: Dicionário com 'nome' e 'email' se a criação tiver sucesso,
            ou dicionário vazio em caso de erro.
        """


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




