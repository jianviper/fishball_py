#!/usr/bin/env python
# coding:utf-8
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette import status

from pydantic import BaseModel
from app.data.sql_member import *

router = APIRouter()


@router.get('/member')
async def get_member():
    data = jsonable_encoder(get_members())
    return JSONResponse(data, status.HTTP_200_OK)


class MemberData(BaseModel):
    member_id: int = None
    name: str
    job: str
    number: int = 0
    is_delete: int = 0


@router.post('/add_member')
async def add_member(member_data: MemberData):
    result = sql_add_member(member_data)
    if result:
        return JSONResponse({'msg': '添加成功'}, status.HTTP_201_CREATED)
    else:
        return JSONResponse({'msg': '用户已存在,请勿重复添加.'}, status.HTTP_200_OK)


@router.post('/update_member')
async def update_member(m_data: MemberData):
    json_m_data = jsonable_encoder(m_data)
    sql_update_member(json_m_data)
    return {'code': 200}


@router.delete('/delete_member')
async def delete_member(member_id):
    sql_delete_member(member_id)
    return {'code': 200}


@router.get('/member_ball_detail')
async def get_member_ball_detail(member_id: int, iter_id: int):
    data = sql_get_member_ball_detail(member_id, iter_id)
    return {'code': 200, 'data': data}
