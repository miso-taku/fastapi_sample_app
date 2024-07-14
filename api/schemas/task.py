from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str | None = Field(None, example="Githubにcommitする")


class TaskCreate(TaskBase):
    pass

class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True


class Task(BaseModel):
    id: int
    done: bool = Field(False, description="完了フラグ")

    class Config:
        orm_mode = True
