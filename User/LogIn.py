import sqlite3
import msvcrt

DB_NAME = "Bd/RentACar.db"

class AuthBase:

    """Classe base para operações de autenticação.

    Args:
        db_name (str): Caminho da base de dados.
    """

    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name

    def conectar(self):

        """Abre uma ligação à base de dados.

        Returns:
            sqlite3.Connection: Conexão ativa à BD.
        """

        return sqlite3.connect(self.db_name)

    def buscar_utilizador(self, nome_ou_email):

        """Procura um utilizador pelo nome ou email.

        Args:
            nome_ou_email (str): Nome ou email a procurar.

        Returns:
            tuple | None: Dados do utilizador (id, nome, email, password, is_admin)
            ou None se não existir.
        """

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nome, email, password, is_admin FROM users WHERE nome=? OR email=?",
            (nome_ou_email, nome_ou_email)
        )
        resultado = cursor.fetchone()
        conn.close()
        return resultado

class Login(AuthBase):

    """Gerencia a autenticação de utilizadores.

    Args:
        db_name (str): Caminho da base de dados.
    """

    def __init__(self, db_name: str = DB_NAME):
        super().__init__(db_name)
        self.session_user = None

    def input_password(self, prompt: str = "Password: "):

        """Lê a password com ocultação de caracteres.

        A tecla TAB alterna entre mostrar/esconder a password.

        Args:
            prompt (str): Texto exibido antes da password.

        Returns:
            str: Password digitada pelo utilizador.
        """

        password = ""
        mostrar = False
        print(prompt, end="", flush=True)

        while True:
            tecla = msvcrt.getch()
            if tecla in (b'\r', b'\n'):
                print()
                break
            elif tecla == b'\x08':  
                if len(password) > 0:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            elif tecla == b'\t':  
                mostrar = not mostrar
                print("\r" + prompt + (password if mostrar else "*" * len(password)), end="", flush=True)
            elif tecla in b'\x00\xe0':  
                msvcrt.getch()
            else:
                try:
                    caractere = tecla.decode()
                except:
                    continue
                password += caractere
                print(caractere if mostrar else "*", end="", flush=True)

        return password

    def autenticar(self):

        """Realiza o processo de login de um utilizador.

        Solicita nome/email + password e verifica na base de dados.

        Returns:
            bool: True se autenticado com sucesso, False caso contrário.
        """

        print("=== Login ===")
        utilizador_input = input("Nome ou Email: ").strip()
        password_input = self.input_password("Password (Tab para mostrar/esconder): ")

        utilizador = self.buscar_utilizador(utilizador_input)

        if utilizador is None:
            print("Utilizador não encontrado!")
            return False

        uid, nome, email, password_db, is_admin = utilizador

        if password_input == password_db:
            self.session_user = {
                "id": uid,
                "nome": nome,
                "email": email,
                "is_admin": bool(is_admin)
            }
            print(f"Bem-vindo(a), {nome}!")
            return True
        else:
            print("Password incorreta!")
            return False
