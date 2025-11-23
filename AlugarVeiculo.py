"""Módulo de aluguer de veículos.

Este módulo implementa o fluxo de aluguer de veículos para um utilizador
autenticado no sistema Rent A Car. As principais funcionalidades incluem:

- Apresentar um menu específico de aluguer
- Listar carros disponíveis para aluguer
- Registar o aluguer de um veículo
- Consultar alugueres activos do utilizador
- Cancelar um aluguer existente
- Voltar ao menu principal do programa
"""



import sys
from os import system
import sqlite3
from Services.Carros import Carros 

class Alugar:

    """Gerencia o processo de aluguer de veículos para um utilizador.

    Args:
        user_id (int): ID do utilizador autenticado.
    """

    def __init__(self,user_id):
        self.user_id = user_id
        self.menu_items = {
            1: ("Listar carros disponiveis", self.listar_carros_disponiveis),
            2: ("Consultar Aluguel",self.consultar_aluguel),          
            3: ("Voltar ao menu principal", self.voltar_ao_main),
           
        }

    def conectar(self):

        """Estabelece conexão com a base de dados.

        Returns:
            sqlite3.Connection: Conexão aberta com o ficheiro da BD.
        """

        return sqlite3.connect("Bd/RentACar.db")
    
    def display_menu(self):

        """Mostra o menu de opções do módulo de aluguer."""

        system('cls')
        print("\n===== MENU ALUGAR VEÍCULO =====")
        for key, (descricao, _) in self.menu_items.items():
            print(f"{key} - {descricao}")

    def listar_carros_disponiveis(self):

        """Mostra carros disponíveis e permite ao utilizador alugar um veículo."""

        system('cls')
        carros = Carros()
        lista = carros.listar_disponiveis()
        if not lista:
            print("Não há carros disponíveis.")
            input("\nPressione ENTER para voltar...")
            system('cls')
            return

        print("\nCarros disponíveis:\n")
        for idx, (marca, modelo, matricula, preco_dia, *rest) in enumerate(lista, start=1):
            print(f"{idx}. {marca} {modelo} | Matrícula: {matricula} | Preço/dia: {preco_dia} EUR")

        print("\n0 - Cancelar")
        escolha_str = input("\nEscolha o número do carro que deseja alugar: ").strip()
        if escolha_str == "0" or escolha_str == "":
            system('cls')
            return
        try:
            escolha = int(escolha_str)
            if escolha < 1 or escolha > len(lista):
                raise ValueError
        except ValueError:
            print("Escolha inválida.")
            input("Pressione ENTER para voltar...")
            system('cls')
            return

        marca, modelo, matricula, preco_dia = lista[escolha - 1][:4]
        print(f"\nSelecionou: {marca} {modelo} ({matricula}) — {preco_dia} EUR/dia")
        
        sucesso = carros.marcar_alugado(matricula, self.user_id) 
        if sucesso:
            print("Veículo alugado com sucesso.")
        else:
            print("Não foi possível marcar o veículo como alugado.")
        input("Pressione ENTER para voltar ao menu...")
        system('cls')


    def consultar_aluguel(self):

        """Lista alugueres ativos do utilizador e permite cancelar um aluguer.

        Returns:
            list: Lista de alugueres atuais do utilizador.
        """

        system('cls')
        print("Veículos atualmente alugados:\n")
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT marca, modelo, matricula, preco_dia , data_inicio , data_fim FROM carros WHERE estado = 'Alugado' AND user_id = ?", (self.user_id,))
        alug = cursor.fetchall()

        if not alug:
            print("Não existem veículos alugados.")
            conn.close()
            input("\nPressione ENTER para voltar ao menu...")
            system('cls')
            return alug

        for idx, (marca, modelo, matricula, preco_dia , data_inicio , data_fim) in enumerate(alug, start=1):
            print(f"{idx}. {marca} {modelo} | Matrícula: {matricula} | Preço/dia: {preco_dia} EUR | Data Início: {data_inicio} | Data Fim: {data_fim}")

        print("\n0 - Voltar\n")
        escolha = input("Escolha o número do veículo para cancelar o aluguer (ou 0 para voltar): ").strip()
        if escolha == "0" or escolha == "":
            conn.close()
            system('cls')
            return alug

        try:
            escolha_i = int(escolha)
            if escolha_i < 1 or escolha_i > len(alug):
                raise ValueError
        except ValueError:
            print("Escolha inválida.")
            input("\nPressione ENTER para voltar...")
            conn.close()
            system('cls')
            return alug

       
        marca, modelo, matricula, preco_dia, data_inicio, data_fim = alug[escolha_i - 1]
        confirmar = input(f"Confirma cancelar o aluguer do {marca} {modelo} ({matricula})? (s/n): ").strip().lower()
        if confirmar != "s":
            print("Cancelamento abortado.")
            input("\nPressione ENTER para voltar...")
            conn.close()
            system('cls')
            return alug

        cursor.execute("UPDATE carros SET estado = 'Disponível', data_inicio = NULL, data_fim = NULL WHERE matricula = ?", (matricula,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Aluguel cancelado com sucesso. Veículo agora Disponível.")
        else:
            print("Falha ao cancelar o aluguel. Verifique a matrícula.")
        conn.close()
        input("\nPressione ENTER para voltar ao menu...")
        system('cls')
        return alug
    

    def voltar_ao_main(self):

        """Retorna ao menu principal."""

        print("Escolheu a opção : Voltar ao menu principal")
        input("Clique ENTER para continuar\n")
        system('cls')
        return

    def menu(self):

        """Executa o loop do menu de aluguer e aguarda a escolha do utilizador."""

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

 





