#!/usr/bin/env python
#coding:utf-8
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from app.data.sql_task import *
from app.data.sql_iter import sql_get_iter

router = APIRouter()


@router.get('/task')
async def get_task():
    data = sql_get_task()
    return data


class Task(BaseModel):
    task_id: int = None
    iter_id: int
    # iter_name: str
    # member_id: int
    # member_name: str
    # task_detail: str
    # task_date: datetime
    # target_num: str
    # get_num: int = 0


@router.post('/add_task')
async def add_task(task_data: Task):
    print(task_data)
    return {'code': 200}
