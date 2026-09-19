from sqlalchemy.orm import Session

from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskReadShema, TaskUpdateResponse


class TaskNotFound(Exception):
    pass


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = TaskRepository(db)

    def list_tasks(self) -> list[TaskReadShema]:
        tasks = self.repository.get_all()
        return [TaskReadShema.model_validate(task) for task in tasks]

    def create_task(self, payload: TaskCreate) -> TaskReadShema:
        task = self.repository.create(title=payload.title)
        self.db.commit()
        return TaskReadShema.model_validate(task)

    def update_task(self, task_id: str, payload: TaskUpdateResponse) -> TaskReadShema:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFound("Задача не найдена")
        if payload.title is not None:
            task.title = payload.title
        if payload.completed is not None:
            task.completed = payload.completed

        self.db.commit()
        return TaskReadShema.model_validate(task)

    def delete_task(self, task_id: str) -> None:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFound("Задача не найдена")
        self.repository.delete(task)
        self.db.commit()
