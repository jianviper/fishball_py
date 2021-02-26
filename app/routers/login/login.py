#!/usr/bin/env python
#coding:utf-8
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette import status
from pydantic import BaseModel
from app.data.sql_login import *
from .security import *
from app.config import Setting

router = APIRouter()


class Users(BaseModel):
    username: str
    password: str


@router.post('/login')
async def login(user_data: Users):
    result = sql_login(user_data.username, user_data.password)
    if result:
        setting = Setting()
        token = create_access_token(result, timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES))
        return {'code': 200, 'data': {'token': token}}


@router.get("/user/info", summary="获取用户信息")
async def get_user_info(token_data: Union[str, Any] = Depends(check_jwt_token)) -> Any:
    """
    获取用户信息
    :param token_data:
    :return:
    """
    print(token_data)
    if token_data:
        # 这个状态能响应说明token验证通过
        return JSONResponse({'msg': '验证通过'}, status.HTTP_200_OK)
    else:
        return JSONResponse({'msg': '验证不通过'}, status.HTTP_401_UNAUTHORIZED)
