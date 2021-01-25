#!/usr/bin/env python
# coding:utf-8
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


def sql_add_task(task_data):
    data = Task(iter_id=task_data.iter_id, iter_name=task_data.iter_name, member_id=task_data.member_id,
                member_name=task_data.member_name, task_detail=task_data.task_detail, task_date=task_data.task_date,
                target_num=task_data.target_num, get_num=task_data.get_num, mark=task_data.mark,
                status=task_data.status, is_delete=task_data.is_delete)
    try:
        db.add(data)
        db.commit()
    finally:
        db.close()


def sql_update_task(task_data: dict):
    try:
        data = db.query(Task).filter(and_(Task.iter_id == task_data['task_id'], Task.is_delete == 0))
        r = data.first()
        json_data = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
        json_data = json_data(r)
        print(type(json_data), json_data)
        print(task_data == json_data)
        data.update(task_data)
        db.commit()
    finally:
        db.close()


def sql_delete_task(task_id):
    try:
        data = db.query(Task).filter(and_(Task.iter_id == task_id, Task.is_delete == 0)).update({'is_delete': 1})
        db.commit()
    finally:
        db.close()


def sql_complete_task(task_id, status):
    try:
        data = db.query(Task).filter(Task.task_id == task_id)
        data.update({'status': status})
        db.commit()
    except BaseException as e:
        print(e)
    finally:
        db.close()
