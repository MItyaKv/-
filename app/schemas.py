from typing import Optional
from pydantic import BaseModel, Field, constr
from enum import Enum


class Status(str, Enum):
    created = "created"
    in_progress = "in_progress"
    done = "done"


class TaskBase(BaseModel):
    title: constr(min_length=1, max_length=200)
    description: Optional[str] = None


class TaskCreate(TaskBase):
    status: Optional[Status] = Status.created


class TaskUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=200)] = None
    description: Optional[str] = None
    status: Optional[Status] = None


class TaskOut(TaskBase):
    id: str
    status: Status

    class Config:
        orm_mode = True
