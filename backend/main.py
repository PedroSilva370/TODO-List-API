from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

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
def listar_tasks():
    return {"tasks": tasks}

@app.post("/tasks", response_model=TaskResposta)
def criar_tasks(task: TaskCriacao):
    nova_task = {"id": len(tasks) + 1, "title": task.title, "description": task.description, "completed": False}
    tasks.append(nova_task)
    return nova_task

@app.get("/tasks/{task_id}")
def buscar_task_id(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.put("/tasks/{task_id}", response_model=TaskResposta)
def atualizar_task(task_novo: TaskCriacao, task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = task_novo.title
            task['description'] = task_novo.description
            return task
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")

@app.delete("/tasks/{task_id}")
def remover_task(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return {'message': 'Tarefa removida com sucesso!'}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")
