from sqlalchemy import Column, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

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