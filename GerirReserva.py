import sqlite3
from datetime import datetime

DB = "Bd/RentACar.db"  


def conectar():
    return sqlite3.connect(DB)


def listar_reservas(user_id=None):
    conn = conectar()
    cursor = conn.cursor()

    if user_id:
        cursor.execute("SELECT * FROM reservas WHERE user_id=?", (user_id,))
    else:
        cursor.execute("SELECT * FROM reservas")

    reservas = cursor.fetchall()
    conn.close()

    if not reservas:
        print(" Não existem reservas.")
        return

    print("\n--- LISTA DE RESERVAS ---")
    for r in reservas:
        print(f"""
ID: {r[0]}
User: {r[1]}
Carro: {r[2]}
Início: {r[3]}
Fim: {r[4]}
Estado: {r[5]}
Preço: {r[6]}€
        """)
    print("--------------------------\n")

def alterar_reserva():
    listar_reservas()
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

    conn = conectar()
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
    cursor.execute("SELECT preco_por_dia FROM carros WHERE id=?", (carro_id,))
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
        

def gerir_reservas():
    while True:
        print("1. Ver reservas")
        print("2. Alterar reserva")
        print("3. Cancelar reserva")
        print("4. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            listar_reservas()
        elif escolha == "2":
            alterar_reserva()
        elif escolha == "3":
            cancelar_reserva()
        else:
            break
