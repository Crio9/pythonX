from sqlalchemy import select
from sqlalchemy.orm import Session

from task_app.models.models import Task
from task_app.schemas.tasks import TaskIn


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Task]:
        return list(self.db.scalars(select(Task).order_by(Task.id)))

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
