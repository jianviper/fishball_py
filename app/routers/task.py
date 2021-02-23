#!/usr/bin/env python
# coding:utf-8
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from app.data.sql_task import *

router = APIRouter()


@router.get('/task')
async def get_task():
    data = sql_get_task()
    return data


class Task(BaseModel):
    task_id: int = None
    iter_id: int = None
    iter_name: str
    member_id: int = None
    members: list
    task_detail: str = None
    task_date: str
    target_num: str = None
    mark: str = None
    status: int = 0
    get_num: int = 0
    is_delete: int = 0


@router.post('/add_task')
async def add_task(task_data: Task):
    d_data = jsonable_encoder(task_data)
    sql_add_task(task_data)
    return {'code': 200}


class TaskUpdate(BaseModel):
    task_id: int
    task_detail: str
    target_num: int


@router.patch('/update_task')
async def update_task(update_data: TaskUpdate):
    data = jsonable_encoder(update_data)
    sql_update_task(data)
    return {'code': 200}


@router.delete('/delete_task')
async def delete_task(task_id):
    print('task_id:', task_id)
    sql_delete_task(task_id)
    return {'code': 200}


class TaskComplete(BaseModel):
    member_id: int
    task_id: int
    status: int = 0
    mark: str = None


@router.patch('/complete_task')
async def complete_task(data: TaskComplete):
    print(jsonable_encoder(data))
    data = sql_complete_task(data)
    return {'code': 200, 'data': data}
