from fastapi import Depends, HTTPException

from models.models import Task
from repositories.tasks import TaskRepository
from schemas.tasks import TaskIn


class TaskService:
    def __init__(
        self,
        repository: TaskRepository = Depends(),
    ):
        self.repository = repository

    def get_all(self) -> list[Task]:
        return self.repository.get_all()

    def get_by_id(self, task_id: int) -> Task:
        task = self.repository.get_by_id(task_id)

        if task is None:
            raise HTTPException(
                status_code=404,
                detail="Task not found",
            )

        return task

    def create(self, data: TaskIn) -> Task:
        return self.repository.create(data)

    def update(self, task_id: int, data: TaskIn) -> Task:
        task = self.get_by_id(task_id)

        return self.repository.update(task, data)

    def delete(self, task_id: int) -> None:
        task = self.get_by_id(task_id)

        self.repository.delete(task)