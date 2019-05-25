from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_

# 创建对象的基类:
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://'
                       'user_cs307:!2345678@129.204.93.30:3306/cs307')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


# 定义Eater对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    user_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_name = Column(String(45))
    user_gender = Column(String(45))
    user_sid = Column(String(45), unique=True)
    user_phone = Column(String(45))
    user_type = Column(String(45))

    # 新建用户
    @staticmethod
    def add_user(name=None, gender=None, sid=None, phone=None, user_type=None):
        if name is None or not isinstance(name, str):
            raise Exception("Name Error! It must be a no none String!")
        if gender != 'F' and gender != 'M':
            raise Exception("Gender Error! It must be a M or F!")
        if sid is None or not isinstance(sid, str):
            raise Exception("SID Error! It must be a no none String!")
        if user_type is None or not isinstance(user_type, str):
            raise Exception("Type Error! It must be a no none String!")
        session = DBSession()
        session.add(User(user_name=name,
                         user_gender=gender,
                         user_sid=sid,
                         user_phone=phone,
                         user_type=user_type))
        session.commit()
        session.close()

    # 查询用户
    @staticmethod
    def find_user(user_id=None, user_name=None, user_gender=None, user_sid=None, user_phone=None, user_type=None):
        data = []

        if user_id is not None and not isinstance(user_id, int):
            raise Exception("Uid Error! Cannot be ", user_id)
        if user_name is not None and not isinstance(user_name, str):
            raise Exception("User name Error! It must be a no none String!")
        if user_gender is not None and user_gender != 'M' and user_gender != 'F':
            raise Exception("Gender Error! It must be F or M!")
        if user_sid is not None and not isinstance(user_sid, str):
            raise Exception("User sid Error! It must be a no none String!")
        if user_phone is not None and not isinstance(user_phone, str):
            raise Exception("User phone Error! It must be a no none String!")
        if user_type is not None and not isinstance(user_type, str):
            raise Exception("User type Error! It must be a no none String!")

        condition = (User.user_id > 0)
        if user_id is not None:
            condition = and_(condition, User.user_id == user_id)
        if user_name is not None:
            condition = and_(condition, User.user_name == user_name)
        if user_gender is not None:
            condition = and_(condition, User.user_gender == user_gender)
        if user_sid is not None:
            condition = and_(condition, User.user_sid == user_sid)
        if user_phone is not None:
            condition = and_(condition, User.user_phone == user_phone)
        if user_type is not None:
            condition = and_(condition, User.user_type == user_type)

        session = DBSession()
        peter = session.query(User).filter(condition).all()
        session.close()
        if peter is None:
            return data
        for i in peter:
            dic = {
                'user_id': i.user_id,
                'user_name': i.user_name,
                'user_gender': i.user_gender,
                'user_sid': i.user_sid,
                'user_phone': i.user_phone,
                'user_type': i.user_type
            }
            data.append(dic)
        return data

    # 修改用户信息
    @staticmethod
    def modify_user(user_id, user_name=None, user_gender=None, user_sid=None, user_phone=None, user_type=None):
        if user_id is None or not isinstance(user_id, int):
            raise Exception("Uid Error! Cannot be ", user_id)
        if user_name is not None and not isinstance(user_name, str):
            raise Exception("User name Error! It must be a no none String!")
        if user_gender is not None and user_gender != 'M' and user_gender != 'F':
            raise Exception("Gender Error! It must be F or M!")
        if user_sid is not None and not isinstance(user_sid, str):
            raise Exception("User sid Error! It must be a no none String!")
        if user_phone is not None and not isinstance(user_phone, str):
            raise Exception("User phone Error! It must be a no none String!")
        if user_type is not None and not isinstance(user_type, str):
            raise Exception("User type Error! It must be a no none String!")

        session = DBSession()
        user = session.query(User).filter(User.user_id == user_id).first()
        if user_name is not None:
            user.user_name = user_name
        if user_gender is not None:
            user.user_gender = user_gender
        if user_sid is not None:
            user.user_sid = user_sid
        if user_phone is not None:
            user.user_phone = user_phone
        if user_type is not None:
            user.user_type = user_type
        session.commit()
        session.close()
