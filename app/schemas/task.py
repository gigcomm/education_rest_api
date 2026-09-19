from pydantic import BaseModel, ConfigDict


class TaskNotFound(Exception):
    pass


class TaskReadShema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    completed: bool


class TaskCreate(BaseModel):
    title: str


class TaskUpdateResponse(BaseModel):
    title: str | None = None
    completed: bool | None = None
