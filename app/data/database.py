#!/usr/bin/env python
# coding:utf-8
# 用来初始化数据库连接
from sqlalchemy import create_engine
# 和 sqlapi 交互，执行转换后的 sql 语句，用于创建基类
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def create_db(env='test'):
    SQLALCHEMY_DATABASE_URL = ''
    # SQLALCHEMY_DATABASE_URL = 'sqlite:///../data/test.db'
    if env == 'test':
        SQLALCHEMY_DATABASE_URL = \
            'mysql+pymysql://sjy_app:sjykj201902141qaz@WSX@39.100.157.36:5506/sjy_test?charset=utf8mb4'
    elif env == 'app':
        SQLALCHEMY_DATABASE_URL = \
            'mysql+pymysql://sjy_test:sjytest1qaz@WSX@39.98.37.54:5506/hetao_note?charset=utf8mb4'
    # connect_args={"check_same_thread":False}
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    DBsession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    return DBsession()


Base = declarative_base()
