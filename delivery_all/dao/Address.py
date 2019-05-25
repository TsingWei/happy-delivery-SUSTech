from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://'
                       'user_cs307:!2345678@129.204.93.30:3306/cs307')
DBSession = sessionmaker(bind=engine)


class Address(Base):
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    uid = Column(Integer)
    address_name = Column(String(45))
    address_phone = Column(String(45))

    # 新建地址
    @staticmethod
    def add_address(uid=None, address_name=None, address_phone=None):
        if uid is None or not isinstance(uid, int):
            raise Exception("Uid Error! Cannot be ", uid)
        if address_name is None or not isinstance(address_name, str):
            raise Exception("Address Error! It must be a no none String!")
        if address_phone is None or not isinstance(address_phone, str):
            raise Exception("Phone Error! It must be a no none String!")
        session = DBSession()
        session.add(Address(uid=uid,
                            address_name=address_name,
                            address_phone=address_phone))
        session.commit()
        session.close()

    # 删除地址
    @staticmethod
    def del_address(uid=None, address_name=None, address_phone=None):
        if uid is not None and not isinstance(uid, int):
            raise Exception("Uid Error! Cannot be ", uid)
        if address_name is not None and not isinstance(address_name, str):
            raise Exception("Address Error! It must be a no none String!")
        if address_phone is not None and not isinstance(address_phone, str):
            raise Exception("Phone Error! It must be a no none String!")

        condition = (Address.address_id > 0)
        if uid is not None:
            condition = and_(condition, Address.uid == uid)
        if address_name is not None:
            condition = and_(condition, Address.address_name == address_name)
        if address_phone is not None:
            condition = and_(condition, Address.address_phone == address_phone)

        session = DBSession()
        session.query(Address).filter(condition).delete()
        session.commit()
        session.close()

    # 查找，返回字典的列表
    @staticmethod
    def find_address(uid=None, address_name=None, address_phone=None):
        data = []

        if not isinstance(uid, int):
            raise Exception("Uid Error! Cannot be ", uid)
        if address_name is not None and not isinstance(address_name, str):
            raise Exception("Address Name Error! It must be a no none String!")
        if address_phone is not None and not isinstance(address_phone, str):
            raise Exception("Address Phone Error! It must be a no none String!")

        condition = (Address.address_id > 0)
        if uid is not None:
            condition = and_(condition, Address.uid == uid)
        if address_name is not None:
            condition = and_(condition, Address.address_name == address_name)
        if address_phone is not None:
            condition = and_(condition, Address.address_phone == address_phone)

        session = DBSession()
        peter = session.query(Address).filter(condition).all()
        session.close()
        if peter is None:
            return data
        for i in peter:
            dic = {
                'address_id': i.address_id,
                'uid': i.uid,
                'address_name': i.address_name,
                'address_phone': i.address_phone
            }
            data.append(dic)
        return data

    # 修改地址
    # address_id 为修改查询值， 其余均为修改值
    @staticmethod
    def modify_address(address_id, uid=None, address_name=None, address_phone=None):
        if not isinstance(address_id, int):
            raise Exception("Address id Error! Cannot be ", address_id)
        if uid is not None and not isinstance(uid, int):
            raise Exception("Uid Error! Cannot be ", uid)
        if address_name is not None and not isinstance(address_name, str):
            raise Exception("Address Name Error! It must be a no none String!")
        if address_phone is not None and not isinstance(address_phone, str):
            raise Exception("Address Phone Error! It must be a no none String!")

        session = DBSession()
        address = session.query(Address).filter(Address.address_id == address_id).first()
        if uid is not None:
            address.uid = uid
        if address_name is not None:
            address.address_name = address_name
        if address_phone is not None:
            address.address_phone = address_phone
        session.commit()
        session.close()
