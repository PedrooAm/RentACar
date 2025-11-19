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
        print("⚠️  Não existem reservas.")
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
