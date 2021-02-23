#!/usr/bin/env python
# coding:utf-8
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.data.models import Iters, Task, Member
from datetime import datetime
from app.data.database import create_db

db: Session = create_db()


def sql_get_iter(iter_id=None):
    try:
        if iter_id:
            r = db.query(Iters).filter(and_(Iters.is_delete == 0, Iters.iter_id == iter_id)).first()
            print(r)
        else:
            r = db.query(Iters).filter(Iters.is_delete == 0).all()
            print(r)
        return r
    finally:
        db.close()


def sql_add_iter(iter_data):
    data = Iters(name=iter_data.name, start_date=iter_data.start_date, end_date=iter_data.end_date,
                 number=iter_data.number, status=iter_data.status, detail=iter_data.detail,
                 is_delete=iter_data.is_delete)
    try:
        db.add(data)
        db.commit()
    finally:
        db.close()


def sql_update_iter(iter_data: dict):
    try:
        data = db.query(Iters).filter(and_(Iters.iter_id == iter_data['iter_id'], Iters.is_delete == 0))
        r = data.first()
        json_data = lambda r: {c.name: convert(r, c.name) for c in r.__table__.columns}
        json_data = json_data(r)
        if iter_data != json_data:
            print(type(json_data), json_data)
            data.update(iter_data)
            db.commit()
    finally:
        db.close()


def convert(r, c):
    if type(getattr(r, c)) == int or type(getattr(r, c)) == str:
        return getattr(r, c)
    else:
        return str(getattr(r, c))


def sql_delete_iter(iter_id):
    try:
        data = db.query(Iters).filter(and_(Iters.iter_id == iter_id, Iters.is_delete == 0)).update({'is_delete': 1})
        db.commit()
    finally:
        db.close()


def sql_get_iter_member(iter_id: int):  #获取此迭代的成员信息
    try:
        query = db.query(Member.member_id, Member.name.label('name'), Member.job.label('job'),
                         func.sum(Task.get_num).label('ball_sum')).filter(Member.member_id == Task.member_id).filter(
            Task.iter_id == iter_id).group_by(Task.member_id)
        col_name = ['member_id', 'member_name', 'job', 'number']
        data = [dict(zip(col_name, q)) for q in query.all()]
        return data
    finally:
        db.close()


def sql_get_iter_member_detail(iter_id: int, member_id: int):
    try:
        query = db.query(Task).filter(and_(Task.iter_id == iter_id, Task.member_id == member_id)).all()
        return query
    finally:
        db.close()


if __name__ == '__main__':
    sql_get_iter_member(4)
