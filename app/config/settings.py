#!/usr/bin/env python
#coding:utf-8
import os
from pydantic import BaseSettings


class Setting(BaseSettings):
    #加密密钥
    str_k = 'fastapi20210225'
    SECRET_KEY: str = 'c7ee573b83d87fd7803bd240474634c7'
    # jwt加密算法
    JWT_ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # 根路径
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
