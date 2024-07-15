from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.task as task_schema
import api.cruds.task as task_crud
from api.db import get_db

router = APIRouter()

# タスクの一覧を取得する
@router.get("/tasks", response_model=list[task_schema.Task])
# async def list_tasks(db: Session = Depends(get_db)):
    # return task_crud.get_tasks_with_done(db)
async def list_tasks(db: AsyncSession = Depends(get_db)):
    return await task_crud.get_tasks_with_done(db)

# タスクを作成する
@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
# async def create_task(task_body: task_schema.TaskCreate, db: Session = Depends(get_db)):
#     return task_crud.create_task(db, task_body)
async def create_task(task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)):
    return await task_crud.create_task(db, task_body)


# タスクを取得する
@router.put("/tasks/{task_id}", response_model=task_schema.TaskCreateResponse)
# async def update_task(task_id: int, task_body: task_schema.TaskCreate, db: Session = Depends(get_db)):
    # task = task_crud.get_task(db, task_id)
async def update_task(task_id: int, task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
                      
    # return task_crud.update_task(db, task_body, original=task)
    return await task_crud.update_task(db, task_body, original=task)

# タスクを削除する
@router.delete("/tasks/{task_id}", response_model=None)
# async def delete_task(task_id: int, db: Session = Depends(get_db)):
#     task = task_crud.get_task(db, task_id=task_id)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.delete_task(db, original=task)