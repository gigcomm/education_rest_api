import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import (
    sessionmaker,
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
)
from starlette import status
from sqlalchemy import create_engine, select

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:5434/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid.uuid4()))


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_credentials=True,
)


class TaskORM(Base):
    __tablename__ = "tasks"
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


class CategoryORM(Base):
    __tablename__ = "categories"
    name: Mapped[str]


class TaskShema(BaseModel):
    id: str
    title: str
    completed: bool


class TaskCreate(BaseModel):
    title: str


class TaskUpdateResponse(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreate(BaseModel):
    name: str


categories: list[CategorySchema] = []
tasks: list[TaskShema] = []


def task_orm_model(task: TaskORM) -> TaskShema:
    return TaskShema(id=task.id, title=task.title, completed=task.completed)


def category_orm_model(category: CategoryORM) -> CategorySchema:
    return CategorySchema(id=category.id, name=category.name)


@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)) -> list[TaskShema]:
    tasks_for_db = db.scalars(select(TaskORM)).all()
    return [task_orm_model(task) for task in tasks_for_db]



@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> TaskShema:
    new_task = TaskORM(title=task.title, completed=False)
    db.add(new_task)
    db.commit()
    return task_orm_model(new_task)


@app.patch("/tasks/{task_id}")
def update_task(
    task_id: str, data: TaskUpdateResponse, db: Session = Depends(get_db)
) -> TaskShema | None:
    task_for_update = db.get(TaskORM, task_id)
    if task_for_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    if data.title is not None:
        task_for_update.title = data.title
    if data.completed is not None:
        task_for_update.completed = data.completed
    db.commit()
    return task_orm_model(task_for_update)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task_for_delete = db.get(TaskORM, task_id)
    if task_for_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    db.delete(task_for_delete)
    db.commit()


@app.get("/categories")
def get_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    categories = db.scalars(select(CategoryORM)).all()
    return [category_orm_model(category) for category in categories]


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)) -> CategorySchema:
    new_category = CategoryORM(name=data.name)
    db.add(new_category)
    db.commit()
    return category_orm_model(new_category)


@app.patch("/categories/{category_id}")
def update_category(
    category_id: str, data: CategoryCreate, db: Session = Depends(get_db)
) -> CategorySchema:
    category_for_update = db.get(CategoryORM, category_id)
    if category_for_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена",
        )
    category_for_update.name = data.name
    db.commit()
    return category_orm_model(category_for_update)


@app.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_category(category_id: str, db: Session = Depends(get_db)):
    category_for_delete = db.get(CategoryORM, category_id)
    if category_for_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена",
        )
    db.delete(category_for_delete)
    db.commit()
