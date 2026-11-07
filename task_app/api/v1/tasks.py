from fastapi import APIRouter
from schemas import TaskIn

router = APIRouter(tags=["tasks"])
tasks = []


@router.get("/tasks", status_code=200)
def get_tasks():
    return tasks


@router.post("/tasks", status_code=201)
def post_tasks(task: TaskIn) -> dict:
    task = {
        "id": len(tasks) + 1,
        "title": task.title,
        "priority": task.priority,
    }
    tasks.append(task)

    return task

