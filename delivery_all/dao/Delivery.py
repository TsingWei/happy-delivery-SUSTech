import time

from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from user_all.dao import Order
Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://'
                       'user_cs307:!2345678@129.204.93.30:3306/cs307')
DBSession = sessionmaker(bind=engine)


class Delivery(Base):
    __tablename__ = 'delivery'

    delivery_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    delivery_name = Column(String(45))
    delivery_phone = Column(String(45))
    delivery_path = Column(String(45))
    delivery_service_year = Column(Integer)
    delivery_rank = Column(Integer)

    @staticmethod
    #通过name,phone添加新的快递员
    def register_new_delivery(name,phone):
        if isinstance(name, str) and isinstance(phone,str):
            try:
                session = DBSession()
                sql = 'insert into delivery (DELIVERY_NAME,DELIVERY_PHONE)VALUES(\'%s\' ,\'%s\' );' % (name,phone)
                session.execute(sql)
                session.commit()
                session.close()
            except:
                print('register_new_delivery fail')
            pass
        else:
            print("please input correct name,phone")

    @staticmethod
    # 通过delivery_id获得快递员评分
    def get_delivery_rank(id):
        if isinstance(id, int) :
            try:
                session = DBSession()
                sql = 'select avg(COMMENT_RANK)from delivery_comment where COMMENT_DELIVERYID=\'%s\';' % (id)
                row=session.execute(sql)
                k=[]
                for r in row:
                    a={
                        'rank':r[0]
                    }
                    k.append([a])
                session.commit()
                session.close()
                return k
            except:
                print('register_new_delivery fail')
            pass
        else:
            print("please input correct name,phone")
    @staticmethod
    # 通过delivery_id获得快递员得到的所有评论
    def get_delivery_comment(id):
        if isinstance(id, int) :
            try:
                session = DBSession()
                sql = 'select COMMENT_DETAILS,COMMENT_RANK from delivery_comment where COMMENT_DELIVERYID=\'%s\' ORDER BY COMMENT_RANK;' % (id)
                row=session.execute(sql)
                k=[]
                for r in row:
                    a={
                        'detail':r[0],
                        'rank':r[1]

                    }
                    k.append([a])
                session.commit()
                session.close()
                return k
            except:
                print('register_new_delivery fail')
            pass
        else:
            print("please input correct name,phone")

    @staticmethod
    # 通过delivery_id获得快递员做过的所有订单
    def get_delivery_all_order(id):
        if isinstance(id, int):
            try:
                session = DBSession()
                sql = 'select ORDER_ID,ADDRESS_NAME,ADDRESS_PHONE,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,ORDER_STATE from `order` ' \
                      'join address on ORDER_ADDRESS_ID= address.ADDRESS_ID where ORDER_DELIVERY_ID=\'%s\';' % ( id)
                row = session.execute(sql)
                k = []
                for r in row:
                    a = {
                        'order_id': r[0],
                        'address_name': r[1],
                        'address_phone': r[2],
                        'order_price': r[3],
                        'start_time': r[4],
                        'end_time': r[5],
                        'order_remark': r[6],
                        'order_state': r[7]

                    }
                    k.append([a])
                session.commit()
                session.close()
                return k
            except:
                print('get_delivery_all_order fail')
            pass
        else:
            print("please input correct id")

    @staticmethod
    # 通过delivery_id获得快递员正在送的所有订单
    def get_delivery_current_order(id):
        if isinstance(id, int):
            try:
                session = DBSession()
                sql = 'select ORDER_ID,ADDRESS_NAME,ADDRESS_PHONE,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,ORDER_STATE from `order` ' \
                      'join address on ORDER_ADDRESS_ID= address.ADDRESS_ID where ORDER_STATE="AC" AND ORDER_DELIVERY_ID=\'%s\';' % ( id)
                row = session.execute(sql)
                k = []
                for r in row:
                    a = {
                        'order_id': r[0],
                        'address_name': r[1],
                        'address_phone': r[2],
                        'order_price': r[3],
                        'start_time': r[4],
                        'end_time': r[5],
                        'order_remark': r[6],
                        'order_state': r[7]

                    }
                    k.append([a])
                session.commit()
                session.close()
                return k
            except:
                print('get_delivery_all_order fail')
            pass
        else:
            print("please input correct id")

    @staticmethod
    # 通过delivery_id获得快递员做过的所有订单
    def change_order_state_to_AC(deliveryid,orderid):
        if isinstance(orderid, int):
            try:

                session = DBSession()
                sql = 'select order_state from `order` where  ORDER_ID=\'%s\';' % ( orderid)
                row = session.execute(sql)
                for r in row:
                    state=r[0]
                if state=="NC":
                    Order.modify_order(orderid,delivery_id=deliveryid)
                    sql = 'update `order` set order_state="AC" where ORDER_ID = \'%s\';' % (orderid)
                    session.execute(sql)

                else:
                    print("你在想抢食？")
                session.commit()
                session.close()
                # return k
            except:
                print('change_order_state')
            pass
        else:
            print("change_order_state")

    @staticmethod
    # 通过delivery_id获得快递员做过的所有订单
    def change_order_state_to_ED(id):
        if isinstance(id, int):
            try:

                session = DBSession()
                sql = 'select order_state from `order` where  ORDER_ID=\'%s\';' % ( id)
                row = session.execute(sql)
                for r in row:
                    state=r[0]
                if state=="AC":
                    # start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    sql = 'update `order` set order_state="ED" where ORDER_ID = \'%s\';' % (id)
                    Order.modify_order(id, end_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                    session.execute(sql)

                else:
                    print("你在想抢食？")
                session.commit()
                session.close()
                # return k
            except:
                print('change_order_state')
            pass
        else:
            print("change_order_state")

    @staticmethod
    # 通过delivery_id获得快递员做过的所有订单
    def show_all_NC_order():
        try:
            session = DBSession()
            sql = 'select DISTINCT  ORDER_ID,ADDRESS_NAME,ADDRESS_PHONE,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,ORDER_STATE ' \
                  'from `order` join address on ORDER_ADDRESS_ID= address.ADDRESS_ID where ORDER_STATE="NC" AND ORDER_END_TIME IS NULL;'
            row = session.execute(sql)
            k=[]
            for r in row:
                a = {
                    'order_id': r[0],
                    'address_name': r[1],
                    'address_phone': r[2],
                    'order_price': r[3],
                    'start_time': r[4],
                    'end_time': r[5],
                    'order_remark': r[6],
                    'order_state': r[7]

                }
                k.append(a)

            session.commit()
            session.close()
            return k
        except:
            print('change_order_state')
        pass

if __name__ == '__main__':
    # result = Delivery.show_all_NC_order()
    # for  r in result:
    #     print(r)
    Delivery. change_order_state_to_ED(11998)
    []