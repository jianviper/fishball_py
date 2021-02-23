#!/usr/bin/env python
#coding:utf-8
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from app.data.sql_used import *

router = APIRouter()


@router.get('/used')
async def get_used(member_id: int = None):
    data = sql_get_used(member_id)
    return data


class Used(BaseModel):
    member_id: int
    member_name: str
    use_num: int
    use_date: str
    use_detail: str


@router.post('/add_used')
async def add_used(used_data: Used):
    data = jsonable_encoder(used_data)
    print(data)
    sql_add_used(used_data)
    return {'code': 200}
