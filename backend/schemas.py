from pydantic import BaseModel, Field, ConfigDict
from enum import Enum
from datetime import datetime

class Prioridade(str, Enum):
    BAIXA = 'baixa'
    MEDIA = 'media'
    ALTA = 'alta'


class TaskCriacao(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    completed: bool = False
    priority: Prioridade = Prioridade.MEDIA
    due_date: datetime | None = None


class TaskAtualizacao(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=500)
    completed: bool | None = None
    priority: Prioridade | None = None
    due_date: datetime | None = None


class TaskSubstituicao(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    completed: bool = False
    priority: Prioridade = Prioridade.MEDIA
    due_date: datetime | None = None


class TaskResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    completed: bool
    priority: Prioridade
    due_date: datetime | None


class UserCriacao(BaseModel):
    username: str
    password: str
