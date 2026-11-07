from fastapi import APIRouter, Depends, Response

from schemas.tasks import TaskIn, TaskOut
from services.tasks import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post(
    "",
    status_code=201,
    response_model=TaskOut,
)
def create_task(
    data: TaskIn,
    service: TaskService = Depends(),
):
    return service.create(data)


@router.get(
    "",
    response_model=list[TaskOut],
)
def get_tasks(
    service: TaskService = Depends(),
):
    return service.get_all()


@router.get(
    "/{task_id}",
    response_model=TaskOut,
)
def get_task(
    task_id: int,
    service: TaskService = Depends(),
):
    return service.get_by_id(task_id)


@router.put(
    "/{task_id}",
    response_model=TaskOut,
)
def update_task(
    task_id: int,
    data: TaskIn,
    service: TaskService = Depends(),
):
    return service.update(task_id, data)


@router.delete(
    "/{task_id}",
    status_code=204,
    response_class=Response,
)
def delete_task(
    task_id: int,
    service: TaskService = Depends(),
):
    service.delete(task_id)

    return Response(status_code=204)