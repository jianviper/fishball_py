#!/usr/bin/env python
# coding:utf-8
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.data.models import Member, Task

from app.data.database import create_db

db: Session = create_db()


def get_members():
    try:
        r = db.query(Member).filter(Member.is_delete == 0).all()
        return r
    finally:
        db.close()


def sql_add_member(m_data):
    data = Member(name=m_data.name, job=m_data.job, number=m_data.number, is_delete=m_data.is_delete)
    try:
        db.add(data)
        db.commit()
    finally:
        db.close()


def sql_update_member(m_data: dict):
    try:
        data = db.query(Member).filter(and_(Member.member_id == m_data['member_id'], Member.is_delete == 0))
        r = data.first()
        data.update(m_data)
        db.commit()
    finally:
        db.close()


def sql_delete_member(member_id):
    try:
        data = db.query(Member).filter(and_(Member.member_id == member_id, Member.is_delete == 0)).update(
            {'is_delete': 1})
        db.commit()
    finally:
        db.close()


def sql_get_member_ball_detail(member_id, iter_id):
    try:
        query = db.query(Task).filter(and_(Task.member_id == member_id, Task.iter_id == iter_id)).all()
        return query
    finally:
        db.close()
