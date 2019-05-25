from sqlalchemy import Column, create_engine, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://'
                       'user_cs307:!2345678@129.204.93.30:3306/cs307')
DBSession = sessionmaker(bind=engine)


class DishComment(Base):
    __tablename__ = 'dish_comment'

    comment_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    comment_userid = Column(Integer)
    comment_chefid = Column(Integer)
    comment_dishid = Column(Integer)
    comment_details = Column(String(45))
    comment_rank = Column(Integer)

    # 新建评论
    @staticmethod
    def new_comment(userid, chefid, dishid, details=None, rank=None):
        if userid is None or not isinstance(userid, int):
            raise Exception("User id Error! It should be a no none Ingeger! Not ", userid)
        if chefid is None or not isinstance(chefid, int):
            raise Exception("Chef id Error! It should be a no none Ingeger! Not ", chefid)
        if dishid is None or not isinstance(dishid, int):
            raise Exception("Dish id Error! It should be a no none Ingeger! Not ", dishid)
        if details is not None and not isinstance(details, str):
            raise Exception("Details Error! It should be a String! Not ", details)
        if rank is not None and not isinstance(rank, int):
            raise Exception("Rank Error! It should be a String! Not ", rank)
        if rank is None and details is None:
            return
        session = DBSession()
        session.add(DishComment(comment_userid=userid,
                                comment_chefid=chefid,
                                comment_commentid=dishid,
                                comment_details=details,
                                comment_rank=rank))
        session.commit()
        session.close()

    # 查看评论
    @staticmethod
    def find_comment(comment_id=None, userid=None, chefid=None, dishid=None, details=None, rank=None):
        if comment_id is not None and not isinstance(comment_id, int):
            raise Exception("Comment id Error! It should be an Ingeger! Not ", comment_id)
        if userid is not None and not isinstance(userid, int):
            raise Exception("User id Error! It should be an Ingeger! Not ", userid)
        if chefid is not None and not isinstance(chefid, int):
            raise Exception("Chef id Error! It should be an Ingeger! Not ", chefid)
        if dishid is not None and not isinstance(dishid, int):
            raise Exception("DishComment id Error! It should be an Ingeger! Not ", dishid)
        if details is not None and not isinstance(details, str):
            raise Exception("Details Error! It should be a String! Not ", details)
        if rank is not None and not isinstance(rank, int):
            raise Exception("Rank Error! It should be a String! Not ", rank)
        
        data = []
        condition = (DishComment.comment_id > 0)
        if comment_id is not None:
            condition = and_(condition, DishComment.comment_id == comment_id)
        if userid is not None:
            condition = and_(condition, DishComment.comment_userid == userid)
        if chefid is not None:
            condition = and_(condition, DishComment.comment_chefid == chefid)
        if dishid is not None:
            condition = and_(condition, DishComment.comment_dishid == dishid)
        if details is not None:
            condition = and_(condition, DishComment.comment_details == details)
        if rank is not None:
            condition = and_(condition, DishComment.comment_rank == rank)

        session = DBSession()
        peter = session.query(DishComment).filter(condition).all()
        session.close()
        if peter is None:
            return None
        for item in peter:
            dic = {
                'comment_id': item.comment_id,
                'comment_userid': item.comment_userid,
                'comment_chefid': item.comment_chefid,
                'comment_dishid': item.comment_dishid,
                'comment_details': item.comment_details,
                'comment_rank': item.comment_rank
            }
            data.append(dic)
        return data


if __name__ == '__main__':
    print(DishComment.find_comment(userid=5))
