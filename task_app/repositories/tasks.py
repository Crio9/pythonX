from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models.models import Task
from schemas.tasks import TaskIn


class TaskRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self) -> list[Task]:
        statement = select(Task).order_by(Task.id)

        return list(self.db.scalars(statement).all())

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id)

    def create(self, data: TaskIn) -> Task:
        task = Task(**data.model_dump())

        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)

        return task

    def update(self, task: Task, data: TaskIn) -> Task:
        task.title = data.title
        task.priority = data.priority

        self.db.commit()
        self.db.refresh(task)

        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()