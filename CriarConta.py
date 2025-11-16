

def validar_email(email: str) -> bool:
    return "@" in email and "." in email


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

    dados = {
        "nome": nome,
        "email": email,
        "password": password 
    }

    print("\n Conta criada com sucesso.")
    return dados



    
