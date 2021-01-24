#!/usr/bin/env python
# coding:utf-8
from fastapi import APIRouter

from app.data.sql_iter import sql_get_iter

router = APIRouter()


@router.get('/iter_persons')
async def get_iter_list():
    iter_list = sql_get_iter()
    return iter_list
