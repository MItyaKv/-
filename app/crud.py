from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from . import models, schemas


def create_task(db: Session, task_in: schemas.TaskCreate) -> models.Task:
    task_id = str(uuid.uuid4())
    db_task = models.Task(
        id=task_id,
        title=task_in.title,
        description=task_in.description,
        status=models.StatusEnum(task_in.status.value),
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: str) -> Optional[models.Task]:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[models.Task]:
    return db.query(models.Task).offset(skip).limit(limit).all()


def update_task(db: Session, task_id: str, task_in: schemas.TaskUpdate) -> Optional[models.Task]:
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    if task_in.title is not None:
        db_task.title = task_in.title
    if task_in.description is not None:
        db_task.description = task_in.description
    if task_in.status is not None:
        db_task.status = models.StatusEnum(task_in.status.value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: str) -> bool:
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True
