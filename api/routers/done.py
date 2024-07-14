from fastapi import APIRouter

router = APIRouter()

# タスクを完了済みにする
@router.put("/tasks/{task_id}/done", response_model=None)
async def mark_task_as_done(task_id: int):
    return

# タスクを未完了にする
@router.delete("/tasks/{task_id}/done", response_model=None)
async def unmark_task_as_done(task_id: int):
    return
