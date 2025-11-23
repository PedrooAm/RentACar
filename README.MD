# RentACar


## 📘 Descrição

O **Rent A Car** é uma aplicação de consola desenvolvida em **Python**, que simula o funcionamento de um sistema de aluguer de carros.  
O utilizador navega por um **menu interativo**, onde pode escolher opções numeradas (1 a 4) para aceder a diferentes funcionalidades, como listar carros, criar conta, iniciar sessão, alugar um veículo, entre outras.

Atualmente, a aplicação encontra-se em fase inicial de desenvolvimento e serve como **estrutura base** para o sistema completo que será criado futuramente com interface gráfica e base de dados.

---

## ⚙️ Estrutura do projeto

Organização do repositório e descrição dos ficheiros/ pastas mais importantes:

```
RentACar/
├─ Bd/
│  └─ RentACar.db          # Base de dados SQLite (dados dos carros, utilizadores, reservas)
├─ User/
│  ├─ CriarConta.py        # Lógica para criar conta de utilizador
│  └─ LogIn.py             # Lógica de autenticação / sessão
├─Services/
|  |─adicionar_carros.py   # Lógica para adicionar carros
|  |─Carros.py             # Acesso à tabela `carros`, listagem e funções de aluguer/cancelamento
|  |─GerirReserva.py       # Funções para gerir reservas (se aplicável)
|  |─ver_historico.py      # Lógica para visualizar o histórico de carros alugados
|  
├─ AlugarVeiculo.py        # Menu/submenu para alugar veículos (interface de consola)
├─ rent_a_car.py           # Programa principal (menu principal)
└─ README.MD               # Documentação (este ficheiro)
```

Breve descrição de cada item
- **Bd/RentACar.db** — Ficheiro da base de dados SQLite.
- **rent_a_car.py** — Ponto de entrada. Mostra o menu principal e chama os submenus.

- **AlugarVeiculo.py** — Interface de utilizador para funcionalidades de aluguer (listar, consultar, cancelar).
- **User/CriarConta.py** — Funções para criação de contas (validação e inserção na BD).
- **User/LogIn.py** — Validação de credenciais e gestão de sessão.
- **Services/GerirReserva.py** — Operações relacionadas com reservas (opcional/expansível).
- **Sevices/ver_historico.py**  — Mostra o carro que o cliente está a usar neste momento e os antigos.
- **Services/adicionar_carros.py** — Funções para introduzir os carros na base de dados
- **Services/Carros.py** — Conexão com a BD; funções: listar_disponiveis(), listar_alugados(), marcar_alugado(), cancelar_aluguel().







---

## 🧭 Funcionamento (fluxo principal)

1. **Arranque**
   - Executar:
     ```bash
     python "c:\Users\O_seu_User\RentACar\rent_a_car.py"
     ```
   - O menu principal é apresentado com opções numeradas.

---

2. **Autenticação**
   - O utilizador pode:
     - Criar nova conta → módulo `User/CriarConta.py`
     - Iniciar sessão → módulo `User/LogIn.py`
        - Para ter ações de admin, inicie sessão com ``(User: Admin , pass: 123456)``
   - Algumas ações exigem sessão iniciada (ex.: ver histórico, gerir reservas).

---

3. **Alugar um veículo**
   - No menu principal selecionar **"Alugar Veículo"** → submenu em `AlugarVeiculo.py`.
   - Funcionalidades:
     - **Listar carros disponíveis** → `Carros.listar_disponiveis()`
     - Escolher um carro para alugar
     - Inserir datas (formato YYYY-MM-DD)
     - Validar data de início/ fim
     - Confirmar aluguer → `Carros.marcar_alugado()`
   - O estado do carro é atualizado para **"Alugado"** e as datas são gravadas na BD.

---

4. **Consultar / Cancelar aluguer**
   - Submenu → **"Consultar Aluguel"**
   - Lista os carros com estado **"Alugado"**
   - Opcional: cancelar aluguer
     - Função: `Carros.cancelar_aluguel()`
     - Estado volta a **"Disponível"**
     - Datas são removidas da BD.

---

5. **Adicionar carros ao sistema**
   - Funcionalidade especialmente útil para administradores.
   - Localizada em `Services/adicionar_carros.py`.
   - Permite inserir novos veículos na tabela `carros`, incluindo:
     - Marca
     - Modelo
     - Matrícula
     - Preço por dia, etc.
   - O sistema verifica:
     - Se a matrícula já existe
     - Se todos os campos obrigatórios foram preenchidos

---

6. **Gerir Reservas**
   - Funções disponíveis no módulo `Services/GerirReserva.py`.
   - Requer sessão iniciada.
   - Permite:
     - Listar reservas do utilizador
     - Alterar datas (quando permitido)
     - Renovar/estender períodos de aluguer
     - Cancelar reservas futuras
   - Esta área pode ser expandida futuramente com:
     - Gestão avançada por administradores
     - Regras de overbooking

---

7. **Ver Histórico**
   - Implementado em `Services/ver_historico.py`.
   - Acesso apenas com login efetuado.
   - Mostra:
     - Veículo atual (se existir aluguer ativo)
     - Lista de todos os veículos alugados anteriormente
     - Datas de cada aluguer
   - Importante para:
     - Controlo do cliente
     - Futuras análises estatísticas

---

8. **UX / Consola**
   - Limpeza de ecrã com `os.system('cls')`
   - Pausas com pressiona ENTER antes de continuar
   - Validações:
     - Inputs numéricos
     - Datas no formato correto
     - Respostas de confirmação
   - Sistema apresenta mensagens claras e intuitivas em caso de erro ou sucesso.







## 💻 Exemplo de utilização 

```bash
===== MENU RENT A CAR =====

Utilizador: Não autenticado

1 - Criar Conta
2 - Iniciar Sessão
4 - Fechar Programa

Por favor, escolha uma opção: 2
----------------------------------------
=== Login ===
Nome ou Email: Nicol
Password (Tab para mostrar/esconder): ******
Bem-vindo(a), Nicol!
Sessão iniciada com sucesso!
Pressione ENTER...
---------------------------------------
==============================
       MENU RENT A CAR
==============================

Utilizador: Nicol | Email: nico@gmail.com

1 - Alugar Veículo
2 - Ver Histórico de Alugueres
3 - Terminar Sessão
4 - Fechar Programa

Por favor, escolha uma opção: 2

Escolheu a opção: Ver Histórico de Alugueres
Pressione ENTER para continuar...

-------------------------------------

--- HISTÓRICO DE ALUGUERES ---
1. Ver carro atual
2. Ver histórico de carros utilizados
3. Próxima reserva
4. Voltar
Escolha uma opção: 3

--- PRÓXIMA RESERVA ---
Carro: Saab tuning | Matrícula: 34JI35
De: 2025-12-02  Até: 2025-12-10
Preço total: 279€
-----------------------
Pressione ENTER para continuar...

