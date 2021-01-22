#!/usr/bin/env python
#coding:utf-8
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.data.models import Task
from datetime import datetime
from app.data.database import create_db

db: Session = create_db()


def sql_get_task():
    try:
        r = db.query(Task).filter(Task.is_delete == 0).all()
        return r
    finally:
        db.close()