#!/usr/bin/env python
#coding:utf-8
import os, time
from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from app.routers.baidu import bdzs

router = APIRouter()


class ExportData(BaseModel):
    date_range: list
    keywords: list


@router.post('/baiduzhishu/download')
async def baiduzhishu(export_data: ExportData):
    # print(export_data)
    file_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    filename = '[{0}]{1}.xls'.format(export_data.keywords[0], file_time)
    path = os.path.abspath(os.path.dirname(__file__)) + '\\file\\' + filename
    bdzs.export(export_data.date_range, export_data.keywords, path)
    while not os.path.exists(path):
        print(os.path.exists(path))
        time.sleep(1)
    # header = {'content-type': 'application/octet-stream'}
    # return {'code': 200, 'data': {'filename': filename, 'file': FileResponse(path)}}
    return FileResponse(path)