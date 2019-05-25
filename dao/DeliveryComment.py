import time

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_
from dao.Order import Order
Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://'
                       'user_cs307:!2345678@129.204.93.30:3306/cs307')
DBSession = sessionmaker(bind=engine)


class DeliveryComment(Base):
    __tablename__ = 'delivery'

    comment_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    comment_user_id = Column(Integer)
    comment_delivery_id = Column(Integer)
    comment_details =  Column(String(45))
    comment_rank = Column(Integer)

    @staticmethod
    #通过userid,deliveryid,comment,rank添加新的快递员评价
    def register_new_delivery_comment(userid,deliveryid,comment,rank):
        if isinstance(userid, int ) and isinstance(deliveryid,int )and isinstance(comment, str ) and isinstance(rank,int ) :
            try:
                session = DBSession()
                sql = 'insert into delivery_comment  (COMMENT_USERID,COMMENT_DELIVERYID,COMMENT_DETAILS,COMMENT_RANK)VALUES(\'%s\', \'%s\' ,\'%s\' ,\'%s\' );' % (userid,deliveryid,comment,rank)
                session.execute(sql)
                session.commit()
                session.close()
            except:
                print('register_new_delivery_comment fail')
            pass
        else:
            print("please input correct userid,deliveryid,comment,rank")


if __name__ == '__main__':
    # result = Delivery.show_all_NC_order()
    # for  r in result:
    #     print(r)
    DeliveryComment. register_new_delivery_comment(10,10,"1234567",4)