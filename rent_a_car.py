"""

Sistema RENT A CAR - Programa Principal

Este módulo implementa o menu principal e o fluxo de navegação
de um sistema Rent-A-Car. Ele tem como funcionalidade
como:

- Criação de conta
- Autenticação de utilizadores
- Aluguer de veículos
- Gestão de reservas (Admin)
- Gestão de carros (Admin)
- Consulta de histórico de alugueres

Também executa o controlo da sessão do utilizador, 
mostrando opções diferentes consoante o tipo de utilizador
(normal ou administrador).

"""

import sys
from os import system
from AlugarVeiculo import Alugar
from User.CriarConta import Conta
from User.LogIn import  Login
from Services.GerirReserva import GerirReservas
from Services.adicionar_carros import AdicionarCarros
from Services.ver_historico import VerHistorico

login_system = Login()
session_user = None

def display_menu(menu):

    """
    Apresenta o cabeçalho e as opções do menu atual.

    Parâmetros
    ----------
    menu : dict[str, (str, Callable)]
        Dicionário onde a chave é o identificador da opção (ex.: "1")
        e o valor é um tuplo (descrição, função a executar).

    Efeitos colaterais
    ------------------
    - Limpa o ecrã (system('cls')).
    - Imprime no stdout o cabeçalho e a lista de opções.
    - Mostra, quando existir, o resumo do utilizador autenticado.

    Notas
    -----
    - Pressupõe que cada valor do dicionário contém exatamente
      (descrição, função). Não valida duplicados.
    """


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

    """
    Fluxo de criação de conta de utilizador.

    Pré-condições
    -------------
    - Nenhuma. Pode ser executado sem sessão.

    Efeitos colaterais
    ------------------
    - Interação via input() para avançar.
    - Limpa o ecrã antes de invocar o fluxo de criação.
    - Invoca `Conta().criar_conta()` (módulo User.CriarConta).

    Exceções
    --------
    - Propaga exceções lançadas pela camada `Conta`.
    """
    
    print("\nEscolheu a opção: Criar Conta")
    input("Pressione ENTER para continuar....")
    system('cls')
    criar = Conta()
    criar.criar_conta()

def Log_in():

    """
    Executa o processo de autenticação e atualiza o estado de sessão global.

    Efeitos colaterais
    ------------------
    - Modifica as variáveis globais `session_user` e `login_system`.
    - Interação via input() e impressão de mensagens de sucesso/erro.
    - Limpa o ecrã no início e no fim.

    Fluxo
    -----
    1) Cria uma instância de `Login`.
    2) Chama `autenticar()`; se sucesso, copia `session_user` da instância.
    3) Informa o utilizador e regressa ao menu.
    """


    global session_user, login_system
    print("\nEscolheu a opção: Iniciar Sessão")
    input("Pressione ENTER para continuar...")
    system('cls')
    log = Login()
    session = log.autenticar()
    if session:
        session_user = log.session_user
        login_system = log
        print("Sessão iniciada com sucesso!")
    else:
        print("Falha ao iniciar sessão.")
    input("Pressione ENTER...")
    system('cls')

def Log_out():

    """Termina a sessão atual."""

    global session_user
    session_user = None
    print("\nSessão terminada.")
    input("Pressione ENTER...")
    system('cls')

def Alugar_Veiculo():

    """Menu de aluguer de veículos (utilizador normal)."""

    print("\nEscolheu a opção: Alugar Veículo")
    input("Pressione ENTER para continuar...")
    system('cls')
    Alug = Alugar(session_user.get("id"))
    Alug.menu()

def Gerir_Reservas():

    """Menu de gestão de reservas (admin)."""

    print("\nEscolheu a opção: Gerir Reservas")
    input("Pressione ENTER para continuar...")
    system('cls')
    Gerir = GerirReservas()
    Gerir.menu(user_id=session_user.get("id"))

def Gerir_Carros():

    """Menu de gestão de carros (admin)."""

    print("\nEscolheu a opção: Gerir Carros (Admin)")
    input("Pressione ENTER para continuar...")
    system('cls')
    svc = AdicionarCarros("Bd/RentACar.db")
    try:
        svc.menu(user_id=session_user.get("id"))
    finally:
        try:
            svc.close()
        except Exception:
            pass

def Ver_Historico():

    """Consulta histórico de alugueres (utilizador normal)."""

    print("\nEscolheu a opção: Ver Histórico de Alugueres")
    input("Pressione ENTER para continuar...")
    system('cls')
    hist = VerHistorico("Bd/RentACar.db")
    hist.menu(user_id=session_user.get("id"))

def Fechar():

    """Encerra o programa."""

    system('cls')
    print("\nObrigado por usar o Rent A Car! Até logo ")
    sys.exit()

def main():

    """Loop principal de navegação do sistema."""

    while True:
        
        if not session_user:
            menu_items = {
                "1": ("Criar Conta", CriarConta),
                "2": ("Iniciar Sessão", Log_in),
                "3": ("Fechar Programa", Fechar),
            }
        else:
            
            is_admin = bool(session_user.get("is_admin"))
            if is_admin:
                menu_items = {
                    "1": ("Gerir Reservas (Admin)", Gerir_Reservas),
                    "2": ("Gerir Carros (Admin)", Gerir_Carros),
                    "3": ("Terminar Sessão", Log_out),
                    "4": ("Fechar Programa", Fechar),
                }
            else:
                menu_items = {
                    "1": ("Alugar Veículo", Alugar_Veiculo),
                    "2": ("Ver Histórico de Alugueres", Ver_Historico),
                    "3": ("Terminar Sessão", Log_out),
                    "4": ("Fechar Programa", Fechar),
                }

        display_menu(menu_items)
        selection = input("Por favor, escolha uma opção: ").strip()
        item = menu_items.get(selection)
        if item:
            _, func = item
            func()
        else:
            print("\nOpção inválida. Tente novamente.\n")
            input("Pressione ENTER para continuar...")
            system('cls')

if __name__ == "__main__":
    main()
