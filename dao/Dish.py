from sqlalchemy import Column, String, create_engine, Integer, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://'
                       'user_cs307:!2345678@129.204.93.30:3306/cs307')
DBSession = sessionmaker(bind=engine)


class Dish(Base):
    __tablename__ = 'dish'

    dish_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    dish_name = Column(String(45), unique=True)
    dish_description = Column(String(45))
    dish_image_path = Column(String(45))
    dish_price = Column(Float)

    # 新增菜品
    @staticmethod
    def new_dish(dish_name, dish_description, dish_price, dish_image_path=None):
        if dish_name is None or not isinstance(dish_name, str):
            raise Exception("Dish name Error! It should be a no none String! Not ", dish_name)
        if dish_description is None or not isinstance(dish_description, str):
            raise Exception("Dish description Error! It should be a no none String! Not", dish_description)
        if dish_image_path is not None and not isinstance(dish_image_path, str):
            raise Exception("Dish image path Error! It should be a String! Not", dish_image_path)
        if dish_price is None or not isinstance(dish_price, float):
            raise Exception("Dish price Error! It should be a no none Float! Not ", dish_price)

        session = DBSession()
        session.add(Dish(dish_name=dish_name,
                         dish_description=dish_description,
                         dish_image_path=dish_image_path,
                         dish_price=dish_price))
        session.commit()
        session.close()

    # 查询菜品
    @staticmethod
    def find_dish(dish_id=None, dish_name=None, dish_description=None, dish_image_path=None, dish_price=None):
        if dish_id is not None and not isinstance(dish_id, int):
            raise Exception("Dish name Error! It should be an Integer! Not ", dish_id)
        if dish_name is not None and not isinstance(dish_name, str):
            raise Exception("Dish name Error! It should be a String! Not ", dish_name)
        if dish_description is not None and not isinstance(dish_description, str):
            raise Exception("Dish description Error! It should be a String! Not", dish_description)
        if dish_image_path is not None and not isinstance(dish_image_path, str):
            raise Exception("Dish image path Error! It should be a String! Not", dish_image_path)
        if dish_price is not None and not isinstance(dish_price, float):
            raise Exception("Dish price Error! It should be a Float! Not ", dish_price)
            
        data = []
        condition = (Dish.dish_id > 0)
        if dish_id is not None:
            condition = and_(condition, Dish.dish_id == dish_id)
        if dish_name is not None:
            condition = and_(condition, Dish.dish_name == dish_name)
        if dish_description is not None:
            condition = and_(condition, Dish.dish_description == dish_description)
        if dish_image_path is not None:
            condition = and_(condition, Dish.dish_image_path == dish_image_path)
        if dish_price is not None:
            condition = and_(condition, Dish.dish_price == dish_price)

        session = DBSession()
        peter = session.query(Dish).filter(condition).all()
        session.close()
        if peter is None:
            return data
        for item in peter:
            dic = {
                'dish_id': item.dish_id,
                'dish_name': item.dish_name,
                'dish_description': item.dish_description,
                'dish_image_path': item.dish_image_path,
                'dish_price': item.dish_price,
            }
            data.append(dic)
        return data

    # 修改菜品信息
    @staticmethod
    def modify_dish(dish_id, dish_name=None, dish_description=None, dish_image_path=None, dish_price=None):
        if dish_id is None or not isinstance(dish_id, int):
            raise Exception("Dish name Error! It should be a no none Integer! Not ", dish_id)
        if dish_name is not None and not isinstance(dish_name, str):
            raise Exception("Dish name Error! It should be a String! Not ", dish_name)
        if dish_description is not None and not isinstance(dish_description, str):
            raise Exception("Dish description Error! It should be a String! Not", dish_description)
        if dish_image_path is not None and not isinstance(dish_image_path, str):
            raise Exception("Dish image path Error! It should be a String! Not", dish_image_path)
        if dish_price is not None and not isinstance(dish_price, float):
            raise Exception("Dish price Error! It should be a Float! Not ", dish_price)

        session = DBSession()
        dish = session.query(Dish).filter(Dish.dish_id == dish_id).first()
        if dish_name is not None:
            dish.dish_name = dish_name
        if dish_description is not None:
            dish.dish_description = dish_description
        if dish_image_path is not None:
            dish.dish_image_path = dish_image_path
        if dish_price is not None:
            dish.dish_price = dish_price
        session.commit()
        session.close()


if __name__ == '__main__':
    # Dish.new_dish('新菜品', '新描述', 10086.1)
    # for i in Dish.find_dish(dish_name='新厨师'):
    #     Dish.modify_dish(i['dish_id'], dish_service_year=5, hall_id=3)
    print(Dish.find_dish(dish_name='新菜品'))
