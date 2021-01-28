#!/usr/bin/env python
# coding:utf-8
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import iteration, member, task, login
from app.routers.baidu import baiduzhishu


def create_app():
    app = FastAPI()

    # 导入路由
    app.include_router(member.router, prefix='/api')
    app.include_router(iteration.router, prefix='/api')
    app.include_router(task.router, prefix='/api')
    app.include_router(login.router, prefix='/api')
    app.include_router(baiduzhishu.router)

    origins = ["http://localhost",
               "http://localhost:8080",
               "http://localhost:8001",
               "http://192.168.105.132",
               "http://192.168.105.132:8080",
               "http://0.0.0.0",
               "http://0.0.0.0:8080",
               ]

    # 允许跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
