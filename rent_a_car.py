import subprocess
import sys
from os import system
from AlugarVeiculo import Alugar


def display_menu(menu):
    system('cls')
    print("\n==============================")
    print("       MENU RENT A CAR          ")
    print("==============================\n")
    for key, (descricao, _) in menu.items():
        print(f"{key} - {descricao}")
    print()


def CriarConta():
    print("\nEscolheu a opção: Criar Conta") 
    input("Pressione ENTER para continuar...")
    system('cls')

def Log_in():
    print("\nEscolheu a opção: Iniciar Sessão") 
    input("Pressione ENTER para continuar...")
    system('cls') 
    subprocess.run(["python", "LogIn.py"]) 

def Alugar_Veiculo():
    print("\nEscolheu a opção: Alugar Veículo") 
    input("Pressione ENTER para continuar...")
    system('cls') 
    Alug = Alugar()
    Alug.executar() 

def Fechar():
    system('cls')  
    print("\nObrigado por usar o Rent A Car! Até logo ")
    sys.exit()


def main():
    
    menu_items = {
        1: ("Criar Conta", CriarConta),
        2: ("Iniciar Sessão", Log_in),
        3: ("Alugar Veículo", Alugar_Veiculo),
        4: ("Fechar Programa", Fechar)
    }

    while True:
        display_menu(menu_items)
        try:
            selection = int(input("Por favor, escolha uma opção: "))
            item = menu_items.get(selection)
            if item:
                descricao, func = item
                func()
            else:
                print("\n Opção inválida. Tente novamente.\n")
                input("Pressione ENTER para continuar...")
        except ValueError:
            print("\n Por favor insira um número válido.\n")
            input("Pressione ENTER para continuar...")

# Executa o menu
if __name__ == "__main__":
    main()
