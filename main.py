import uuid
from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette import status

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=['*'],
    allow_credentials=True,
)

class Task(BaseModel):
    id: str
    title: str
    completed: bool

class TaskCreate(BaseModel):
    title: str

class TaskUpdateResponse(BaseModel):
    title: str | None = None
    completed: bool | None = None


tasks: list[Task] = []

@app.get('/tasks')
def read_tasks() -> list[Task]:
    return tasks


@app.post('/tasks', status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> Task:
    new_task = Task(id=str(uuid.uuid4()), title=task.title, completed=False)
    tasks.append(new_task)
    return new_task

@app.patch('/tasks/{task_id}')
def update_task(task_id: str, data: TaskUpdateResponse) -> Task | None:
    for task in tasks:
        if task.id == task_id:
            if data.title:
                task.title = data.title
            if data.completed is not None:
                task.completed = data.completed
            return task

@app.delete('/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
