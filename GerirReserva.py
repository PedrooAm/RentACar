import sqlite3
from datetime import datetime
 

class GerirReservas:
        
    def __init__(self, db_path="Bd/RentACar.db"):
            self.db_path = db_path

    def conectar(self):
            return sqlite3.connect(self.db_path)


    def listar_reservas(self, user_id):
        conn = self.conectar()
        cursor = conn.cursor()

        if user_id:
            cursor.execute("""
                SELECT reservas.id, reservas.user_id, reservas.carro_id, carros.marca, carros.modelo, reservas.data_inicio, reservas.data_fim, reservas.preco_total, reservas.estado
                FROM reservas 
                JOIN carros ON reservas.carro_id = carros.id
                WHERE reservas.user_id = ? AND reservas.estado != 'cancelada'
            """, (user_id,))
        else:
            cursor.execute("""
                SELECT reservas.id, reservas.user_id, reservas.carro_id, carros.marca, carros.modelo, reservas.data_inicio, reservas.data_fim, reservas.preco_total, reservas.estado
                FROM reservas 
                JOIN carros ON reservas.carro_id = carros.id
                WHERE reservas.estado != 'cancelada'
            """)

        reservas = cursor.fetchall()
        conn.close()
        if not reservas:
            print(" Não existem reservas.")
            return

        if not reservas:
            print("Não existem reservas.")
            return

        print("\n--- LISTA DE RESERVAS ---")
        for r in reservas:
            print(f"""
    ID: {r[0]}
    User: {r[1]}
    Carro: {r[2]} - {r[3]} {r[4]}
    Início: {r[5]}
    Fim: {r[6]}
    Preço: {r[7]}€
    Estado: {r[8]}
            """)
        print("--------------------------\n")

    def alterar_reserva(self, user_id=None):
        self.listar_reservas(user_id)
        reserva_id = input("ID da reserva a alterar: ")

        nova_data_inicio = input("Nova data de início (YYYY-MM-DD): ")
        nova_data_fim = input("Nova data de fim (YYYY-MM-DD): ")

        # calcular número de dias
        try:
            d1 = datetime.strptime(nova_data_inicio, "%Y-%m-%d")
            d2 = datetime.strptime(nova_data_fim, "%Y-%m-%d")
            dias = (d2 - d1).days
            if dias <= 0:
                print("Datas inválidas! Fim tem de ser posterior ao início.")
                return
        except ValueError:
            print("Formato de data inválido!")
            return

        conn = self.conectar()
        cursor = conn.cursor()

        # obter carro_id e preço antigo da reserva
        cursor.execute("SELECT carro_id, preco_total FROM reservas WHERE id=?", (reserva_id,))
        resultado = cursor.fetchone()
        if not resultado:
            print("Reserva não encontrada!")
            conn.close()
            return

        carro_id, preco_antigo = resultado

        # obter preço do carro
        cursor.execute("SELECT preco_dia FROM carros WHERE id=?", (carro_id,))
        resultado_carro = cursor.fetchone()
        if not resultado_carro:
            print("Carro não encontrado!")
            conn.close()
            return

        preco_carro = resultado_carro[0]

        # calcular novo preço total
        preco_novo = preco_carro * dias

        # calcular diferença
        diferenca = preco_novo - preco_antigo

        # atualizar reserva
        cursor.execute("""
            UPDATE reservas
            SET data_inicio=?, data_fim=?, preco_total=?
            WHERE id=?
        """, (nova_data_inicio, nova_data_fim, preco_novo, reserva_id))

        conn.commit()
        conn.close()

        # informar cliente sobre diferença de pagamento
        if diferenca > 0:
            print(f"Reserva alterada com sucesso! O cliente deve pagar mais {diferenca}€")
        elif diferenca < 0:
            print(f"Reserva alterada com sucesso! Cliente tem direito a reembolso de {-diferenca}€")
        else:
            print("Reserva alterada com sucesso! Sem diferença de preço.")
        
    def cancelar_reserva(self, user_id):
        self.listar_reservas(user_id)
        reserva_id = input("ID da reserva a cancelar: ")

        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute("UPDATE reservas SET estado='cancelada' WHERE id=?", (reserva_id,))
        conn.commit()
        conn.close()

        print("Reserva cancelada!")

    def menu(self, user_id=None):
        while True:
            print("\n--- GERIR RESERVAS ---")
            print("1. Ver reservas")
            print("2. Alterar reserva")
            print("3. Cancelar reserva")
            print("4. Voltar")
            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                self.listar_reservas(user_id)
            elif escolha == "2":
                self.alterar_reserva(user_id)
            elif escolha == "3":
                self.cancelar_reserva(user_id)
            elif escolha == "4":
                    break
            else:
                print("Opção inválida!")
