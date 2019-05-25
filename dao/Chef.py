from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://'
                       'user_cs307:!2345678@129.204.93.30:3306/cs307')
DBSession = sessionmaker(bind=engine)


class Chef(Base):
    __tablename__ = 'chef'

    chef_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    chef_service_year = Column(Integer)
    chef_name = Column(String(45))
    chef_rank = Column(Integer)
    hall_id = Column(Integer)

    # 新建厨师
    @staticmethod
    def new_chef(chef_name, chef_rank, chef_service_year=None, hall_id=None):
        if chef_name is None or not isinstance(chef_name, str):
            raise Exception("Chef name Error! Must be a no none String ! not ", chef_name)
        if chef_rank is None or not isinstance(chef_rank, int):
            raise Exception("Chef rank Error! Must be a no none Integer ! not ", chef_rank)
        if chef_service_year is not None and not isinstance(chef_service_year, int):
            raise Exception("Chef service year Error! Must be an Integer ! not ", chef_service_year)
        if hall_id is not None and not isinstance(hall_id, int):
            raise Exception("Hall id Error! Must be an Integer ! not ", hall_id)

        session = DBSession()
        session.add(Chef(chef_name=chef_name,
                         chef_service_year=chef_service_year,
                         chef_rank=chef_rank,
                         hall_id=hall_id))
        session.commit()
        session.close()
        
    # 查询厨师信息
    @staticmethod
    def find_chef(chef_id=None, chef_name=None, chef_service_year=None, chef_rank=None, hall_id=None):
        if chef_id is not None and not isinstance(chef_id, int):
            raise Exception("Chef id  Error! It must be an Integer! Not ", chef_id)
        if chef_name is not None and not isinstance(chef_name, str):
            raise Exception("Chef name Error! It must be a String! Not ", chef_id)
        if chef_service_year is not None and not isinstance(chef_service_year, int):
            raise Exception("Chef service year Error! It must be an Integer! Not ", chef_service_year)
        if chef_rank is not None and not isinstance(chef_rank, int):
            raise Exception("Chef rank Error! It must be an Integer! Not ", chef_rank)
        if hall_id is not None and not isinstance(hall_id, int):
            raise Exception("Hall id Error! It must be an Integer! Not ", hall_id)

        data = []
        condition = (Chef.chef_id > 0)
        if chef_id is not None:
            condition = and_(condition, Chef.chef_id == chef_id)
        if chef_name is not None:
            condition = and_(condition, Chef.chef_name == chef_name)
        if chef_rank is not None:
            condition = and_(condition, Chef.chef_rank == chef_rank)
        if hall_id is not None:
            condition = and_(condition, Chef.hall_id == hall_id)
        if chef_service_year is not None:
            condition = and_(condition, Chef.chef_service_year == chef_service_year)
        
        session = DBSession()
        peter = session.query(Chef).filter(condition).all()
        session.close()
        if peter is None:
            return data
        for item in peter:
            dic = {
                'chef_id': item.chef_id,
                'chef_name': item.chef_name,
                'chef_service_year': item.chef_service_year,
                'chef_rank': item.chef_rank,
                'hall_id': item.hall_id,
            }
            data.append(dic)
        return data
        
    # 修改厨师信息
    @staticmethod
    def modify_chef(chef_id, chef_name=None, chef_service_year=None, chef_rank=None, hall_id=None):
        if chef_id is None or not isinstance(chef_id, int):
            raise Exception("Chef id  Error! It must be a no none Integer! Not ", chef_id)
        if chef_name is not None and not isinstance(chef_name, str):
            raise Exception("Chef name Error! It must be a String! Not ", chef_id)
        if chef_service_year is not None and not isinstance(chef_service_year, int):
            raise Exception("Chef service year Error! It must be an Integer! Not ", chef_service_year)
        if chef_rank is not None and not isinstance(chef_rank, int):
            raise Exception("Chef rank Error! It must be an Integer! Not ", chef_rank)
        if hall_id is not None and not isinstance(hall_id, int):
            raise Exception("Hall id Error! It must be an Integer! Not ", hall_id)
        
        session = DBSession()
        chef = session.query(Chef).filter(Chef.chef_id == chef_id).first()
        if chef_name is not None:
            chef.chef_name = chef_name
        if chef_service_year is not None:
            chef.chef_service_year = chef_service_year
        if chef_rank is not None:
            chef.chef_rank = chef_rank
        if hall_id is not None:
            chef.hall_id = hall_id
        session.commit()
        session.close()

    # 删除厨师信息
    @staticmethod
    def del_chef(chef_id=None, chef_name=None, chef_service_year=None, chef_rank=None, hall_id=None):
        if chef_id is not None and not isinstance(chef_id, int):
            raise Exception("Chef id  Error! It must be an Integer! Not ", chef_id)
        if chef_name is not None and not isinstance(chef_name, str):
            raise Exception("Chef name Error! It must be a String! Not ", chef_id)
        if chef_service_year is not None and not isinstance(chef_service_year, int):
            raise Exception("Chef service year Error! It must be an Integer! Not ", chef_service_year)
        if chef_rank is not None and not isinstance(chef_rank, int):
            raise Exception("Chef rank Error! It must be an Integer! Not ", chef_rank)
        if hall_id is not None and not isinstance(hall_id, int):
            raise Exception("Hall id Error! It must be an Integer! Not ", hall_id)

        condition = (Chef.chef_id > 0)
        if chef_id is not None:
            condition = and_(condition, Chef.chef_id == chef_id)
        if chef_name is not None:
            condition = and_(condition, Chef.chef_name == chef_name)
        if chef_rank is not None:
            condition = and_(condition, Chef.chef_rank == chef_rank)
        if hall_id is not None:
            condition = and_(condition, Chef.hall_id == hall_id)
        if chef_service_year is not None:
            condition = and_(condition, Chef.chef_service_year == chef_service_year)

        session = DBSession()
        session.query(Chef).filter(condition).delete()
        session.commit()
        session.close()


if __name__ == '__main__':
    Chef.new_chef('新厨师', 5)
    for i in Chef.find_chef(chef_name='新厨师'):
        Chef.modify_chef(i['chef_id'], chef_service_year=5, hall_id=3)
    print(Chef.find_chef(chef_name='新厨师'))
    Chef.del_chef(chef_name='新厨师')
