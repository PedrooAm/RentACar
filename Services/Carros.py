import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "Bd" / "RentACar.db"

class Carros:

    """Gestão de veículos da base de dados.

    Responsável por garantir estrutura da tabela, listar carros,
    validar datas, marcar alugueres e cancelar alugueres.
    """

    def conectar(self):

        """Garante existência da pasta da BD e liga ao ficheiro SQLite.

        Returns:
            sqlite3.Connection: Conexão ativa à base de dados.
        """

        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(str(DB_PATH))

    # =============================================
    #   GARANTE QUE AS COLUNAS EXISTEM
    # =============================================
    def _ensure_columns(self):

        """Garante que colunas novas existem na tabela `carros`."""

        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("PRAGMA table_info(carros)")
            cols = [row[1] for row in cursor.fetchall()]

            if "data_inicio" not in cols:
                cursor.execute("ALTER TABLE carros ADD COLUMN data_inicio TEXT")
            if "data_fim" not in cols:
                cursor.execute("ALTER TABLE carros ADD COLUMN data_fim TEXT")
            if "user_id" not in cols:
                cursor.execute("ALTER TABLE carros ADD COLUMN user_id INTEGER")

            conn.commit()
        finally:
            conn.close()

    # =============================================
    #   GARANTE QUE TABELA RESERVAS EXISTE
    # =============================================
    def _ensure_reservas(self):

        """Garante que a tabela `reservas` existe na BD."""

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                carro_id INTEGER,
                data_inicio TEXT,
                data_fim TEXT,
                preco_total REAL,
                estado TEXT
            )
        """)
        conn.commit()
        conn.close()

    # =============================================
    #   LISTAR CARROS
    # =============================================
    def Listar(self):

        """Mostra no terminal a lista de carros disponíveis.

        Returns:
            list: Lista de tuplos com carros disponíveis.
        """

        self._ensure_columns()
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT marca, modelo, matricula, preco_dia FROM carros WHERE estado = 'Disponível'")
        carros = cursor.fetchall()
        print("Carros Disponíveis para Aluguel:")
        for carro in carros:
            marca, modelo, matricula, preco_dia = carro
            print(f"Marca: {marca}, Modelo: {modelo}, Matricula: {matricula}, Preço ao dia: {preco_dia} EUR")
        conn.close()
        return carros

    def listar_disponiveis(self):

        """Lista carros disponíveis sem imprimir nada.

        Returns:
            list: Lista de carros disponíveis.
        """

        self._ensure_columns()
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT marca, modelo, matricula, preco_dia FROM carros WHERE estado = 'Disponível'")
        carros = cursor.fetchall()
        conn.close()
        return carros

    def listar_alugados(self, user_id):

        """Lista carros alugados por um utilizador.

        Args:
            user_id (int): ID do utilizador.

        Returns:
            list: Carros alugados pelo utilizador.
        """

        self._ensure_columns()
        if not user_id:
            return []

        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT marca, modelo, matricula, preco_dia, data_inicio, data_fim 
            FROM carros 
            WHERE estado = 'Alugado' AND user_id = ?
        """, (user_id,))
        carros = cursor.fetchall()
        conn.close()
        return carros

    # =============================================
    #   VALIDAR DATA
    # =============================================
    def _valid_date(self, date_str):

        """Valida formato de data YYYY-MM-DD.

        Args:
            date_str (str): Data a validar.

        Returns:
            bool: True se válida, caso contrário False.
        """

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except Exception:
            return False

    # =============================================
    #   MARCAR CARRO COMO ALUGADO (CORRIGIDO)
    # =============================================
    def marcar_alugado(self, matricula, user_id):

        """Marca um carro como alugado e regista uma reserva.

        Pede datas ao utilizador, valida disponibilidade e grava
        os dados na base de dados.

        Args:
            matricula (str): Matrícula do carro.
            user_id (int): ID do utilizador que vai alugar.

        Returns:
            bool: True se aluguer for registado, False caso contrário.
        """


        self._ensure_columns()
        self._ensure_reservas()

        conn = self.conectar()
        cursor = conn.cursor()

        # AGORA SELECIONA O ID TAMBÉM !!!
        cursor.execute("SELECT id, preco_dia, estado FROM carros WHERE matricula = ?", (matricula,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            print("Matrícula não encontrada.")
            return False

        carro_id, preco_dia, estado = row

        if estado != "Disponível":
            conn.close()
            print("Carro não está disponível para aluguer.")
            return False

        # PEDIR DATAS
        while True:
            data_inicio = input("Insira a data de início (YYYY-MM-DD) ou 0 para cancelar: ").strip()
            if data_inicio == "0" or data_inicio == "":
                print("Aluguer cancelado.")
                conn.close()
                return False

            data_fim = input("Insira a data de fim (YYYY-MM-DD): ").strip()

            if not (self._valid_date(data_inicio) and self._valid_date(data_fim)):
                print("Formato de data inválido. Use YYYY-MM-DD.")
                continue

            di = datetime.strptime(data_inicio, "%Y-%m-%d")
            df = datetime.strptime(data_fim, "%Y-%m-%d")

            if df < di:
                print("Data fim deve ser igual ou posterior à data início.")
                continue

            break

        dias = (df - di).days + 1
        total = float(preco_dia) * dias

        print(f"Dias: {dias} | Total: {total:.2f} EUR")

        confirmar = input("Confirma aluguer com estas datas? (s/n): ").strip().lower()
        if confirmar != "s":
            print("Aluguer cancelado.")
            conn.close()
            return False

        try:
            # MARCAR CARRO COMO ALUGADO
            cursor.execute("""
                UPDATE carros
                SET estado = 'Alugado', data_inicio = ?, data_fim = ?, user_id = ?
                WHERE matricula = ? AND estado = 'Disponível'
            """, (data_inicio, data_fim, user_id, matricula))

            # REGISTAR RESERVA
            cursor.execute("""
                INSERT INTO reservas (user_id, carro_id, data_inicio, data_fim, preco_total, estado)
                VALUES (?, ?, ?, ?, ?, 'confirmada')
            """, (user_id, carro_id, data_inicio, data_fim, total))

            conn.commit()
            print("Reserva criada com sucesso.")
            return True

        except sqlite3.OperationalError as e:
            print("Erro na BD:", e)
            conn.rollback()
            return False

        finally:
            conn.close()

    # =============================================
    #   CANCELAR ALUGUEL
    # =============================================
    def cancelar_aluguel(self, matricula):

        """Cancela o aluguer de um carro.

        Args:
            matricula (str): Matrícula do carro.

        Returns:
            bool: True se foi alterado, False caso contrário.
        """

        self._ensure_columns()
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE carros 
            SET estado = 'Disponível', data_inicio = NULL, data_fim = NULL, user_id = NULL
            WHERE matricula = ? AND estado = 'Alugado'
        """, (matricula,))

        conn.commit()
        changed = cursor.rowcount
        conn.close()
        return changed > 0
