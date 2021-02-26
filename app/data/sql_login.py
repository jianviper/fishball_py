#!/usr/bin/env python
#coding:utf-8
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.data.models import User

from app.data.database import create_db

db: Session = create_db()


def sql_login(username, password):
    try:
        query = db.query(User).filter(and_(User.username == username, User.password == password)).first()
        print(query)
        m_id = query.user_id
        if query:
            return m_id
        else:
            return False
    finally:
        db.close()


if __name__ == '__main__':
    print(sql_login('xugang', 123456))
