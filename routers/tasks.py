from fastapi import APIRouter, Depends
from starlette import status
from starlette.exceptions import HTTPException

from api.dependencies import get_task_services
from schemas.task import TaskReadShema, TaskUpdateResponse
from services.task import TaskService, TaskNotFound

task_router = APIRouter(prefix="/tasks", tags=["tasks"])


@task_router.get("")
def read_tasks(task_service: TaskService = Depends(get_task_services)) -> list[TaskReadShema]:
    return task_service.list_tasks()


@task_router.post("", status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskUpdateResponse, task_service: TaskService = Depends(get_task_services)) -> TaskReadShema:
    return task_service.create_task(payload)


@task_router.patch("/{task_id}")
def update_task(task_id: str, payload: TaskUpdateResponse, task_service: TaskService = Depends(get_task_services)) -> TaskReadShema | None:
    try:
        return task_service.update_task(task_id, payload)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )


@task_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, task_service: TaskService = Depends(get_task_services)):
    try:
        task_service.delete_task(task_id)
    except TaskNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена"
        )
