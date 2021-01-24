#!/usr/bin/env python
# coding:utf-8
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel
from app.data.sql_member import *

router = APIRouter()


@router.get('/member')
async def get_member():
    data = get_members()
    return data


class MemberData(BaseModel):
    m_id: int = None
    name: str
    job: str
    is_delete: int = 0


@router.post('/add_member')
async def add_member(member_data: MemberData):
    sql_add_member(member_data)


@router.post('/update_member')
async def update_member(m_data: MemberData):
    json_m_data = jsonable_encoder(m_data)
    sql_update_member(json_m_data)
    return {'code': 200}


@router.delete('/delete_member')
async def delete_member(m_id):
    sql_delete_member(m_id)
    return {'code': 200}
