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

    #===============================================================================================
    #通过chefid 获得厨师的评论
    @staticmethod
    def get_dish_comment_from_chef_id(chefid):
        if isinstance(chefid, int):
            try:
                session = DBSession()
                sql='select CHEF_NAME,DISH_NAME,COMMENT_DETAILS,COMMENT_RANK from (select * from dish_comment join chef join dish on ' \
                    'COMMENT_CHEFID=CHEF_ID and COMMENT_DISHID=DISH_ID  where COMMENT_CHEFID=\'%s\' order by DISH_NAME)a ' \
                    'join (select DISH_ID from chef_to_dish where CHEF_ID=\'%s\')b on a.DISH_ID=b.DISH_ID;'%(chefid,chefid)
                row = session.execute(sql)
                k=[]
                for r in row:
                    a = {
                        'chef_name':r[0],
                        'dish_name': r[1],
                        'comment_detail': r[2],
                        'comment_rank': r[3]

                    }
                    k.append(a)
                session.commit()
                session.close()
                return k

            except:
                print('查询失败')
            pass
        else:
            print("please input correct chef id")

    @staticmethod
    #通过chefid 获得厨师的评分  \'%s\'
    def get_chef_rank_from_chef_id(chefid):
        if isinstance(chefid, int):
            try:
                session = DBSession()
                sql='select CHEF_NAME,avg(COMMENT_RANK) from(select * from dish_comment join chef join dish on ' \
                    'COMMENT_CHEFID=CHEF_ID and COMMENT_DISHID=DISH_ID  where COMMENT_CHEFID=\'%s\' order by DISH_NAME)a ' \
                    'join (select DISH_ID from chef_to_dish where CHEF_ID=\'%s\')b on a.DISH_ID=b.DISH_ID ;'%(chefid,chefid)
                row = session.execute(sql)
                k=[]
                for r in row:
                    a={
                        'chef_name':r[0],
                        'rank':r[1]
                    }
                    k.append(a)
                session.commit()
                session.close()
                return k

            except:
                print('查询失败')
            pass
        else:
            print("please input correct chef id")

    @staticmethod
    #通过chefid 获得厨师的菜的评分  \'%s\'
    def get_dish_rank_from_chef_id(chefid):
        if isinstance(chefid, int):
            try:
                session = DBSession()
                sql = 'select CHEF_NAME,DISH_NAME,avg(COMMENT_RANK) from(select * from dish_comment join chef join dish on ' \
                      'COMMENT_CHEFID=CHEF_ID and COMMENT_DISHID=DISH_ID  where COMMENT_CHEFID=\'%s\' order by DISH_NAME)a ' \
                      'join (select DISH_ID from chef_to_dish where CHEF_ID=\'%s\')b on a.DISH_ID=b.DISH_ID group by DISH_NAME ;' % (
                      chefid, chefid)
                row = session.execute(sql)
                k=[]
                for r in row:
                    a = {
                        'chef_name': r[0],
                        'dish_name': r[1],
                        'rank': r[2]
                    }
                    k.append(a)

                session.commit()
                session.close()
                return k

            except:
                print('查询失败')
            pass
        else:
            print("please input correct chef id")

    @staticmethod
    #通过CHEFid设置厨师所属食堂
    def set_chef_hall_by_chef_id(chefid,hallid):
        if isinstance(chefid, int) and isinstance(hallid, int):
            session = DBSession()
            sql0='select HALL_ID from hall'
            row = session.execute(sql0)
            hall=[]
            for r in row:
               hall.append(r[0])
            pd=0
            for i in hall:
                if (hallid==i):
                    pd=1
            if (pd==0):
                print("你想上天？")

            try:
                sql = 'update chef set HALL_ID=\'%s\' WHERE CHEF_ID=\'%s\';' % (hallid, chefid)
                session.execute(sql)
                session.commit()
            except:
                session.rollback()
                print('查询失败')
                return [-999]
            session.commit()
            session.close()
            pass
        else:
            print("please input correct chef id")

    @staticmethod
    #通过DISHID 设置菜品价格
    def set_dish_price_by_dish_id(dishid,price):
        if isinstance(dishid, int)and isinstance(price, int):
            try:
                session = DBSession()
                sql = 'update dish set DISH_PRICE=\'%s\' WHERE DISH_ID=\'%s\';' % (price, dishid)
                session.execute(sql)
                session.commit()
                session.close()
            except:
                print('查询失败')

            pass
        else:
            print("please input correct chef id")
    @staticmethod
    #通过DISHID 设置菜品描述
    def set_dish_description_by_dish_id(dishid,description):
        if isinstance(dishid, int) and isinstance(description,str):
            try:
                session = DBSession()
                sql = 'update dish set DISH_DESCRIPTION=\'%s\' WHERE DISH_ID=\'%s\';' % (description, dishid)
                session.execute(sql)
                session.commit()
            except:
                print('查询失败')
            pass
        else:
            print("please input correct dishid,description")

    @staticmethod
    #通过chefid ,dishid 为厨师添加菜品
    def add_dish_from_chef_id(chefid,dishid):
        if isinstance(dishid, int) and isinstance(dishid, int):
            sql = 'insert into chef_to_dish  (CHEF_ID,DISH_ID,REMAIN,`RANK`)VALUES(\'%s\',\'%s\',0,0);' % (chefid, dishid)
            try:
                session = DBSession()
                # 执行sql语句
                session.execute(sql)
                # 提交到数据库执行
                session.commit()
                session.close()
            except:
                # Rollback in case there is any error
                print('插入失败')
            pass
        else:
            print("please input correct chefid, dishid")

    @staticmethod
    #通过chefid ,dishid 为厨师删除菜品
    def delete_dish_from_chef_id(chefid,dishid):
        if isinstance(dishid, int) and isinstance(dishid, int):
            sql = 'delete from chef_to_dish where CHEF_ID=\'%s\' AND DISH_ID=\'%s\';' % (chefid, dishid)
            session = DBSession()
            try:
                # 执行sql语句
                session.execute(sql)
                # 提交到数据库执行
                session.commit()
                return [1]
            except:
                # Rollback in case there is any error
                session.rollback()
                print('插入失败')
                return [0]
            session.close()
        else:
            print("please input correct chefid, dishid")


if __name__ == '__main__':
    # Chef.new_chef('新厨师', 5)
    # for i in Chef.find_chef(chef_name='新厨师'):
    #     Chef.modify_chef(i['chef_id'], chef_service_year=5, hall_id=3)
    # print(Chef.find_chef(chef_name='新厨师'))
    # Chef.del_chef(chef_name='新厨师')
    k='asdadasd'
    Chef.delete_dish_from_chef_id(4,5)