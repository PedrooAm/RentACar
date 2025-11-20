import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "Bd" / "RentACar.db"

class Carros:
    def conectar(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(str(DB_PATH))

    def _ensure_columns(self):
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("PRAGMA table_info(carros)")
            cols = [row[1] for row in cursor.fetchall()]
            if "data_inicio" not in cols:
                cursor.execute("ALTER TABLE carros ADD COLUMN data_inicio TEXT")
            if "data_fim" not in cols:
                cursor.execute("ALTER TABLE carros ADD COLUMN data_fim TEXT")
            conn.commit()
        finally:
            conn.close()

    def Listar(self):
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
        self._ensure_columns()
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT marca, modelo, matricula, preco_dia FROM carros WHERE estado = 'Disponível'")
        carros = cursor.fetchall()
        conn.close()
        return carros

    def listar_alugados(self):
        self._ensure_columns()
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT marca, modelo, matricula, preco_dia, data_inicio, data_fim FROM carros WHERE estado = 'Alugado'")
        carros = cursor.fetchall()
        conn.close()
        return carros

    def _valid_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except Exception:
            return False

    def marcar_alugado(self, matricula):
     
        self._ensure_columns()
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT preco_dia, estado FROM carros WHERE matricula = ?", (matricula,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            print("Matrícula não encontrada.")
            return False
        preco_dia, estado = row
        if estado != "Disponível":
            conn.close()
            print("Carro não está disponível para aluguer.")
            return False

       
        while True:
            data_inicio = input("Insira a data de início (YYYY-MM-DD) ou 0 para cancelar: ").strip()
            if data_inicio == "0" or data_inicio == "":
                print("Aluguer cancelado.")
                conn.close()
                return False
            data_fim = input("Insira a data de fim (YYYY-MM-DD): ").strip()
            if not (self._valid_date(data_inicio) and self._valid_date(data_fim)):
                print("Formato de data inválido. Use YYYY-MM-DD. Tente novamente.")
                continue
            di = datetime.strptime(data_inicio, "%Y-%m-%d")
            df = datetime.strptime(data_fim, "%Y-%m-%d")
            if df < di:
                print("Data fim deve ser igual ou posterior à data início. Tente novamente.")
                continue
            break

        dias = (df - di).days + 1
        total = preco_dia * dias
        print(f"Dias: {dias} | Total: {total:.2f} EUR")
        confirmar = input("Confirma aluguer com estas datas? (s/n): ").strip().lower()
        if confirmar != "s":
            print("Aluguer cancelado.")
            conn.close()
            return False

        try:
            cursor.execute(
                "UPDATE carros SET estado = 'Alugado', data_inicio = ?, data_fim = ? WHERE matricula = ? AND estado = 'Disponível'",
                (data_inicio, data_fim, matricula)
            )
            conn.commit()
            changed = cursor.rowcount
            return changed > 0
        except sqlite3.OperationalError as e:
            print("Erro na BD:", e)
            return False
        finally:
            conn.close()

    def cancelar_aluguel(self, matricula):
        self._ensure_columns()
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE carros SET estado = 'Disponível', data_inicio = NULL, data_fim = NULL WHERE matricula = ? AND estado = 'Alugado'",
            (matricula,)
        )
        conn.commit()
        changed = cursor.rowcount
        conn.close()
        return changed > 0



