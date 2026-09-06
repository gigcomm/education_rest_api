import uuid

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=['*']
)

class Task(BaseModel):
    id: str
    title: str
    completed: bool

class TaskResponse(BaseModel):
    title: str


tasks: list[Task] = []

@app.get('/tasks')
def read_tasks() -> list[Task]:
    return tasks


@app.post('/tasks')
def create_task(task: TaskResponse) -> Task:
    new_task = Task(id=str(uuid.uuid4()), title=task.title, completed=False)
    tasks.append(new_task)
    return new_task

book: str = ''

@app.get('/book')
def read_book() -> str:
    return f"Любимая книга: {book}"

class RequestBook(BaseModel):
    book: str

@app.post('/book')
def create_book(data: RequestBook) -> dict:
    global book
    book = data.book
    return {"message": "Добавлена любимая книга"}