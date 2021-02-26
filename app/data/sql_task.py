#!/usr/bin/env python
# coding:utf-8
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from app.data.models import Task, Member
from datetime import datetime
from app.data.database import create_db

db: Session = create_db()


def sql_get_task(iter_id=None):
    try:
        if iter_id:
            r = db.query(Task).filter(and_(Task.iter_id == iter_id, Task.is_delete == 0)).order_by(
                desc(Task.task_date)).all()
        else:
            r = db.query(Task).filter(Task.is_delete == 0).order_by(desc(Task.task_date)).all()
        return r
    finally:
        db.close()


def sql_add_task(task_data):
    try:
        for m in task_data.members:
            # num = db.query(Member).filter(Member.member_id == m['member_id']).first().number
            data = Task(iter_id=task_data.iter_id, iter_name=task_data.iter_name, member_id=m['member_id'],
                        member_name=m['name'], task_detail=m['task'], task_date=task_data.task_date,
                        target_num=m['target_num'], get_num=task_data.get_num, mark=task_data.mark,
                        status=task_data.status, is_delete=task_data.is_delete)
            db.add(data)
            db.commit()
    finally:
        db.close()


def sql_update_task(update_data):
    try:
        data = db.query(Task).filter(and_(Task.task_id == update_data['task_id'], Task.is_delete == 0))
        data.update({'task_detail': update_data['task_detail'], 'target_num': update_data['target_num']})
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
        data = db.query(Task).filter(and_(Task.task_id == task_id, Task.is_delete == 0))
        data.update({'is_delete': 1})
        db.commit()
    except BaseException as e:
        print(e)
    finally:
        db.close()


def sql_complete_task(data):
    try:
        query = db.query(Task).filter(Task.task_id == data.task_id)
        get_num = query.first().target_num
        sql_status = query.first().status
        iter_id = query.first().iter_id
        if data.status == 1 and sql_status == 0:  #完成任务
            ball_count = update_member_num(data.member_id, get_num)  #更新用户鱼丸总数
            #更新任务状态及鱼丸数
            query.update({'status': data.status, 'get_num': get_num, 'count': ball_count, 'mark': data.mark})
            update_iter_num(iter_id)  #更新当前迭代鱼丸总数
        elif data.status == 0 and sql_status == 0:  #未完成
            ball_count = db.query(Member).filter(Member.member_id == data.member_id).first().number
            #更新任务状态及鱼丸数
            query.update({'status': 2, 'get_num': 0, 'count': ball_count, 'mark': data.mark})
        db.commit()
        return sql_get_task()
    except BaseException as e:
        print(e)
    finally:
        db.close()


def update_iter_num(iter_id):
    from app.data.models import Iters
    iter_query = db.query(Iters).filter(Iters.iter_id == iter_id)
    num = db.query(func.sum(Task.get_num)).filter(and_(Task.iter_id == iter_id, Task.is_delete == 0)).scalar()
    iter_query.update({'number': num})


def update_member_num(member_id, get_num):
    query = db.query(Member).filter(Member.member_id == member_id)
    # num = db.query(func.sum(Task.get_num)).filter(Task.member_id == member_id).scalar()
    num = query.first().number
    query.update({'number': num + get_num})
    return num + get_num


if __name__ == '__main__':
    # sql_complete_task(8, 1)
    # update_iter_num(4)
    sql_delete_task(24)
