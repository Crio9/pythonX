from task_app.api.v1.tasks import router as tasks_router
from task_app.api.v1.users import router as users_router

__all__ = [
    "tasks_router",
    "users_router",
]
