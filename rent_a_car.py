
import sys
from os import system
from AlugarVeiculo import Alugar
from User.CriarConta import Conta
from User.LogIn import  Login
from GerirReserva import GerirReservas

login_system = Login()
session_user = None


def display_menu(menu):
    system('cls')
    print("\n==============================")
    print("       MENU RENT A CAR          ")
    print("==============================\n")

    if session_user and isinstance(session_user, dict):
        print(f"Utilizador: {session_user.get('nome')} | Email: {session_user.get('email')}\n")
    else:
        print("Utilizador: Não autenticado\n")

    for key, (descricao, _) in menu.items():
        print(f"{key} - {descricao}")
    print()


def CriarConta():
    print("\nEscolheu a opção: Criar Conta") 
    input("Pressione ENTER para continuar...")
    system('cls')
    criar = Conta()
    criar.criar_conta()

def Log_in():
    global session_user , login_system
    print("\nEscolheu a opção: Iniciar Sessão") 
    input("Pressione ENTER para continuar...")
    system('cls')
    log = Login() 
    session_user = log.autenticar()
    if session_user: 
        session_user = log.session_user
        login_system = log
        print("Sessão iniciada com sucesso!, para voltar ao menu principal... ")
    else:
        print("Falha ao iniciar sessão. A voltar ao menu principal... ")    
    input("Pressione ENTER...")
    system('cls')
   
    

def Alugar_Veiculo():
    print("\nEscolheu a opção: Alugar Veículo") 
    input("Pressione ENTER para continuar...")
    system('cls')
    Alug = Alugar()
    Alug.menu()

def Gerir_Reservas():
    print("\nEscolheu a opção: Gerir Reservas") 
    input("Pressione ENTER para continuar...")
    system('cls')
    Gerir = GerirReservas()
    Gerir.menu(user_id=session_user.get("id"))
     

def Fechar():
    system('cls')  
    print("\nObrigado por usar o Rent A Car! Até logo ")
    sys.exit()


def main():
    while True:
         
        menu_items = {
            "1": ("Criar Conta", CriarConta),
            "2": ("Iniciar Sessão", Log_in),
        }

        
        if session_user and isinstance(session_user, dict):
            menu_items["3"] = ("Alugar Veículo", Alugar_Veiculo)
            
            if session_user.get("is_admin"):
                menu_items["4"] = ("Gerir Reservas (Admin)", Gerir_Reservas)
                menu_items["5"] = ("Fechar Programa", Fechar)
            else:
                menu_items["4"] = ("Fechar Programa", Fechar)

        else:
            menu_items["3"] = ("Fechar Programa", Fechar)

        display_menu(menu_items)
        selection = input("Por favor, escolha uma opção: ").strip()
        item = menu_items.get(selection)
        if item:
            descricao, func = item
            func()
        else:
            print("\nOpção inválida. Tente novamente.\n")
            input("Pressione ENTER para continuar...")
            system('cls')


if __name__ == "__main__":
    main()
