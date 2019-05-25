from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time
from sqlalchemy.sql import and_
from dao.Dish import Dish
from dao.Hall import Hall
from dao.ChefToDish import ChefToDish
from dao.OrderToRemain import OrderToRemain

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://'
                       'user_cs307:!2345678@129.204.93.30:3306/cs307')
DBSession = sessionmaker(bind=engine)


class Order(Base):
    __tablename__ = 'order'

    order_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    order_address_id = Column(Integer)
    order_delivery_id = Column(Integer)
    order_price = Column(Integer)
    order_start_time = Column(String(45))
    order_end_time = Column(String(45))
    order_remark = Column(String(45))
    order_state = Column(String(45))

    # 新建订单
    @staticmethod
    def new_order(address_id, state, orders, hall_id, start_time=None,
                  delivery_id=None, price=None, end_time=None, remark=None):
        if address_id is None or not isinstance(address_id, int):
            raise Exception("Address id Error! It should be a no none Integer! Not ", address_id)
        if state != 'AC' and state != 'ED' and state != 'NC':
            raise Exception("State Error! It should be AC, ED or NC! Not ", state)
        if start_time is not None and not isinstance(start_time, str):
            raise Exception("Start time Error! It should be a no none String! Not ", address_id)
        if delivery_id is not None and not isinstance(delivery_id, int):
            raise Exception("Delivery id Error! It should be an Integer! Not ", delivery_id)
        if price is not None and not isinstance(price, float):
            raise Exception("Price Error! It should be an Integer! Not ", price)
        if end_time is not None and not isinstance(end_time, str):
            raise Exception("End time Error! It should be a String! Not ", end_time)
        if remark is not None and not isinstance(remark, str):
            raise Exception("Remark Error! It should be a String! Not ", remark)
        if orders is None or not isinstance(orders, dict):
            raise Exception("Error! Orders should be a dictionary")
        if hall_id is None or not isinstance(hall_id, int):
            raise Exception("Hall id Error! It should be a no none Integer! Not ", hall_id)
        if start_time is None:
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        if price is None:
            price = 0
            for key in orders:
                dish = Dish.find_dish(dish_id=key)
                if len(dish) > 1:
                    raise Exception('Error! Two dish with a same name: ', dish[0]["dish_name"])
                res = Hall.get_chef_id(dish[0]['dish_id'], hall_id)
                if res is not None:
                    ChefToDish.modify_remain(res.chef_id, res.dish_id, -orders[key])
                    price += dish[0]['dish_price'] * orders[key]
                else:
                    return False
        session = DBSession()
        session.add(Order(order_address_id=address_id,
                          order_delivery_id=delivery_id,
                          order_price=price,
                          order_start_time=start_time,
                          order_end_time=end_time,
                          order_remark=remark,
                          order_state=state))
        session.commit()
        session.close()
        order_id = Order.find_order(address_id=address_id, price=price, start_time=start_time)[0]['order_id']
        for key in orders:
            dish = Dish.find_dish(key)
            res = Hall.get_chef_id(dish[0]['dish_id'], hall_id)
            for i in range(0, orders[key]):
                OrderToRemain.new_connect(order_id, res.id)
        return True

    # 查询订单
    @staticmethod
    def find_order(order_id=None, address_id=None, state=None, start_time=None,
                   delivery_id=None, price=None, end_time=None, remark=None):
        if order_id is not None and not isinstance(order_id, int):
            raise Exception("Order id Error! It should be an Integer! Not ", order_id)
        if address_id is not None and not isinstance(address_id, int):
            raise Exception("Address id Error! It should be an Integer! Not ", address_id)
        if state is not None and state != 'AC' and state != 'ED' and state != 'NC':
            raise Exception("State Error! It should be AC, ED or NC! Not ", state)
        if start_time is not None and not isinstance(start_time, str):
            raise Exception("Start time Error! It should be a no none String! Not ", address_id)
        if delivery_id is not None and not isinstance(delivery_id, int):
            raise Exception("Delivery id Error! It should be an Integer! Not ", delivery_id)
        if price is not None and not isinstance(price, float):
            raise Exception("Price Error! It should be an Float! Not ", price)
        if end_time is not None and not isinstance(end_time, str):
            raise Exception("End time Error! It should be a String! Not ", end_time)
        if remark is not None and not isinstance(remark, str):
            raise Exception("Remark Error! It should be a String! Not ", remark)

        condition = (Order.order_id > 0)
        if order_id is not None:
            condition = and_(condition, Order.order_id == order_id)
        if address_id is not None:
            condition = and_(condition, Order.order_address_id == address_id)
        if delivery_id is not None:
            condition = and_(condition, Order.order_delivery_id == delivery_id)
        if price is not None:
            condition = and_(condition, Order.order_price == price)
        if start_time is not None:
            condition = and_(condition, Order.order_start_time == start_time)
        if end_time is not None:
            condition = and_(condition, Order.order_end_time == end_time)
        if remark is not None:
            condition = and_(condition, Order.order_remark == remark)
        if state is not None:
            condition = and_(condition, Order.order_state == state)
        session = DBSession()
        peter = session.query(Order).filter(condition).all()
        session.close()
        if peter is None:
            return None
        data = []
        for i in peter:
            dic = {
                'order_id': i.order_id,
                'order_address_id': i.order_address_id,
                'order_delivery_id': i.order_delivery_id,
                'order_price': i.order_price,
                'order_start_time': i.order_start_time,
                'order_end_time': i.order_end_time,
                'order_remark': i.order_remark,
                'order_state': i.order_state
            }
            data.append(dic)
        return data

    # 修改订单
    @staticmethod
    def modify_order(order_id, address_id=None, state=None, start_time=None,
                     delivery_id=None, price=None, end_time=None, remark=None):
        if order_id is None or not isinstance(order_id, int):
            raise Exception("Order id Error! It should be a no none Integer! Not ", order_id)
        if address_id is not None and not isinstance(address_id, int):
            raise Exception("Address id Error! It should be an Integer! Not ", address_id)
        if state is not None and state != 'AC' and state != 'ED' and state != 'NC':
            raise Exception("State Error! It should be AC, ED or NC! Not ", state)
        if start_time is not None and not isinstance(start_time, str):
            raise Exception("Start time Error! It should be a no none String! Not ", address_id)
        if delivery_id is not None and not isinstance(delivery_id, int):
            raise Exception("Delivery id Error! It should be an Integer! Not ", delivery_id)
        if price is not None and not isinstance(price, float):
            raise Exception("Price Error! It should be an Float! Not ", price)
        if end_time is not None and not isinstance(end_time, str):
            raise Exception("End time Error! It should be a String! Not ", end_time)
        if remark is not None and not isinstance(remark, str):
            raise Exception("Remark Error! It should be a String! Not ", remark)

        session = DBSession()
        order = session.query(Order).filter(Order.order_id == order_id).first()
        if address_id is not None:
            order.order_address_id = address_id
        if state is not None:
            order.order_state = state
        if delivery_id is not None:
            order.order_delivery_id = delivery_id
        if price is not None:
            order.order_price = price
        if start_time is not None:
            order.order_start_time = start_time
        if end_time is not None:
            order.order_end_time = end_time
        if remark is not None:
            order.order_remark = remark
        session.commit()
        session.close()


if __name__ == '__main__':
    print(Order.new_order(1, 'NC', {5: 2, 13: 6}, 3))
