import sqlite3
from typing import Optional
import sys
from os import system

class AdicionarCarros:

    """Gestão de carros (apenas para administradores).

    Permite listar, adicionar e remover carros associados ao sistema.
    
    Args:
        db_path (str): Caminho para a base de dados SQLite.
    """

    def __init__(self, db_path: str = "Bd/RentACar.db") -> None:
        self.db_path = db_path

   
    def conectar(self):

        """Abre uma ligação à base de dados.

        Returns:
            sqlite3.Connection: Conexão ativa à base de dados.
        """

        return sqlite3.connect(self.db_path)

    def _is_admin(self, *, user_id: Optional[int] = None, username: Optional[str] = None) -> bool:

        """Verifica se o utilizador é administrador.

        Args:
            user_id (int, optional): ID do utilizador.
            username (str, optional): Username do utilizador.

        Returns:
            bool: True se for admin, False caso contrário.
        """

        conn = self.conectar()
        cur = conn.cursor()
        if user_id is not None:
            cur.execute("SELECT is_admin FROM users WHERE id=?", (user_id,))
        else:
            cur.execute("SELECT is_admin FROM users WHERE username=? COLLATE NOCASE", (username,))
        row = cur.fetchone()
        conn.close()
        return bool(row and row[0] == 1)

    def _resolve_admin_id(self, *, user_id: Optional[int] = None, username: Optional[str] = None) -> int:

        """Obtém o ID do admin e valida permissões.

        Args:
            user_id (int, optional): ID do utilizador.
            username (str, optional): Username do utilizador.

        Raises:
            PermissionError: Se o utilizador não existir ou não for admin.

        Returns:
            int: ID do utilizador admin.
        """

        conn = self.conectar()
        cur = conn.cursor()
        if user_id is not None:
            cur.execute("SELECT id, is_admin FROM users WHERE id=?", (user_id,))
        else:
            cur.execute("SELECT id, is_admin FROM users WHERE username=? COLLATE NOCASE", (username,))
        row = cur.fetchone()
        conn.close()
        if not row:
            raise PermissionError("Utilizador não encontrado.")
        uid, is_admin = int(row[0]), int(row[1])
        if is_admin != 1:
            raise PermissionError("Acesso negado! Apenas administradores podem adicionar ou remover carros.")
        return uid

   
    def listar_carros(self) -> list:

        """Lista todos os carros registados.

        Returns:
            list: Lista de tuplos com dados dos carros.
        """

        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, marca, modelo, matricula, user_id, preco_dia, estado FROM carros ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()
        return rows

    def add_car(
        self,
        *,
        by_user_id: Optional[int] = None,
        by_username: Optional[str] = None,
        marca: str,
        modelo: str,
        matricula: str,
        preco_dia: float,
        estado: str = "Disponível",
    ) -> int:
        
        """Adiciona um novo carro à base de dados.

        Args:
            by_user_id (int, optional): ID do utilizador que executa a ação.
            by_username (str, optional): Username do utilizador que executa a ação.
            marca (str): Marca do carro.
            modelo (str): Modelo do carro.
            matricula (str): Matrícula do carro.
            preco_dia (float): Preço por dia em euros.
            estado (str): Estado atual do carro (ex: "Disponível").

        Raises:
            PermissionError: Se o utilizador não for admin.
            sqlite3.IntegrityError: Se a matrícula for duplicada ou dados forem inválidos.

        Returns:
            int: ID do carro recém inserido.
        """

        admin_id = self._resolve_admin_id(user_id=by_user_id, username=by_username)
        conn = self.conectar()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO carros (marca, modelo, matricula, user_id, preco_dia, estado)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (marca.strip(), modelo.strip(), matricula.strip().upper(), admin_id, float(preco_dia), estado.strip()),
            )
            conn.commit()
            new_id = cur.lastrowid
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise sqlite3.IntegrityError("Não foi possível inserir o carro (matrícula duplicada ou dados inválidos).") from e
        finally:
            conn.close()
        return int(new_id)

    def delete_car(
        self,
        *,
        by_user_id: Optional[int] = None,
        by_username: Optional[str] = None,
        car_id: int,
    ) -> None:
        
        """Remove um carro da base de dados.

        Args:
            by_user_id (int, optional): ID do utilizador que executa a ação.
            by_username (str, optional): Username do utilizador que executa a ação.
            car_id (int): ID do carro a remover.

        Raises:
            PermissionError: Se o utilizador não for admin.
            ValueError: Se o carro não existir.
        """

        
        admin_id = self._resolve_admin_id(user_id=by_user_id, username=by_username)
        conn = self.conectar()
        cur = conn.cursor()
        cur.execute("SELECT id, marca, modelo, matricula FROM carros WHERE id=?", (car_id,))
        car = cur.fetchone()
        if not car:
            conn.close()
            raise ValueError("Carro não encontrado.")
        try:
            cur.execute("DELETE FROM carros WHERE id=?", (car_id,))
            conn.commit()
            print(f"Carro ID {car_id} ({car[1]} {car[2]} - {car[3]}) removido com sucesso pelo admin {admin_id}.")
        finally:
            conn.close()

  
    def menu(self, user_id: Optional[int] = None, username: Optional[str] = None) -> None:

        """Menu interativo de gestão de carros (apenas admins).

        Args:
            user_id (int, optional): ID do utilizador autenticado.
            username (str, optional): Username do utilizador autenticado.
        """

        
        if not self._is_admin(user_id=user_id, username=username):
            print("Acesso negado! Apenas administradores podem gerir carros.")
            return

        while True:
            print("--- GESTÃO DE CARROS ---")
            print("1. Listar carros")
            print("2. Adicionar carro")
            print("3. Remover carro")
            print("4. Voltar")
            escolha = input("Escolha uma opção: ").strip()
            system('cls')

            if escolha == "1":
                rows = self.listar_carros()
                if not rows:
                    print("Não existem carros registados.")
                else:
                    print("--- LISTA DE CARROS ---")
                    for c in rows:
                        print(f"ID: {c[0]} | {c[1]} {c[2]} | Mat: {c[3]} | Admin: {c[4]} | Preço/dia: {c[5]}€ | Estado: {c[6]}")
                    print("-----------------------")
                    input("Pressione ENTER para voltar ao menu...")
                    system('cls')

            elif escolha == "2":
             
                while True:
                    marca = input("Marca: ").strip()
                    modelo = input("Modelo: ").strip()
                    matricula = input("Matrícula: ").strip().upper()
                    try:
                        preco_dia = float(input("Preço por dia (€): ").strip().replace(",", "."))
                    except ValueError:
                        print("Preço inválido!")
                        input("Pressione ENTER para continuar...")
                        system('cls')
                        continue
                    estado = input("Estado [Disponível/Em manutenção/...]: ").strip() or "Disponível"
                    try:
                        new_id = self.add_car(
                            by_user_id=user_id,
                            by_username=username,
                            marca=marca,
                            modelo=modelo,
                            matricula=matricula,
                            preco_dia=preco_dia,
                            estado=estado,
                        )
                        print(f"Carro adicionado com sucesso! ID: {new_id}")
                    except PermissionError as e:
                        print(e)
                    except sqlite3.IntegrityError as e:
                        print(e)
                    except Exception as e:
                        print("Erro inesperado:", e)

                    escolha_add = input("Pressione '+' para adicionar outro carro ou ENTER para voltar ao menu: ").strip()
                    if escolha_add == "+":
                        system('cls')
                        continue
                    else:
                        system('cls')
                        break

            elif escolha == "3":
               
                entrada = input("ID do carro a remover (ou 'c' para cancelar): ").strip().lower()
                if entrada == 'c':
                    system('cls')
                    continue

                try:
                    car_id = int(entrada)
                except ValueError:
                    print("ID inválido!")
                    input("Pressione ENTER para continuar...")
                    system('cls')
                    continue

                try:
                    self.delete_car(by_user_id=user_id, by_username=username, car_id=car_id)
                except ValueError as e:
                    print(e)
                except PermissionError as e:
                    print(e)
                except Exception as e:
                    print("Erro inesperado:", e)

                input("Pressione ENTER para continuar...")
                system('cls')

            elif escolha == "4":
                break
            else:
                print("Opção inválida!")
