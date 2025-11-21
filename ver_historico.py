import sqlite3
from datetime import datetime
from typing import Optional


class VerHistorico:
    """
    Classe responsável por exibir o histórico de alugueres de um cliente.
    Pode ser importada e utilizada na main com:
        from ver_historico import VerHistorico
        VerHistorico().menu(user_id=1)
    """

    def __init__(self, db_path: str = "Bd/RentACar.db") -> None:
        self.db_path = db_path

    # -------------------------
    # Infra
    # -------------------------
    def conectar(self):
        return sqlite3.connect(self.db_path)

    def _is_cliente(self, *, user_id: Optional[int] = None, username: Optional[str] = None) -> bool:
        """Verifica se o utilizador é cliente (não administrador)."""
        conn = self.conectar()
        cur = conn.cursor()
        if user_id is not None:
            cur.execute("SELECT is_admin FROM users WHERE id=?", (user_id,))
        else:
            cur.execute("SELECT is_admin FROM users WHERE nome=? COLLATE NOCASE", (username,))
        row = cur.fetchone()
        conn.close()
        return bool(row and row[0] == 0)

    def _resolve_cliente_id(self, *, user_id: Optional[int] = None, username: Optional[str] = None) -> int:
        """Confirma o ID do cliente e valida se não é admin."""
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
    # Consultas
    # -------------------------
    def carro_atual(self, cliente_id: int):
        """Obtém o carro atualmente alugado (reserva confirmada e ativa)."""
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
        """, (cliente_id, hoje, hoje))
        row = cur.fetchone()
        conn.close()
        return row

    def historico_carros(self, cliente_id: int):
        """Obtém carros já utilizados (reservas concluídas)."""
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
        """, (cliente_id, hoje))
        rows = cur.fetchall()
        conn.close()
        return rows

    # -------------------------
    # Menu interativo
    # -------------------------
    def menu(self, user_id: Optional[int] = None, username: Optional[str] = None):
        """Exibe o menu interativo para o cliente."""
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
            print("3. Voltar")
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

            elif escolha == "2":
                rows = self.historico_carros(cliente_id)
                if not rows:
                    print("\nAinda não possui histórico de alugueres concluídos.")
                else:
                    print("\n--- HISTÓRICO DE ALUGUERES ---")
                    for c in rows:
                        print(f"{c[0]} {c[1]} | Matrícula: {c[2]} | {c[3]} → {c[4]} | Total: {c[5]}€")
                    print("-------------------------------")

            elif escolha == "3":
                break
            else:
                print("Opção inválida!")
