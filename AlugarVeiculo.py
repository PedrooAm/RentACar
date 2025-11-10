import subprocess
import sys
from os import system

from Carros import Carros 

class Alugar:
    def __init__(self):
       
        self.menu_items = {
            1: self.listar_carros_disponiveis,
            2: self.voltar_ao_main,
            3: self.fechar
        }

    def display_menu(self):
        
        print("\n===== MENU RENT A CAR =====")
        for key, func in self.menu_items.items():
            print(f"{key} - {func.__name__}")

    def listar_carros_disponiveis(self):
        
        print("Escolheu a opção 1")
        input("Clique ENTER para continuar\n")
        system('cls')  
        carros = Carros()
        carros.executar()

    def voltar_ao_main(self):
       
        print("Escolheu a opção 2")
        input("Clique ENTER para continuar\n")
        system('cls')
        subprocess.run(["python", "rent_a_car.py"])

    def fechar(self):
      
        system('cls')
        print("Adeus!")
        sys.exit()
        
        while True:
            self.display_menu()
            try:
                selection = int(input("Por favor escolha uma opção: "))
                action = self.menu_items.get(selection)
                if action:
                    action()
                else:
                    print("Opção inválida. Tente novamente.\n")
            except ValueError:
                print("Por favor insira um número válido.\n")



