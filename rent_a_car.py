import subprocess
import sys
from os import system


def display_menu(menu):

    for k, function in menu.items():
        print(k, function.__name__)


def CriarConta():
    print("you have selected menu option one") # Simulate function output.
    input("Press Enter to Continue\n")
    system('cls')
    subprocess.run(["python", "CriarConta.py"])
    


def Log_in():
    print("you have selected menu option two") # Simulate function output.
    input("Press Enter to Continue\n")
    system('cls')  # clears stdout


def Alugar_Veiculo():
    print("you have selected menu option three") # Simulate function output.
    input("Press Enter to Continue\n")
    system('cls')  # clears stdout


def Fechar():
    system('cls')  
    print("Goodbye")
    sys.exit()


def main():
 
    functions_names = [CriarConta, Log_in, Alugar_Veiculo, Fechar]
    menu_items = dict(enumerate(functions_names, start=1))

    while True:
        display_menu(menu_items)
        selection = int(
            input("Please enter your selection number: "))  # Get function key
        selected_value = menu_items[selection]  # Gets the function name
        selected_value()  # add parentheses to call the function


if __name__ == "__main__":
    main()