import subprocess
import sys
from os import system

from AlugarVeiculo import Alugar



def display_menu(menu):


    print("\n===== MENU RENT A CAR ===== \U0001F697")
  
    for k, (descricao,_) in menu.items():
        print(f"{k} -{descricao}" )


def CriarConta():
    print("Escolheu a opcão 1") 
    input("Clique ENTER para continuar\n")
    system('cls')
   
    


def Log_in():
    print("Escolheu a opção 2") 
    input("Clique ENTER para continuar\n")
    system('cls') 
    subprocess.run(["python", "LogIn.py"]) 


def Alugar_Veiculo():
    print("Escolheu a opção 3") 
    input("Clique ENTER para continuar\n")
    system('cls') 
    Alug = Alugar()
    Alug.executar()
    


def Fechar():
    system('cls')  
    print("Adeus!")
    sys.exit()


def main():
 
    menu_items = {
            1: ("Criar Conta",CriarConta),
            2: ("Iniciar Sessão",Log_in),
            3: ("Alugar Veiculo",Alugar_Veiculo),
            4: ("Fechar",Fechar)
        }

    while True:
        display_menu(menu_items)
        try:
            selection = int(input("Por favor escolha uma opção: "))
            item = menu_items.get(selection)
            if item:
                descricao, func = item  
                func()                  
            else:
                print("Opção inválida.\n")
        except ValueError:
            print("Por favor insira um número válido.\n")


if __name__ == "__main__":
    main()