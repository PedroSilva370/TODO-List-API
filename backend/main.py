from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from database import get_db
from sqlalchemy import select
from models import Task
from sqlalchemy.orm import Session

app = FastAPI(title='TODO List API')

tasks = []

class TaskCriacao(BaseModel):
    title: str
    description: str

class TaskResposta(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

@app.get("/")
def home():
    return {"message": "TODO List API funcionando!"}

@app.get("/tasks")
def listar_tasks(db: Session = Depends(get_db)):
    query = select(Task)
    all_tasks = db.execute(query).scalars().all()
    return {"tasks": all_tasks}

@app.post("/tasks", response_model=TaskResposta)
def criar_tasks(task: TaskCriacao, db: Session = Depends(get_db)):
    nova_task =Task(title=task.title, description=task.description)
    db.add(nova_task)
    db.commit()
    db.refresh(nova_task)
    return nova_task

@app.get("/tasks/{task_id}")
def buscar_task_id(task_id: int, db: Session = Depends(get_db)):
    task_buscada = select(Task).where(Task.id == task_id)
    resultado = db.execute(task_buscada)
    task = resultado.scalar_one_or_none()
    if task:
        return task
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.put("/tasks/{task_id}", response_model=TaskResposta)
def atualizar_task(task_novo: TaskCriacao, task_id: int, db: Session = Depends(get_db)):
    task_buscada = select(Task).where(Task.id == task_id)
    resultado = db.execute(task_buscada)
    task = resultado.scalar_one_or_none()
    if task:
        task.title = task_novo.title
        task.description = task_novo.description
        db.commit()
        db.refresh(task)
        return task
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.delete("/tasks/{task_id}")
def remover_task(task_id: int, db: Session = Depends(get_db)):
    task_buscada = select(Task).where(Task.id == task_id)
    resultado = db.execute(task_buscada)
    task = resultado.scalar_one_or_none()
    if task:
        db.delete(task)
        db.commit()
        return {'message': "Tarefa removida com sucesso!"}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")
