# TODO List API

API REST para gerenciamento de tarefas, desenvolvida com Python e FastAPI, com autenticação JWT, PostgreSQL e interface web em HTML, CSS e JavaScript.

**Desenvolvimento:** backend desenvolvido por mim; frontend construído com auxílio de inteligência artificial (IA).

## Demonstração

- **API:** https://todo-list-api-qbo7.onrender.com/
- **Swagger:** https://todo-list-api-qbo7.onrender.com/docs

## Funcionalidades

- Cadastro de usuários e autenticação JWT.
- Hash de senhas com Argon2.
- Criação, listagem, consulta, atualização e exclusão de tarefas.
- Atualização completa e parcial de tarefas.
- Definição de prioridade: baixa, média e alta.
- Definição de prazos.
- Marcação de tarefas como concluídas ou pendentes.
- Filtro por prioridade e status de conclusão.
- Associação de tarefas ao usuário autenticado.
- Persistência de dados em PostgreSQL.

## Tecnologias

| Tecnologia | Utilização |
|---|---|
| Python | Backend |
| FastAPI | API REST |
| PostgreSQL | Banco de dados |
| SQLAlchemy | ORM |
| Pydantic | Validação de dados |
| JWT | Autenticação |
| Argon2 | Hash de senhas |
| HTML5 | Estrutura do frontend |
| CSS3 | Estilização |
| JavaScript | Interatividade e integração com a API |
| Git e GitHub | Versionamento e hospedagem do código |
| Render | Deploy da API |

## Arquitetura

```mermaid
flowchart TD
    A[Usuário] --> B[Frontend HTML CSS JavaScript]
    B --> C[API REST FastAPI]
    C --> D[Autenticação JWT]
    C --> E[Validação Pydantic]
    D --> F[Operações da aplicação]
    E --> F
    F --> G[SQLAlchemy]
    G --> H[(PostgreSQL)]
```

## Estrutura do projeto

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
├── .gitignore
├── requirements.txt
└── README.md
```

## Endpoints

### Usuários

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/users` | Cadastro de usuário |
| POST | `/login` | Login e geração de JWT |

### Tarefas

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/tasks` | Lista tarefas |
| GET | `/tasks/{task_id}` | Consulta tarefa por ID |
| POST | `/tasks` | Cria tarefa |
| PUT | `/tasks/{task_id}` | Atualiza tarefa |
| PATCH | `/tasks/{task_id}` | Atualiza parcialmente tarefa |
| DELETE | `/tasks/{task_id}` | Exclui tarefa |

Os endpoints de tarefas exigem autenticação JWT.

### Filtros

O endpoint `GET /tasks` aceita os parâmetros `priority` e `completed`.

```text
GET /tasks?priority=alta
GET /tasks?completed=false
GET /tasks?priority=media&completed=true
```

## Autenticação

O endpoint `POST /login` retorna um token de acesso:

```json
{
  "access_token": "seu_token",
  "token_type": "bearer"
}
```

O token deve ser enviado no cabeçalho das requisições protegidas:

```text
Authorization: Bearer seu_token
```

## Banco de dados

A conexão com o PostgreSQL é configurada pela variável de ambiente `DATABASE_URL`.

Exemplo:

```text
DATABASE_URL=postgresql://usuario:senha@localhost:5432/todo_list
```

## Execução local

### 1. Clonar o repositório

```bash
git clone https://github.com/PedroSilva370/TODO-List-API.git
cd TODO-List-API
```

### 2. Criar o ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar o banco de dados

Configure a variável `DATABASE_URL` no arquivo `.env`.

### 5. Iniciar a API

```bash
fastapi dev backend/main.py
```

Documentação local: http://127.0.0.1:8000/docs

### 6. Configurar o frontend

No arquivo `frontend/script.js`, altere `API_URL` para o endereço da API local:

```javascript
const API_URL = "http://127.0.0.1:8000";
```

## Deploy

A API está hospedada no Render.

- **API:** https://todo-list-api-qbo7.onrender.com/
- **Swagger:** https://todo-list-api-qbo7.onrender.com/docs

## Autor

**Pedro Gaudencio**

- GitHub: [@PedroSilva370](https://github.com/PedroSilva370)
- Repositório: [TODO-List-API](https://github.com/PedroSilva370/TODO-List-API)

## Créditos

- **Backend:** desenvolvido por mim.
- **Frontend:** construído com auxílio de inteligência artificial (IA).