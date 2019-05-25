from sqlalchemy import Column, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://'
                       'user_cs307:!2345678@129.204.93.30:3306/cs307')
DBSession = sessionmaker(bind=engine)


class ChefToDish(Base):
    __tablename__ = 'chef_to_dish'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    chef_id = Column(Integer)
    dish_id = Column(Integer)
    remain = Column(Integer)
    rank = Column(Integer)

    # 新增关系
    @staticmethod
    def new_connect(chef_id, dish_id, remain, rank):
        if chef_id is None or not isinstance(chef_id, int):
            raise Exception('Chef is Error! It should be a no none Integer! Not ', chef_id)
        if dish_id is None or not isinstance(dish_id, int):
            raise Exception('Dish is Error! It should be a no none Integer! Not ', dish_id)
        if remain is None or not isinstance(remain, int):
            raise Exception('Remain is Error! It should be a no none Integer! Not ', remain)
        if rank is None or not isinstance(rank, int):
            raise Exception('Rank is Error! It should be a no none Integer! Not ', rank)
        if ChefToDish.find_connect(chef_id, dish_id) is not None:
            raise Exception('Exist!')
        session = DBSession()
        session.add(ChefToDish(chef_id=chef_id,
                               dish_id=dish_id,
                               remain=remain,
                               rank=rank))
        session.commit()
        session.close()

    # 删除关系
    @staticmethod
    def del_connect(cid=None, chef_id=None, dish_id=None, remain=None, rank=None):
        if cid is not None and not isinstance(cid, int):
            raise Exception('ID is Error! It should be an Integer! Not ', chef_id)
        if chef_id is not None and not isinstance(chef_id, int):
            raise Exception('Chef is Error! It should be an Integer! Not ', chef_id)
        if dish_id is not None and not isinstance(dish_id, int):
            raise Exception('Dish is Error! It should be an Integer! Not ', dish_id)
        if remain is not None and not isinstance(remain, int):
            raise Exception('Remain is Error! It should be an Integer! Not ', remain)
        if rank is not None and not isinstance(rank, int):
            raise Exception('Rank is Error! It should be an Integer! Not ', rank)

        condition = (ChefToDish.id > 0)
        if cid is not None:
            condition = and_(condition, ChefToDish.id == cid)
        if chef_id is not None:
            condition = and_(condition, ChefToDish.chef_id == chef_id)
        if dish_id is not None:
            condition = and_(condition, ChefToDish.dish_id == dish_id)
        if remain is not None:
            condition = and_(condition, ChefToDish.remain == remain)
        if rank is not None:
            condition = and_(condition, ChefToDish.rank == rank)

        session = DBSession()
        session.query(ChefToDish).filter(condition).delete()
        session.commit()
        session.close()

    # 修改关系
    @staticmethod
    def modify_connect(chef_id, dish_id, remain=None, rank=None):
        if chef_id is None or not isinstance(chef_id, int):
            raise Exception('Chef is Error! It should be a no none Integer! Not ', chef_id)
        if dish_id is None or not isinstance(dish_id, int):
            raise Exception('Dish is Error! It should be a no none Integer! Not ', dish_id)
        if remain is not None and not isinstance(remain, int):
            raise Exception('Remain is Error! It should be an Integer! Not ', remain)
        if rank is not None and not isinstance(rank, int):
            raise Exception('Rank is Error! It should be an Integer! Not ', rank)
        if remain is None and rank is None:
            return
        session = DBSession()
        condition = (ChefToDish.chef_id == chef_id)
        condition = and_(condition, ChefToDish.dish_id == dish_id)
        peter = session.query(ChefToDish).filter(condition).first()
        if remain is not None:
            peter.remain = remain
        if rank is not None:
            peter.remain = remain
        session.commit()
        session.close()

    # 查找关系
    @staticmethod
    def find_connect(cid=None, chef_id=None, dish_id=None, remain=None, rank=None):
        if cid is not None and not isinstance(cid, int):
            raise Exception('ID is Error! It should be an Integer! Not ', chef_id)
        if chef_id is not None and not isinstance(chef_id, int):
            raise Exception('Chef is Error! It should be an Integer! Not ', chef_id)
        if dish_id is not None and not isinstance(dish_id, int):
            raise Exception('Dish is Error! It should be an Integer! Not ', dish_id)
        if remain is not None and not isinstance(remain, int):
            raise Exception('Remain is Error! It should be an Integer! Not ', remain)
        if rank is not None and not isinstance(rank, int):
            raise Exception('Rank is Error! It should be an Integer! Not ', rank)

        condition = (ChefToDish.id > 0)
        if cid is not None:
            condition = and_(condition, ChefToDish.id == cid)
        if chef_id is not None:
            condition = and_(condition, ChefToDish.chef_id == chef_id)
        if dish_id is not None:
            condition = and_(condition, ChefToDish.dish_id == dish_id)
        if remain is not None:
            condition = and_(condition, ChefToDish.remain == remain)
        if rank is not None:
            condition = and_(condition, ChefToDish.rank == rank)
        session = DBSession()
        peter = session.query(ChefToDish).filter(condition).all()
        session.close()
        if peter is None:
            return None
        data = []
        for i in peter:
            dic = {
                'id': i.id,
                'chef_id': i.chef_id,
                'dish_id': i.dish_id,
                'remain': i.remain,
                'rank': i.rank
            }
            data.append(dic)
        return data

    # 修改剩余量
    @staticmethod
    def modify_remain(chef_id, dish_id, remain):
        if chef_id is None or not isinstance(chef_id, int):
            raise Exception('Chef id is Error! It should be a no none Integer! Not ', chef_id)
        if dish_id is None or not isinstance(dish_id, int):
            raise Exception('Dish id is Error! It should be a no none Integer! Not ', dish_id)
        if remain is not None and not isinstance(remain, int):
            raise Exception('Remain is Error! It should be an Integer! Not ', remain)
        session = DBSession()
        condition = (ChefToDish.chef_id == chef_id)
        condition = and_(condition, ChefToDish.dish_id == dish_id)
        peter = session.query(ChefToDish).filter(condition).first()
        peter.remain += remain
        session.commit()
        session.close()
