from fastapi import Depends
from sqlalchemy.orm import Session

from task_app.database import get_db
from task_app.repositories.tasks import TaskRepository
from task_app.services.tasks import TaskService


def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


def get_task_service(
    repository: TaskRepository = Depends(get_task_repository),
) -> TaskService:
    return TaskService(repository)
