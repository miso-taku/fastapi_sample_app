from fastapi import APIRouter

import api.schemas.task as task_schema

router = APIRouter()

# タスクの一覧を取得する
@router.get("/tasks", response_model=list[task_schema.Task])
async def list_tasks():
    return [task_schema.Task(id=1, title="1つ目のタスク")]

# タスクを作成する
@router.post("/tasks")
async def create_task():
    pass

# タスクを取得する
@router.put("/tasks/{task_id}")
async def update_task():
    pass

# タスクを削除する
@router.delete("tasks/{task_id}")
async def delete_task():
    pass