from fastapi import FastAPI, Depends, HTTPException
from schemas import TaskCriacao, TaskAtualizacao, TaskSubstituicao, TaskResposta, Prioridade, UserCriacao
from database import get_db
from models import Task, User
from sqlalchemy.orm import Session
from crud import criar_task as crud_criar_task
from crud import buscar_task_id as crud_buscar_task_id
from crud import substituir_task as crud_substituir_task
from crud import atualizar_parcial_task as crud_atualizar_parcial_task
from crud import remover_task as crud_remover_task
from crud import listar_tasks_por_filtros as crud_listar_tasks_por_filtros
from crud import listar_tasks_atrasadas as crud_listar_tasks_atrasadas
from crud import criar_usuario as crud_criar_usuario
from pwdlib import PasswordHash
from crud import buscar_usuario_username as crud_buscar_usuario_username
import os
import jwt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

app = FastAPI(title='TODO List API')
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:63342",
        "http://127.0.0.1:63342",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
password_hash = PasswordHash.recommended()
security = HTTPBearer()

def verificar_token(credenciais: HTTPAuthorizationCredentials = Depends(security)):
    token = credenciais.credentials
    try:
        dados= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return dados
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

@app.get("/")
def home():
    return {"message": "TODO List API funcionando!"}

@app.post("/users")
def criar_usuario(user: UserCriacao, db: Session = Depends(get_db)):
    senha_hash = password_hash.hash(user.password)
    novo_usuario = User(username=user.username, hashed_password=senha_hash)
    return crud_criar_usuario(db, novo_usuario)

@app.post("/login")
def login(user: UserCriacao, db: Session = Depends(get_db)):
    usuario = crud_buscar_usuario_username(db, user.username)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    senha_valida = password_hash.verify(user.password, usuario.hashed_password)
    if not senha_valida:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    dados_token = {"sub": str(usuario.id), "exp": datetime.now(timezone.utc) + timedelta(minutes=30)}
    token = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/tasks")
def listar_tasks(priority: Prioridade | None = None, completed: bool | None = None, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    tasks = crud_listar_tasks_por_filtros(db, int(token["sub"]), priority, completed)
    return {"tasks": tasks}

@app.get("/tasks/overdue")
def listar_tasks_atrasadas(db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    return {"tasks": crud_listar_tasks_atrasadas(db, int(token["sub"]))}

@app.post("/tasks", response_model=TaskResposta, status_code=201)
def criar_tasks(task: TaskCriacao, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    nova_task = Task(title=task.title, description=task.description, completed=task.completed, priority=task.priority, due_date=task.due_date, user_id=int(token["sub"]))
    return crud_criar_task(db, nova_task)

@app.get("/tasks/{task_id}")
def buscar_task_id(task_id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    task = crud_buscar_task_id(db, task_id, int(token["sub"]))
    if task:
        return task
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.put("/tasks/{task_id}", response_model=TaskResposta)
def atualizar_task(task_novo: TaskSubstituicao, task_id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    task = crud_buscar_task_id(db, task_id, int(token["sub"]))
    if task:
        dados_novos = Task(title=task_novo.title, description=task_novo.description, completed=task_novo.completed, priority=task_novo.priority, due_date=task_novo.due_date)
        return crud_substituir_task(db, task, dados_novos)
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.patch("/tasks/{task_id}", response_model=TaskResposta)
def atualizar_parcial_task(task_novo: TaskAtualizacao, task_id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    task = crud_buscar_task_id(db, task_id, int(token["sub"]))
    if task:
        dados = task_novo.model_dump(exclude_unset=True)
        return crud_atualizar_parcial_task(db, task, dados)
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.delete("/tasks/{task_id}", status_code=204)
def remover_task(task_id: int, db: Session = Depends(get_db), token: dict = Depends(verificar_token)):
    task = crud_buscar_task_id(db, task_id, int(token["sub"]))
    if task:
        crud_remover_task(db, task)
        return
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")