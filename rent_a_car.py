import subprocess
import sys
from os import system


def display_menu(menu):

    for k, function in menu.items():
        print(k, function.__name__)


def CriarConta():
    print("Escolheu a opcão 1") 
    input("Clique ENTER para continuar\n")
    system('cls')
    subprocess.run(["python", "CriarConta.py"])
    


def Log_in():
    print("Escolheu a opção 2") 
    input("Clique ENTER para continuar\n")
    system('cls') 
    subprocess.run(["python", "LogIn.py"]) 


def Alugar_Veiculo():
    print("Escolheu a opção 3") 
    input("Clique ENTER para continuar\n")
    system('cls') 
    subprocess.run(["python", "Alugar.py"]) 


def Fechar():
    system('cls')  
    print("Adeus!")
    sys.exit()


def main():
 
    functions_names = [CriarConta, Log_in, Alugar_Veiculo, Fechar]
    menu_items = dict(enumerate(functions_names, start=1))

    while True:
        display_menu(menu_items)
        selection = int(
            input("Por favor escolha uma opção: "))  
        selected_value = menu_items[selection]  
        selected_value()  


if __name__ == "__main__":
    main()