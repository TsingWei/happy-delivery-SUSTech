import pymysql
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


def check():
    try:
        # 查询
        row = session.execute('select * from dish;')
        for r in row:
            print(r)
    except:
        print('查询失败')
    pass


def add():
    USER_NAME='test'
    USER_GENDER='M'
    USER_SID='11111111'
    USER_PHONE='11111111'
    USER_TYPE='STUDENT'
    sql='insert into user (USER_NAME, USER_GENDER, USER_SID, USER_PHONE, USER_TYPE)values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');'%(USER_NAME,USER_GENDER,USER_SID,USER_PHONE,USER_TYPE)
    try:
        # 执行sql语句
        session.execute(sql)
        # 提交到数据库执行
        session.commit()
    except:
        # Rollback in case there is any error
        session.rollback()
        print('插入失败')
    pass


def delete():
    TABLE = 'user'
    USER_SID='11111111'
    sql='delete from %s where USER_SID = \'%s\';'%(TABLE,USER_SID)

    try:
        # 执行sql语句
        session.execute(sql)
        # 提交到数据库执行
        session.commit()
    except:
        # Rollback in case there is any error
        session.rollback()
        print('删除失败')
    pass


def update():
    TABLE = 'user'
    USER_SID='11111111'
    MODIFY_COLUMN = 'USER_NAME'
    MODIFY_VALUE = 'haha'
    sql='update %s set %s = \'%s\' where USER_SID = \'%s\';'%(TABLE,MODIFY_COLUMN,MODIFY_VALUE,USER_SID)

    try:
        # 执行sql语句
        session.execute(sql)
        # 提交到数据库执行
        session.commit()
    except:
        # Rollback in case there is any error
        session.rollback()
        print('修改失败')
    pass


if __name__ == '__main__':
    HOST = '129.204.93.30'
    PORT = '3306'
    DATABASE = 'cs307'
    USERNAME = 'user_cs307'
    PASSWORD = '!2345678'
    DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset-utf8".format(username=USERNAME, password=PASSWORD,host=HOST,port=PORT,db=DATABASE)
    # 创建一个引擎
    engine = create_engine(DB_URI)
    Session_class = sessionmaker(bind=engine)  # 创建用于数据库session的类
    session = Session_class()
    # 增
    # add()
    # 删
    # delete()
    # 改
    # update()
    # 查
    # check()


