from pydantic import BaseModel, Field

class Task(BaseModel):
    id: int
    title: str | None = Field(None, example="Githubにcommitする")
    done: bool = Field(False, description="完了フラグ")

