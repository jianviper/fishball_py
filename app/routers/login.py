#!/usr/bin/env python
#coding:utf-8
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from app.data.sql_login import *

router = APIRouter()


class Users(BaseModel):
    username: str
    password: str


@router.post('/login')
async def login(user_data: Users):
    data = sql_login(user_data.username, user_data.password)
    return data
