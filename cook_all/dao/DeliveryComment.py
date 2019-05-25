from sqlalchemy import Column, create_engine, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://'
                       'user_cs307:!2345678@129.204.93.30:3306/cs307')
DBSession = sessionmaker(bind=engine)


class DeliveryComment(Base):
    __tablename__ = 'delivery_comment'

    comment_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    comment_userid = Column(Integer)
    comment_deliveryid = Column(Integer)
    comment_details = Column(String(45))
    comment_rank = Column(Integer)

    # 新建评论
    @staticmethod
    def new_comment(userid, deliveryid, details=None, rank=None):
        if userid is None or not isinstance(userid, int):
            raise Exception("User id Error! It should be a no none Ingeger! Not ", userid)
        if deliveryid is None or not isinstance(deliveryid, int):
            raise Exception("Deliveryid id Error! It should be a no none Ingeger! Not ", deliveryid)
        if details is not None and not isinstance(details, str):
            raise Exception("Details Error! It should be a String! Not ", details)
        if rank is not None and not isinstance(rank, int):
            raise Exception("Rank Error! It should be a String! Not ", rank)
        if rank is None and details is None:
            return
        session = DBSession()
        session.add(DeliveryComment(comment_userid=userid,
                                    comment_deliveryid=deliveryid,
                                    comment_details=details,
                                    comment_rank=rank))
        session.commit()
        session.close()

    # 查看评论
    @staticmethod
    def find_comment(comment_id=None, userid=None, deliveryid=None, details=None, rank=None):
        if comment_id is not None and not isinstance(comment_id, int):
            raise Exception("Comment id Error! It should be an Ingeger! Not ", comment_id)
        if userid is not None and not isinstance(userid, int):
            raise Exception("User id Error! It should be an Ingeger! Not ", userid)
        if deliveryid is not None and not isinstance(deliveryid, int):
            raise Exception("DishComment id Error! It should be an Ingeger! Not ", deliveryid)
        if details is not None and not isinstance(details, str):
            raise Exception("Details Error! It should be a String! Not ", details)
        if rank is not None and not isinstance(rank, int):
            raise Exception("Rank Error! It should be a String! Not ", rank)

        data = []
        condition = (DeliveryComment.comment_id > 0)
        if comment_id is not None:
            condition = and_(condition, DeliveryComment.comment_id == comment_id)
        if userid is not None:
            condition = and_(condition, DeliveryComment.comment_userid == userid)
        if deliveryid is not None:
            condition = and_(condition, DeliveryComment.comment_deliveryid == deliveryid)
        if details is not None:
            condition = and_(condition, DeliveryComment.comment_details == details)
        if rank is not None:
            condition = and_(condition, DeliveryComment.comment_rank == rank)

        session = DBSession()
        peter = session.query(DeliveryComment).filter(condition).all()
        session.close()
        if peter is None:
            return None
        for item in peter:
            dic = {
                'comment_id': item.comment_id,
                'comment_userid': item.comment_userid,
                'comment_deliveryid': item.comment_deliveryid,
                'comment_details': item.comment_details,
                'comment_rank': item.comment_rank
            }
            data.append(dic)
        return data


if __name__ == '__main__':
    print(DeliveryComment.find_comment(userid=5))
