# TODO List API

API REST para gerenciamento de tarefas, desenvolvida com Python e FastAPI.

O projeto implementa autenticação de usuários com JWT, persistência de dados em PostgreSQL e operações CRUD para gerenciamento de tarefas.

## Tecnologias

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* JWT
* Argon2
* HTML
* CSS
* JavaScript
* Git
* GitHub

## Funcionalidades

* Cadastro de usuários
* Hash seguro de senhas com Argon2
* Login com geração de JWT
* Autenticação e proteção das rotas
* Criação de tarefas
* Listagem de tarefas
* Busca de tarefa por ID
* Atualização completa de tarefas
* Atualização parcial de tarefas
* Exclusão de tarefas
* Definição de prioridade
* Definição de prazo
* Filtro por prioridade
* Filtro por status de conclusão
* Listagem de tarefas atrasadas
* Associação das tarefas ao usuário autenticado

## Estrutura

```text
TODO-List-API/
├── backend/
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## API

### Usuários

| Método | Endpoint | Descrição                |
| ------ | -------- | ------------------------ |
| POST   | `/users` | Cadastra um usuário      |
| POST   | `/login` | Realiza login e gera JWT |

### Tarefas

| Método | Endpoint           | Descrição                            |
| ------ | ------------------ | ------------------------------------ |
| GET    | `/tasks`           | Lista tarefas do usuário autenticado |
| GET    | `/tasks/{task_id}` | Busca uma tarefa                     |
| GET    | `/tasks/overdue`   | Lista tarefas atrasadas              |
| POST   | `/tasks`           | Cria uma tarefa                      |
| PUT    | `/tasks/{task_id}` | Substitui uma tarefa                 |
| PATCH  | `/tasks/{task_id}` | Atualiza parcialmente uma tarefa     |
| DELETE | `/tasks/{task_id}` | Remove uma tarefa                    |

As rotas de tarefas exigem autenticação através de um token JWT.

## Autenticação

Após realizar o login em `/login`, a API retorna um token:

```json
{
  "access_token": "seu_token",
  "token_type": "bearer"
}
```

O token deve ser enviado nas requisições protegidas através do header:

```text
Authorization: Bearer seu_token
```

As tarefas são associadas automaticamente ao usuário identificado pelo JWT.

## Banco de dados

O projeto utiliza PostgreSQL como banco de dados e SQLAlchemy como ORM.

A URL de conexão é configurada através da variável de ambiente:

```text
DATABASE_URL
```

As credenciais e informações sensíveis não devem ser armazenadas no repositório.

## Como executar

Clone o repositório:

```bash
git clone https://github.com/PedroSilva370/TODO-List-API.git
cd TODO-List-API
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure as variáveis de ambiente no arquivo `.env`.

Execute a API:

```bash
fastapi dev backend/main.py
```

A documentação interativa da API estará disponível no Swagger:

```text
/docs
```

## Status

Em desenvolvimento.

O backend possui CRUD completo, persistência em PostgreSQL e autenticação JWT.
