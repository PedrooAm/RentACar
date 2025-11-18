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
