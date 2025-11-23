import sqlite3
from datetime import datetime
from typing import Optional
from os import system


class VerHistorico:

    """Consulta de histórico e estado atual de alugueres de um cliente."""


    def __init__(self, db_path: str = "Bd/RentACar.db") -> None:

        """Inicializa o gestor de histórico.

        Args:
            db_path (str): Caminho da base de dados.
        """

        self.db_path = db_path

    # -------------------------
    # Conexão com a base de dados
    # -------------------------
    def conectar(self):

        """Abre ligação com a base de dados.

        Returns:
            sqlite3.Connection: Conexão ativa.
        """

        return sqlite3.connect(self.db_path)

    # -------------------------
    # Verifica se o user é cliente
    # -------------------------
    def _is_cliente(self, *, user_id: Optional[int] = None, username: Optional[str] = None) -> bool:

        """Verifica se o utilizador é cliente (não admin).

        Args:
            user_id (int, optional): ID do utilizador.
            username (str, optional): Nome do utilizador.

        Returns:
            bool: True se for cliente, False caso contrário.
        """

        conn = self.conectar()
        cur = conn.cursor()

        if user_id is not None:
            cur.execute("SELECT is_admin FROM users WHERE id=?", (user_id,))
        else:
            cur.execute("SELECT is_admin FROM users WHERE nome=? COLLATE NOCASE", (username,))

        row = cur.fetchone()
        conn.close()
        return bool(row and row[0] == 0)  # 0 = cliente

    # -------------------------
    # Obter ID do cliente
    # -------------------------
    def _resolve_cliente_id(self, *, user_id: Optional[int] = None, username: Optional[str] = None) -> int:

        """Obtém o ID do cliente e verifica permissões.

        Args:
            user_id (int, optional): ID do utilizador.
            username (str, optional): Nome do utilizador.

        Raises:
            PermissionError: Se o utilizador não existir ou for administrador.

        Returns:
            int: ID do utilizador cliente.
        """

        conn = self.conectar()
        cur = conn.cursor()

        if user_id is not None:
            cur.execute("SELECT id, is_admin FROM users WHERE id=?", (user_id,))
        else:
            cur.execute("SELECT id, is_admin FROM users WHERE nome=? COLLATE NOCASE", (username,))

        row = cur.fetchone()
        conn.close()

        if not row:
            raise PermissionError("Utilizador não encontrado.")

        uid, is_admin = int(row[0]), int(row[1])
        if is_admin == 1:
            raise PermissionError("Acesso negado! Apenas clientes podem ver o histórico.")

        return uid

    # -------------------------
    # Carro atualmente alugado
    # -------------------------
    def carro_atual(self, user_id: int):

        """Obtém o carro que o cliente está a utilizar atualmente.

        Args:
            user_id (int): ID do cliente.

        Returns:
            tuple | None: Dados do carro atual ou None se não houver.
        """

        hoje = datetime.now().date()
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.marca, c.modelo, c.matricula, r.data_inicio, r.data_fim, r.preco_total
            FROM reservas r
            JOIN carros c ON c.id = r.carro_id
            WHERE r.user_id = ?
              AND r.estado = 'confirmada'
              AND date(r.data_inicio) <= date(?)
              AND date(r.data_fim) >= date(?)
            ORDER BY r.data_inicio DESC
            LIMIT 1
        """, (user_id, hoje, hoje))
        row = cur.fetchone()
        conn.close()
        return row

    # -------------------------
    # Histórico de carros (reservas passadas)
    # -------------------------
    def historico_carros(self, user_id: int):

        """Lista reservas concluídas no passado.

        Args:
            user_id (int): ID do cliente.

        Returns:
            list: Lista de carros utilizados anteriormente.
        """

        hoje = datetime.now().date()
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.marca, c.modelo, c.matricula, r.data_inicio, r.data_fim, r.preco_total
            FROM reservas r
            JOIN carros c ON c.id = r.carro_id
            WHERE r.user_id = ?
              AND r.estado = 'confirmada'
              AND date(r.data_fim) < date(?)
            ORDER BY r.data_fim DESC
        """, (user_id, hoje))
        rows = cur.fetchall()
        conn.close()
        return rows

    # -------------------------
    # Próxima reserva futura
    # -------------------------
    def proxima_reserva(self, user_id: int):

        """Obtém a próxima reserva futura do cliente.

        Args:
            user_id (int): ID do cliente.

        Returns:
            tuple | None: Dados da próxima reserva ou None.
        """

        hoje = datetime.now().date()
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("""
            SELECT c.marca, c.modelo, c.matricula, r.data_inicio, r.data_fim, r.preco_total
            FROM reservas r
            JOIN carros c ON c.id = r.carro_id
            WHERE r.user_id = ? 
              AND r.estado = 'confirmada'
              AND date(r.data_inicio) > date(?)
            ORDER BY r.data_inicio ASC
            LIMIT 1
        """, (user_id, hoje))
        row = cur.fetchone()
        conn.close()
        return row

    # -------------------------
    # Menu interativo completo
    # -------------------------
    def menu(self, user_id: Optional[int] = None, username: Optional[str] = None):

        """Menu interativo para clientes visualizarem histórico e reservas.

        Args:
            user_id (int, optional): ID do utilizador cliente.
            username (str, optional): Nome do utilizador cliente.
        """

        if not self._is_cliente(user_id=user_id, username=username):
            print("Acesso negado! Apenas clientes podem ver o histórico.")
            return

        try:
            cliente_id = self._resolve_cliente_id(user_id=user_id, username=username)
        except PermissionError as e:
            print(e)
            return

        while True:
            print("\n--- HISTÓRICO DE ALUGUERES ---")
            print("1. Ver carro atual")
            print("2. Ver histórico de carros utilizados")
            print("3. Próxima reserva")
            print("4. Voltar")
            escolha = input("Escolha uma opção: ").strip()

            if escolha == "1":
                carro = self.carro_atual(cliente_id)
                if not carro:
                    print("\nNão está a utilizar nenhum carro atualmente.")
                else:
                    print("\n--- CARRO ATUAL ---")
                    print(f"Marca/Modelo: {carro[0]} {carro[1]}")
                    print(f"Matrícula: {carro[2]}")
                    print(f"De: {carro[3]}  Até: {carro[4]}")
                    print(f"Preço total: {carro[5]}€")
                    print("---------------------")
                input("Pressione ENTER para continuar...")
                system('cls')

            elif escolha == "2":
                rows = self.historico_carros(cliente_id)
                if not rows:
                    print("\nAinda não possui histórico de alugueres concluídos.")
                else:
                    print("\n--- HISTÓRICO DE ALUGUERES ---")
                    for c in rows:
                        print(f"{c[0]} {c[1]} | Matrícula: {c[2]} | {c[3]} → {c[4]} | Total: {c[5]}€")
                    print("-------------------------------")
                input("Pressione ENTER para continuar...")
                system('cls')

            elif escolha == "3":
                futura = self.proxima_reserva(cliente_id)
                if not futura:
                    print("\nNão possui nenhuma reserva futura agendada.")
                else:
                    print("\n--- PRÓXIMA RESERVA ---")
                    print(f"Carro: {futura[0]} {futura[1]} | Matrícula: {futura[2]}")
                    print(f"De: {futura[3]}  Até: {futura[4]}")
                    print(f"Preço total: {futura[5]}€")
                    print("-----------------------")
                input("Pressione ENTER para continuar...")
                system('cls')

            elif escolha == "4":
                break

            else:
                print("Opção inválida!")
