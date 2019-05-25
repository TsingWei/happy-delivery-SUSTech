from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_
from user_all.dao import Chef
from user_all.dao import ChefToDish
from user_all.dao import Dish

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://'
                       'user_cs307:!2345678@129.204.93.30:3306/cs307')
DBSession = sessionmaker(bind=engine)


class Hall(Base):
    __tablename__ = 'hall'
    
    hall_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    hall_name = Column(String(45))

    # 新建食堂
    @staticmethod
    def new_hall(hall_name):
        if hall_name is None or not isinstance(hall_name, str):
            raise Exception("Hall name Error! It should be a no none String! Not ", hall_name)

        session = DBSession()
        session.add(Hall(hall_name=hall_name))
        session.commit()
        session.close()
        
    # 修改食堂
    @staticmethod
    def modify_hall(hall_id, hall_name):
        if hall_id is None or not isinstance(hall_id, str):
            raise Exception("Hall ID Error! It should be a no none Integer! Not ", hall_id)
        if hall_name is None or not isinstance(hall_name, str):
            raise Exception("Hall name Error! It should be a no none String! Not ", hall_name)

        session = DBSession()
        hall = session.query(Hall).filter(Hall.hall_id == hall_id).first()
        if hall_name is not None:
            hall.hall_name = hall_name
        session.commit()
        session.close()

    # 查看食堂下菜品
    @staticmethod
    def get_dishes(hall_id):
        if hall_id is None or not isinstance(hall_id, int):
            raise Exception("Hall ID Error! It should be a no none Integer! Not ", hall_id)

        session = DBSession()
        dish = session\
            .query(Hall.hall_id, Dish.dish_id, Dish.dish_image_path
                   , Dish.dish_description, Dish.dish_price, Dish.dish_name) \
            .order_by(Dish.dish_id) \
            .join(Chef, Chef.hall_id == Hall.hall_id)\
            .join(ChefToDish, ChefToDish.chef_id == Chef.chef_id)\
            .join(Dish, ChefToDish.dish_id == Dish.dish_id)\
            .filter(Hall.hall_id == hall_id)\
            .distinct().all()
        if dish is None:
            return []
        data = []
        for item in dish:
            dic = {
                'hall_id': item.hall_id,
                'dish_id': item.dish_id,
                'dish_name': item.dish_name,
                'dish_description': item.dish_description,
                'dish_image_path': item.dish_image_path,
                'dish_price': item.dish_price,
            }
            data.append(dic)
        return data

    # 获得chef to dish 中的id
    @staticmethod
    def get_chef_id(dish_id, hall_id):
        if dish_id is None or not isinstance(dish_id, int):
            raise Exception('Dish id Error! It should be a no none Integer! Not', dish_id)

        condition = (Hall.hall_id == hall_id)
        condition = and_(condition, Dish.dish_id == dish_id)
        condition = and_(condition, ChefToDish.remain > 0)
        session = DBSession()
        rid = session\
            .query(Dish.dish_id, ChefToDish.chef_id, ChefToDish.id)\
            .join(ChefToDish, Dish.dish_id == ChefToDish.dish_id)\
            .join(Chef, Chef.chef_id == ChefToDish.chef_id)\
            .join(Hall, Hall.hall_id == Chef.hall_id) \
            .filter(condition) \
            .first()
        if rid is None:
            return None
        session.commit()
        session.close()
        return rid


if __name__ == '__main__':
    for i in Hall.get_dishes(2):
        print(i)
    # print(Hall.get_chef_id(5, 1))
