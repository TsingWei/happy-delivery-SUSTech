from sqlalchemy import Column, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://'
                       'user_cs307:!2345678@129.204.93.30:3306/cs307')
DBSession = sessionmaker(bind=engine)


class OrderToRemain(Base):
    __tablename__ = 'order_to_remain'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    order_id = Column(Integer)
    chef_to_dish_id = Column(Integer)

    # 新建关系
    @staticmethod
    def new_connect(order_id, chef_to_dish_id):
        if order_id is None or not isinstance(order_id, int):
            raise Exception('Order is Error! It should be a no none Integer! Not ', order_id)
        if chef_to_dish_id is None or not isinstance(chef_to_dish_id, int):
            raise Exception('Chef to dish id is Error! It should be a no none Integer! Not ', chef_to_dish_id)

        session = DBSession()
        session.add(OrderToRemain(order_id=order_id,
                                  chef_to_dish_id=chef_to_dish_id))
        session.commit()
        session.close()
