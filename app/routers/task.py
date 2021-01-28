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
    iter_id: int
    iter_name: str
    member_id: int
    member_name: str
    task_detail: str
    task_date: datetime
    target_num: str
    mark: str = None
    status: int = 0
    get_num: int = 0
    is_delete: int = 0


@router.post('/add_task')
async def add_task(task_data: Task):
    d_data = jsonable_encoder(task_data)
    print(d_data)
    sql_add_task(task_data)
    return {'code': 200}


@router.post('/update_task')
async def update_task(task_data: Task):
    d_data = jsonable_encoder(task_data)
    print(d_data)
    sql_update_task(d_data)
    return {'code': 200}


@router.delete('/delete_task')
async def delete_task(task_id):
    sql_delete_task(task_id)
    return {'code': 200}


@router.get('/complete_task')
async def complete_task(task_id: int, status: int, member_id: int):
    print(task_id, status, member_id)
    data = sql_complete_task(task_id, status, member_id)
    return {'code': 200, 'data': data}
