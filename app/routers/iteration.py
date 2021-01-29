#!/usr/bin/env python
# coding:utf-8
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from app.data.sql_iter import *

router = APIRouter()


@router.get('/iters')
async def get_iter_list():
    iter_list = sql_get_iter()
    return iter_list


class IterData(BaseModel):
    iter_id: int = None
    name: str
    start_date: str
    end_date: str
    status: int = 0
    detail: str
    number: int = 0
    is_delete: int = 0


@router.post('/add_iter')
async def add_iter(iter_data: IterData):
    print(iter_data)
    sql_add_iter(iter_data)
    iter_list = sql_get_iter()
    return {'code': 200, 'data': iter_list}


@router.put('/update_iter')
async def update_iter(iter_data: IterData):
    json_data = jsonable_encoder(iter_data)
    json_data['start_date'] = str(json_data['start_date']).replace('T', ' ')
    json_data['end_date'] = str(json_data['end_date']).replace('T', ' ')
    print(type(json_data), json_data)
    sql_update_iter(json_data)
    return {'code': 200}


@router.delete('/delete_iter')
async def delete_iter(iter_id):
    sql_delete_iter(iter_id)
    return {'code': 200}


@router.get('/iter_member')
async def get_iter_member(iter_id: int):
    data = sql_get_iter_member(iter_id)
    return data


@router.get('/iter_member_detail')
async def get_iter_member_detail(iter_id: int, member_id: int):
    data = sql_get_iter_member_detail(iter_id, member_id)
    return {'code': 200, 'data': data}
