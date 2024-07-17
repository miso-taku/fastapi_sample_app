import datetime
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str | None = Field(None, example="Githubにcommitする")
    due_date: datetime.date | None = Field(None, example="2023-12-31")


class TaskCreate(TaskBase):
    pass

class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True


class Task(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")

    class Config:
        orm_mode = True
