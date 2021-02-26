#!/usr/bin/env python
#coding:utf-8
from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from fastapi import Header
# 导入配置文件
from app.config import Setting


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    # 生成token
    :param subject: 保存到token的值
    :param expires_delta: 过期时间
    :return:
    """
    setting = Setting()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    print(to_encode, setting.SECRET_KEY, setting.JWT_ALGORITHM)
    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.JWT_ALGORITHM)
    return encoded_jwt


def check_jwt_token(token: Optional[str] = Header(...)) -> Union[str, Any]:
    """
    解析验证 headers中为token的值 当然也可以用 Header(..., alias="Authentication") 或者 alias="X-token"
    :param token:
    :return:
    """
    from jose.exceptions import ExpiredSignatureError, JWTError
    try:
        print('tttttt', token)
        setting = Setting()
        payload = jwt.decode(
            token,
            setting.SECRET_KEY, algorithms=[setting.JWT_ALGORITHM]
        )
        print('check', payload)
        return payload
    except ExpiredSignatureError as e:
        print("token过期", e)
    except JWTError as e:
        print("token验证失败", e)
