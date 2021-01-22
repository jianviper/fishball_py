#!/usr/bin/env python
#coding:utf-8
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.data.models import Iters
from datetime import datetime
from app.data.database import create_db

db: Session = create_db()


def sql_get_iter(iter_id=None):
    try:
        if iter_id:
            r = db.query(Iters).filter(and_(Iters.is_delete == 0, Iters.iter_id == iter_id)).first()
            print(type(r))
        else:
            r = db.query(Iters).filter(Iters.is_delete == 0).all()
        return r
    finally:
        db.close()


def sql_add_iter(iter_data):
    data = Iters(name=iter_data.name, start_date=iter_data.start_date, end_date=iter_data.end_date,
                 status=iter_data.status, detail=iter_data.detail, is_delete=iter_data.is_delete)
    try:
        db.add(data)
        db.commit()
    finally:
        db.close()


def sql_update_iter(iter_data: dict):
    try:
        data = db.query(Iters).filter(and_(Iters.iter_id == iter_data['iter_id'], Iters.is_delete == 0))
        r = data.first()
        json_data = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
        json_data = json_data(r)
        print(type(json_data), json_data)
        print(iter_data == json_data)
        data.update(iter_data)
        db.commit()
    finally:
        db.close()


def sql_delete_iter(iter_id):
    try:
        data = db.query(Iters).filter(and_(Iters.iter_id == iter_id, Iters.is_delete == 0)).update({'is_delete': 1})
        db.commit()
    finally:
        db.close()


if __name__ == '__main__':
    sql_get_iter()
