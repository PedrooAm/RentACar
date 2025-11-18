import sqlite3


class Carros:

    
    def conectar(self):
        return sqlite3.connect("Bd/RentACar.db")



    def Listar(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT  modelo, marca,matricula FROM carros ")
    
        carros = cursor.fetchall()        
        print("Carros Disponíveis para Aluguel:")
        for carro in carros:
            id, modelo, marca, ano, disponivel = carro
            print(f"ID: {id}, Modelo: {modelo}, Marca: {marca}, Ano: {ano}")

        
        
    