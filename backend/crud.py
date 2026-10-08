from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Task, User
from schemas import Prioridade

def listar_tasks(db: Session):
    query = select(Task)
    resultado = db.execute(query)
    return resultado.scalars().all()

def criar_task(db: Session, task: Task):
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def buscar_task_id(db: Session, task_id: int, user_id: int):
    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    resultado = db.execute(query)
    return resultado.scalar_one_or_none()

def substituir_task(db: Session, task: Task, task_novo: Task):
    task.title = task_novo.title
    task.description = task_novo.description
    task.completed = task_novo.completed
    task.priority = task_novo.priority
    task.due_date = task_novo.due_date
    db.commit()
    db.refresh(task)
    return task

def atualizar_parcial_task(db: Session, task: Task, dados: dict):
    for campo, valor in dados.items():
        setattr(task, campo, valor)
    db.commit()
    db.refresh(task)
    return task

def remover_task(db: Session, task: Task):
    db.delete(task)
    db.commit()

def listar_tasks_por_prioridade(db: Session, priority: Prioridade):
    query = select(Task).where(Task.priority == priority.value)
    resultado = db.execute(query)
    return resultado.scalars().all()

def listar_tasks_por_filtros(db: Session, user_id: int, priority: Prioridade | None = None, completed: bool | None = None):
    query = select(Task).where(Task.user_id == user_id)
    if priority is not None:
        query = query.where(Task.priority == priority.value)
    if completed is not None:
        query = query.where(Task.completed == completed)
    resultado = db.execute(query)
    return resultado.scalars().all()

def listar_tasks_atrasadas(db: Session, user_id: int):
    from datetime import datetime

    query = select(Task).where(Task.due_date < datetime.now(), Task.completed == False, Task.user_id == user_id)
    resultado = db.execute(query)
    return resultado.scalars().all()

def criar_usuario(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def buscar_usuario_username(db: Session, username: str):
    query = select(User).where(User.username == username)
    resultado = db.execute(query)
    return resultado.scalar_one_or_none()
