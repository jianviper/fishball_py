#!/usr/bin/env python
# coding:utf-8
import uvicorn
from app import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app='main:app', host='192.168.105.132', port=8001, reload='debug')
