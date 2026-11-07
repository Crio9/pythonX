from fastapi import APIRouter, Depends, Response

from task_app.dependencies import get_task_service
from task_app.schemas.tasks import TaskIn, TaskOut
from task_app.services.tasks import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskOut])
def get_tasks(service: TaskService = Depends(get_task_service)):
    return service.get_all()


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    return service.get_by_id(task_id)


@router.post("", status_code=201, response_model=TaskOut)
def create_task(data: TaskIn, service: TaskService = Depends(get_task_service)):
    return service.create(data)


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int, data: TaskIn, service: TaskService = Depends(get_task_service)
):
    return service.update(task_id, data)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    service.delete(task_id)
    return Response(status_code=204)

