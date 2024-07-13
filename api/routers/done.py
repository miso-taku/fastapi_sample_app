from fastapi import APIRouter

router = APIRouter()

# タスクを完了済みにする
@router.put("/tasks/{task_id}/done")
async def mark_task_as_done():
    pass

# タスクを未完了にする
@router.delete("/tasks/{task_id}/done")
async def unmark_task_as_done():
    pass
