# RentACar


## 📘 Descrição

O **Rent A Car** é uma aplicação de consola desenvolvida em **Python**, que simula o funcionamento de um sistema de aluguer de carros.  
O utilizador navega por um **menu interativo**, onde pode escolher opções numeradas (1 a 10) para aceder a diferentes funcionalidades, como listar carros, criar conta, iniciar sessão, alugar um veículo, entre outras.

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
├─ Carros.py               # Acesso à tabela `carros`, listagem e funções de aluguer/cancelamento
├─ AlugarVeiculo.py        # Menu/submenu para alugar veículos (interface de consola)
├─ GerirReserva.py         # Funções para gerir reservas (se aplicável)
├─ rent_a_car.py           # Programa principal (menu principal)
└─ README.MD               # Documentação (este ficheiro)
```

Breve descrição de cada item
- **Bd/RentACar.db** — Ficheiro da base de dados SQLite.
- **rent_a_car.py** — Ponto de entrada. Mostra o menu principal e chama os submenus.
- **Carros.py** — Conexão com a BD; funções: listar_disponiveis(), listar_alugados(), marcar_alugado(), cancelar_aluguel().
- **AlugarVeiculo.py** — Interface de utilizador para funcionalidades de aluguer (listar, consultar, cancelar).
- **User/CriarConta.py** — Funções para criação de contas (validação e inserção na BD).
- **User/LogIn.py** — Validação de credenciais e gestão de sessão.
- **GerirReserva.py** — Operações relacionadas com reservas (opcional/expansível).







---

## 🧭 Funcionamento (fluxo principal)

1. **Arranque**
   - Executar: ``python`` "c:\Users\O_seu_User\RentACar\rent_a_car.py"
   - O menu principal é apresentado com opções numeradas.

2. **Autenticação**
   - O utilizador pode criar conta ``(CriarConta)`` ou iniciar sessão ``(LogIn)``.
   - Algumas ações (ex.: gerir reservas) podem exigir sessão iniciada.

3. **Alugar um veículo**
   - No menu principal escolher "Alugar Veículo" → abre o submenu em ``AlugarVeiculo.py``.
   - Selecionar "Listar carros disponíveis" — ``Carros.listar_disponiveis()`` devolve os veículos com estado "Disponível".
   - Escolher o número do veículo que deseja alugar.
   - As datas (data_inicio/data_fim) são pedidas dentro de ``Carros.marcar_alugado()`` — validação de formato YYYY-MM-DD e ordem (data_fim >= data_inicio).
   - Ao confirmar, ``Carros.marcar_alugado()`` atualiza a tabela `carros` definindo estado = 'Alugado' e gravando data_inicio/data_fim.

4. **Consultar / Cancelar aluguer**
   - No submenu "Consultar Aluguel" lista-se os carros com estado 'Alugado' (incluindo data_inicio e data_fim).
   - Escolher um aluguer para cancelar; ao confirmar, ``Carros.cancelar_aluguel()`` define o estado para = 'Disponível' e limpa as datas.

5. **Base de dados**
   - A tabela `carros` deve ter, no mínimo, colunas: marca, modelo, matricula, preco_dia, estado, data_inicio, data_fim.
   - O código contém funções que verificam/criam colunas ausentes (PRAGMA / ALTER TABLE) 

6. **UX / Consola**
   - Sempre que necessário é pedido `ENTER` para pausar a visualização antes de limpar o ecrã (``system('cls')``).
   - Validações: inputs numéricos e formato de datas; mensagens claras em caso de erro.






## 💻 Exemplo de utilização 

```bash
===== MENU RENT A CAR =====
1 - Criar Conta
2 - Iniciar Sessão
3 - Alugar Veículo
4 - Fechar Programa

Por favor, escolha uma opção: 3

===== MENU ALUGAR VEÍCULO =====
1 - Listar carros disponiveis
2 - Consultar Aluguel
3 - Voltar ao menu principal
4 - Encerrar

Por favor escolha uma opção: 1

Carros disponíveis:
1. Toyota Yaris | Matrícula: ABC-123 | Preço/dia: 25 EUR

Escolha o número do carro que deseja alugar: 1
Insira a data de início (YYYY-MM-DD): 2025-11-22
Insira a data de fim (YYYY-MM-DD): 2025-11-25
Confirma aluguer com estas datas? (s/n): s
Veículo alugado com sucesso.
```

---
