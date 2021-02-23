#!/usr/bin/env python
# coding:utf-8
from sqlalchemy import Column, ForeignKey, Integer, Boolean, VARCHAR, DateTime, DATE
from sqlalchemy.orm import relationships
from .database import Base
from datetime import datetime


class Iters(Base):
    __tablename__ = 'fish_iters'
    iter_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    start_date = Column(DATE)
    end_date = Column(DATE)
    status = Column(Integer)
    number = Column(Integer)
    detail = Column(VARCHAR(255))
    is_delete = Column(Integer)

    def __repr__(self):
        return '{0}'.format(
            {'id': self.iter_id, 'name': self.name, 'start_date': self.start_date, 'end_date': self.end_date,
             'status': self.status, 'number': self.number, 'detail': self.detail, 'is_delete': self.is_delete})

    # def __repr__(self):
    #     return "<Iterations(id=%s,name=%s,start_date=%s,end_date=%s,status=%s,number=%s,detail=%s)>" % (
    #         self.id, self.name, self.start_date, self.end_date, self.status, self.number, self.detail)


class Task(Base):
    __tablename__ = 'fish_task'
    task_id = Column(Integer, primary_key=True)
    iter_id = Column(Integer, ForeignKey('fish_iters.iter_id'))
    iter_name = Column(VARCHAR(255))
    member_id = Column(Integer, ForeignKey('fish_member.member_id'))
    member_name = Column(VARCHAR(255))
    task_detail = Column(VARCHAR(255))
    task_date = Column(DATE)
    target_num = Column(Integer)
    get_num = Column(Integer)
    mark = Column(VARCHAR(255))
    status = Column(Integer)
    is_delete = Column(Integer)
    count = Column(Integer)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
            return dict

    def __repr__(self):
        return "<Task(id=%s,iter_id=%s,iter_name=%s,member_id=%s,member_name=%s,task_detail=%s,task_date=%s," \
               "target_num=%s,get_num=%s,mark=%s,status=%s,is_delete=%s,count=%s)>" % (
                   self.task_id, self.iter_id, self.iter_name, self.member_id, self.member_name, self.task_detail,
                   self.task_date, self.target_num, self.get_num, self.mark, self.status, self.is_delete, self.count)


class Member(Base):
    __tablename__ = 'fish_member'
    member_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    job = Column(VARCHAR(255))
    number = Column(Integer)
    is_delete = Column(Integer)

    def __repr__(self):
        return "<Member(id=%s,name=%s,job=%s,number=%s,is_delete=%s)>" % (
            self.member_id, self.name, self.job, self.number, self.is_delete)


class Fish_ball_record(Base):
    __tablename__ = 'fish_ball_record'
    record_id = Column(Integer, primary_key=True)
    iter_id = Column(Integer, ForeignKey('fish_iters.id'))
    iter_name = Column(VARCHAR(255))
    member_id = Column(Integer, ForeignKey('fish_member.id'))
    member_name = Column(VARCHAR(20))
    use_id = Column(Integer)
    use_detail = Column(VARCHAR(255))
    use_date = Column(DATE)
    number = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return "<fish_ball_record(record_id=%s,iter_id=%s,iter_name=%s,member_id=%s,member_name=%s,use_id=%s," \
               "use_detail=%s,use_date=%s,number=%s,status=%s)>" % (
                   self.record_id, self.iter_id, self.iter_name, self.member_id, self.member_name, self.use_id,
                   self.use_detail, self.use_date, self.number, self.status)


class User(Base):
    __tablename__ = 'fish_user'
    user_id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(255))
    password = Column(VARCHAR(255))
    status = Column(Integer)
    role = Column(Integer)

    def __repr__(self):
        return '<User(user_id=%s,username=%s,password=%s,status=%s,role=%s)>' % (
            self.user_id, self.username, self.password, self.status, self.role)


class Used(Base):
    __tablename__ = 'fish_used'
    use_id = Column(Integer, primary_key=True)
    member_id = Column(Integer)
    member_name = Column(VARCHAR(20))
    use_detail = Column(VARCHAR(255))
    use_date = Column(DATE)
    use_num = Column(Integer)
    count = Column(Integer)

    def __repr__(self):
        return '<Used(use_id=%s,member_id=%s,member_name=%s,use_detail=%s,use_date=%s,use_num=%s,count=%s)>' % (
            self.use_id, self.member_id, self.member_name, self.use_detail, self.use_date, self.use_num, self.count)
