import sys
from os import system

from Carros import Carros 

class Alugar:
    def __init__(self):
       
        self.menu_items = {
            1: ("Listar carros disponiveis", self.listar_carros_disponiveis),
            2: ("Voltar ao menu principal", self.voltar_ao_main),
            3: ("Encerrar", self.fechar)
        }

    def display_menu(self):
        system('cls')
        print("\n===== MENU ALUGAR VEÍCULO =====")
        for key, (descricao, _) in self.menu_items.items():
            print(f"{key} - {descricao}")

    def listar_carros_disponiveis(self):
        print("Escolheu a opção 1")
        input("Clique ENTER para continuar\n")
        system('cls')
        carros = Carros()
        carros.Listar()
        input("\nPressione ENTER para voltar ao menu de Alugar...")

    def voltar_ao_main(self):
        print("Escolheu a opção 2")
        input("Clique ENTER para continuar\n")
        system('cls')
        return

    def menu(self):
    
        while True:
            self.display_menu()
            selection_str = input("Por favor escolha uma opção: ").strip()
            try:
                selection = int(selection_str)
            except ValueError:
                print("Por favor insira um número válido.\n")
                input("Pressione ENTER para continuar...")
                continue

            item = self.menu_items.get(selection)
            if not item:
                print("Opção inválida. Tente novamente.\n")
                input("Pressione ENTER para continuar...")
                continue

            descricao, func = item
            if func == self.voltar_ao_main:
                func()
                return  
            func()

    def fechar(self):
        system('cls')
        print("Adeus!")
        sys.exit()





