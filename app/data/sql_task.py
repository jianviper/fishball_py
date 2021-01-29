#!/usr/bin/env python
# coding:utf-8
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
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


def sql_update_task(update_data):
    try:
        data = db.query(Task).filter(and_(Task.task_id == update_data['task_id'], Task.is_delete == 0))
        r = data.first()
        if r.task_detail != update_data['task_detail']:
            print(r)
            data.update({'task_detail': update_data['task_detail']})
            db.commit()
    finally:
        db.close()


def sql_update_task1(task_data: dict):
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


def sql_complete_task(task_id, status, member_id):
    try:
        query = db.query(Task).filter(Task.task_id == task_id)
        target_num = 0
        iter_id = query.first().iter_id
        if status == 1:
            target_num = query.first().target_num
        query.update({'status': status, 'get_num': target_num})
        update_iter_num(iter_id)  #更新迭代鱼丸总数
        update_member_num(member_id)  #更新用户鱼丸总数
        db.commit()
        return sql_get_task()
    except BaseException as e:
        print(e)
    finally:
        db.close()


def update_iter_num(iter_id):
    from app.data.models import Iters
    iter_query = db.query(Iters).filter(Iters.iter_id == iter_id)
    num = db.query(func.sum(Task.get_num)).filter(Task.iter_id == iter_id).scalar()
    iter_query.update({'number': num})


def update_member_num(member_id):
    from app.data.models import Member
    query = db.query(Member).filter(Member.member_id == member_id)
    num = db.query(func.sum(Task.get_num)).filter(Task.member_id == member_id).scalar()
    query.update({'number': num})


if __name__ == '__main__':
    # sql_complete_task(8, 1)
    update_iter_num(4)
