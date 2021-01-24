#!/usr/bin/env python
# coding:utf-8
from sqlalchemy import Column, ForeignKey, Integer, Boolean, VARCHAR, DateTime
from sqlalchemy.orm import relationships
from .database import Base


class Iters(Base):
    __tablename__ = 'fish_iters'
    iter_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
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
    member_id = Column(Integer, ForeignKey('fish_member.m_id'))
    member_name = Column(VARCHAR(255))
    task_detail = Column(VARCHAR(255))
    task_date = Column(DateTime)
    target_num = Column(Integer)
    get_num = Column(Integer)
    is_delete = Column(Integer)

    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
            return dict

    def __repr__(self):
        return "<Task(id=%s,iter_id=%s,iter_name=%s,member_id=%s,member_name=%s,task=%s,task_date=%s,target_num=%s," \
               "get_num=%s,is_delete=%s)>" % (
                   self.task_id, self.iter_id, self.iter_name, self.member_id, self.member_name, self.task_detail,
                   self.task_date, self.target_num, self.get_num, self.is_delete)


class Member(Base):
    __tablename__ = 'fish_member'
    m_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    job = Column(VARCHAR(255))
    number = Column(Integer)
    is_delete = Column(Integer)

    def __repr__(self):
        return "<Member(id=%s,name=%s,job=%s,number=%s,is_delete=%s)>" % (
            self.m_id, self.name, self.job, self.number, self.is_delete)


class Ball_detial(Base):
    __tablename__ = 'fish_ball_detail'
    ball_id = Column(Integer, primary_key=True)
    iter_id = Column(Integer, ForeignKey('fish_iters.id'))
    task_id = Column(Integer, ForeignKey('fish_task.id'))
    member_id = Column(Integer, ForeignKey('fish_member.id'))
    number = Column(Integer)

    def __repr__(self):
        return "<Ball_detail(id=%s,iter_id=%s,task_id=%s,member=%s,number=%s)>" % (
            self.ball_id, self.iter_id, self.task_id, self.member_id, self.number)
