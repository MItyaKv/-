from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager", version="1.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = crud.create_task(db, task_in)
    return task


@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def read_task(task_id: str, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/tasks", response_model=List[schemas.TaskOut])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: str, task_in: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.update_task(db, task_id, task_in)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    ok = crud.delete_task(db, task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
