#!/usr/bin/env python
#coding:utf-8
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.data.models import Used, Member
from app.data.database import create_db

db: Session = create_db()


def sql_get_used(member_id=None):
    try:
        if member_id:
            r = db.query(Used).filter(Used.member_id == member_id).all()
        else:
            r = db.query(Used).all()
        return r
    finally:
        db.close()


if __name__ == '__main__':
    print(sql_get_used())


def sql_add_used(used_data):
    try:
        update_member = db.query(Member).filter(Member.member_id == used_data.member_id)
        ball_count = update_member.first().number
        update_member.update({'number': ball_count - used_data.use_num})
        data = Used(member_id=used_data.member_id, member_name=used_data.member_name, use_date=used_data.use_date,
                    use_detail=used_data.use_detail, use_num=used_data.use_num, count=ball_count - used_data.use_num)
        db.add(data)
        db.commit()
    finally:
        db.close()
