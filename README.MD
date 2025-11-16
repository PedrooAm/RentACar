# RentACar


## 📘 Descrição

O **Rent A Car** é uma aplicação de consola desenvolvida em **Python**, que simula o funcionamento de um sistema de aluguer de carros.  
O utilizador navega por um **menu interativo**, onde pode escolher opções numeradas (1 a 10) para aceder a diferentes funcionalidades, como listar carros, criar conta, iniciar sessão, alugar um veículo, entre outras.

Atualmente, a aplicação encontra-se em fase inicial de desenvolvimento e serve como **estrutura base** para o sistema completo que será criado futuramente com interface gráfica e base de dados.

---

## ⚙️ Estrutura do Projeto

rent_a_car/

- **`rent_a_car.py`** — Ficheiro principal da aplicação (menu principal). 
- **`RentACar.sqlite`** — Ficheiro de base de dados da aplicação.
- **`setup_db.py`** — Ficheiro com a configuração da base de dados.   
- **`CriarConta.py`** — Script chamado quando o utilizador escolhe criar uma conta.  
- **`Login.py`** — Script responsável pelo login do utilizador.  
- **`AlugarCarro.py`** — Script que simula o processo de aluguer de um carro.  
- **`README.md`** — Documento de explicação do projeto.  

## 🧭 Funcionamento

1. Quando o utilizador executa o programa `rent_a_car.py`, o menu principal é apresentado no ecrã.
2. O menu mostra várias opções numeradas (por exemplo, 1 a 10).
3. O utilizador digita o número correspondente à ação que deseja realizar.
4. Dependendo da escolha, o programa:
   - Executa scripts externos (como `CriarConta.py`, `Login.py`, `AlugarCarro.py`);
   - Mostra informações no ecrã;
   - Ou termina a execução (no caso da opção “Sair”).

---

## 💻 Exemplo de Utilização

```bash
===== MENU RENT A CAR =====
1 - listar_carros_disponiveis
2 - voltar_ao_main
3 - fechar

Por favor escolha uma opção: 1
Escolheu a opção 1
Clique ENTER para continuar
