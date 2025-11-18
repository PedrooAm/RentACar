import sqlite3
import msvcrt

DB_NAME = "Bd/RentACar.db"

def conectar():
    return sqlite3.connect(DB_NAME)

def buscar_usuario(nome_ou_email):
    """Busca usuário pelo nome ou email na tabela 'users'."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nome, email, password FROM users WHERE nome=? OR email=?",
        (nome_ou_email, nome_ou_email)
    )
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def input_password(prompt="Password: "):
    """Lê a password com asteriscos, permite mostrar/esconder com Tab."""
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
            caractere = tecla.decode()
            password += caractere
            print(caractere if mostrar else "*", end="", flush=True)

    return password

def login():
    print("=== Login ===")
    usuario_input = input("Nome ou Email: ").strip()
    password_input = input_password("Password (Tab para mostrar/esconder): ")

    usuario = buscar_usuario(usuario_input)

    if usuario is None:
        print("Usuário não encontrado!")
        return False

    _, nome, email, password_db = usuario

    if password_input == password_db:
        print(f"Bem-vindo(a), {nome}!")
        return True
    else:
        print("Password incorreta!")
        return False

if __name__ == "__main__":
    login()
