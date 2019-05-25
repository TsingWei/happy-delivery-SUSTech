from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_

# 创建对象的基类:
Base = declarative_base()
# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://'
                       'user_cs307:!2345678@129.204.93.30:3306/cs307')
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)


# 定义Eater对象:
class Manager(Base):
    # 表的名字:
    __tablename__ = 'manager'

    # 表的结构:
    manager_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    manager_name = Column(String(45))
    manager_phone = Column(String(45))
    manager_hall_id = Column(Integer)


    #从食堂名字！！名字！！！获得这若干个
    @staticmethod
    def get_order_id_from_hall_name(hall):
        if isinstance(hall, String):
            try:
                session = DBSession()
                result = []
                # 查询
                sql = 'select DISTINCT  ORDER_ID from (select CHEF_ID,HALL_NAME from chef join hall on chef.HALL_ID=hall.HALL_ID )a join (select  DISTINCT ORDER_ID,CHEF_ID from order_to_remain join chef_to_dish on order_to_remain.CHEF_TO_DISH_ID=chef_to_dish.ID ORDER by order_to_remain.ORDER_ID)b on a.CHEF_ID=b.CHEF_ID and HALL_NAME=\'%s\'order by ORDER_ID;' % hall
                row = session.execute(sql)
                k=[]
                for r in row:
                    order_id = {
                        'id': r[0]
                    }
                    k.append(order_id)
                session.commit()
                session.close()

                return k
            except:
                print('查询失败')
            pass
        else:
            print('请输入正确的食堂名')

    #通过managerid获得这个manager所属的食堂名字,return list[字典]
    @staticmethod
    def get_hall_name_from_manager_id(managerid):
        if isinstance(managerid, int):
            try:
                session = DBSession()
                # 查询 select HALL_NAME from manager JOIN hall on MANAGER_HALL_ID=HALL_ID where MANAGER_ID="4";
                sql ='select HALL_NAME from manager JOIN hall on MANAGER_HALL_ID=HALL_ID where MANAGER_ID=\'%s\';'%managerid
                row = session.execute(sql)
                k=[]
                for r in row:
                    # print(r[0])
                    hall_name = {
                        'name': r[0]
                    }
                    k.append(hall_name)
                # print(type(k[0]))
                session.commit()
                session.close()
                # print(type(hall_name['name']))

                return k

            except:
                print('查询get_hall_name_from_manager_id失败')

            pass
        else:
            print("请输入正确的managerid")

    @staticmethod
    #通过订单号返回订单信息
    def get_order_from_order_id(orderid):
        if isinstance(orderid, int):
            try:
                session = DBSession()
                # 查询 select HALL_NAME from manager JOIN hall on MANAGER_HALL_ID=HALL_ID where MANAGER_ID="4";
                sql = 'select ORDER_ID,ORDER_STATE,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,' \
                      'ADDRESS_NAME,UID,ADDRESS_PHONE,DELIVERY_NAME,DELIVERY_PHONE from `order`join address join delivery on DELIVERY_ID=ORDER_DELIVERY_ID ' \
                      'and ORDER_ADDRESS_ID=ADDRESS_ID where ORDER_ID=\'%s\';' % orderid
                # sql='select ORDER_ID,ORDER_STATE,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,ADDRESS_NAME,UID,ADDRESS_PHONE,DELIVERY_NAME,DELIVERY_PHONE from `order`join address join delivery on DELIVERY_ID=ORDER_DELIVERY_ID and ORDER_ADDRESS_ID=ADDRESS_ID where ORDER_ID=\'222\';'
                row = session.execute(sql)
                k = []
                for r in row:
                    order={
                        'order_id':r[0],
                        'order_state':r[1],
                        'order_price':r[2],
                        'order_start_time':r[3],
                        'order_end_time':r[4],
                        'order_remark':r[5],
                        'address_name':r[6],
                        'uid':r[7],
                        'address_phone':r[8],
                        'delivery_name':r[9],
                        'delivery_phone':r[10]
                    }
                    k.append(order)
                session.commit()
                session.close()
                return k

            except:
                print('查询失败:订单号返回订单信息')

            pass
        else:
            print("请输入正确的订单号")

    #通过管理员id获得管理员可管理的所有订单
    @staticmethod
    def get_order_from_manager_id(managerid):
        if isinstance(managerid, int):
            try:
                session = DBSession()
                sql = 'select DISTINCT e.ORDER_ID,ORDER_STATE,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,ADDRESS_NAME,UID,ADDRESS_PHONE,DELIVERY_NAME,DELIVERY_PHONE ' \
                      'from (select DISTINCT ORDER_ID,ORDER_STATE,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,ADDRESS_NAME,UID,ADDRESS_PHONE,DELIVERY_NAME,DELIVERY_PHONE from `' \
                      'order`join address join delivery on DELIVERY_ID=ORDER_DELIVERY_ID and ORDER_ADDRESS_ID=ADDRESS_ID order by ORDER_ID)e join (select DISTINCT ORDER_ID from ' \
                      '(select HALL_NAME from manager JOIN hall on MANAGER_HALL_ID=HALL_ID where MANAGER_ID=\'%s\')c join (select HALL_NAME,ORDER_ID from (select CHEF_ID,HALL_NAME from ' \
                      'chef join hall on chef.HALL_ID=hall.HALL_ID )a join (select  DISTINCT ORDER_ID,CHEF_ID from order_to_remain join chef_to_dish ' \
                      'on order_to_remain.CHEF_TO_DISH_ID=chef_to_dish.ID ORDER by order_to_remain.ORDER_ID)b on a.CHEF_ID=b.CHEF_ID ORDER BY ORDER_ID)d on c.HALL_NAME=d.HALL_NAME )f ' \
                      'on e.ORDER_ID=f.ORDER_ID order by e.ORDER_ID;' % managerid
                row = session.execute(sql)
                k = []
                for r in row:
                    # print(r)
                    order = {
                        'order_id': r[0],
                        'order_state': r[1],
                        'order_price': r[2],
                        'order_start_time': r[3],
                        'order_end_time': r[4],
                        'order_remark': r[5],
                        'address_name': r[6],
                        'uid': r[7],
                        'address_phone': r[8],
                        'delivery_name': r[9],
                        'delivery_phone': r[10]
                    }
                    k.append(order)

                session.commit()
                session.close()
                return k

            except:
                print('查询失败：通过管理员id获得管理员可管理的所有订单')
            pass
        else:
            print("请输入正确的manager")

    # 通过managerid 获得对应食堂的菜品评论信息
    @staticmethod
    def get_dish_comment_from_manager_id(managerid):
        if isinstance(managerid, int):
            try:
                session = DBSession()
                sql = 'select DISTINCT e.ORDER_ID,ORDER_STATE,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,ADDRESS_NAME,UID,ADDRESS_PHONE,DELIVERY_NAME,DELIVERY_PHONE from (select DISTINCT ORDER_ID,ORDER_STATE,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,ADDRESS_NAME,UID,ADDRESS_PHONE,DELIVERY_NAME,DELIVERY_PHONE from `order`join address join delivery on DELIVERY_ID=ORDER_DELIVERY_ID and ORDER_ADDRESS_ID=ADDRESS_ID order by ORDER_ID)e join (select DISTINCT ORDER_ID from (select HALL_NAME from manager JOIN hall on MANAGER_HALL_ID=HALL_ID where MANAGER_ID=\'%s\')c join (select HALL_NAME,ORDER_ID from (select CHEF_ID,HALL_NAME from chef join hall on chef.HALL_ID=hall.HALL_ID )a join (select  DISTINCT ORDER_ID,CHEF_ID from order_to_remain join chef_to_dish on order_to_remain.CHEF_TO_DISH_ID=chef_to_dish.ID ORDER by order_to_remain.ORDER_ID)b on a.CHEF_ID=b.CHEF_ID ORDER BY ORDER_ID)d on c.HALL_NAME=d.HALL_NAME )f on e.ORDER_ID=f.ORDER_ID order by e.ORDER_ID;' % managerid


                row = session.execute(sql)
                k = []
                for r in row:

                    dish_comment={
                        'order_id': r[0],
                        'order_state': r[1],
                        'order_price': r[2],
                        'order_start_time': r[3],
                        'order_end_time': r[4],
                        'order_remark': r[5],
                        'address_name': r[6],
                        'uid': r[7],
                        'address_phone': r[8],
                        'delivery_name': r[9],
                        'delivery_phone': r[10]

                    }
                    k.append(dish_comment)
                session.commit()
                session.close()
                return k

            except:
                print('查询失败')
                return [-999]
            pass
        else:
            print("请输入正确的manager")

    # 通过managerid 获得对应食堂的总平均评论rank
    @staticmethod
    def get_dish_comment_rank_from_manager_id(managerid):
        if isinstance(managerid, int):
            try:

                session = DBSession()
                sql = 'select DISTINCT  MANAGER_ID, HALL_NAME,avg(COMMENT_RANK) ' \
                      'from (select * from dish_comment join dish join chef on dish.DISH_ID=dish_comment.COMMENT_DISHID ORDER BY' \
                      ' chef.HALL_ID,DISH_NAME)a join  (select HALL_ID, HALL_NAME,MANAGER_ID from manager JOIN hall' \
                      ' on MANAGER_HALL_ID=HALL_ID where MANAGER_ID=\'%s\')b on a.HALL_ID=b.HALL_ID;' % managerid
                row = session.execute(sql)
                k = []

                for r in row:
                    dish_comment_rank={
                        'manager_id': r[0],
                        'hall_name': r[1],
                        'rank': r[2]

                    }
                    k.append(dish_comment_rank)
                session.commit()
                session.close()
                return k

            except:
                print('查询失败')
                return [-999]
            pass
        else:
            print("请输入正确的managerid")

    # 通过managerid获得管理的厨师的平均rank
    @staticmethod
    def get_chef_rank_from_manager_id(managerid):
        if isinstance(managerid, int):
            try:
                session = DBSession()
                k = []
                sql = 'select MANAGER_HALL_ID from manager  where MANAGER_ID=\'%s\';' % managerid
                hall_all_id = session.execute(sql)
                for hall in hall_all_id:
                    hall_id = hall[0]
                    # print(hall[0])
                    sql0 = 'select   HALL_NAME,CHEF_NAME,avg(COMMENT_RANK) from ( select  hall.HALL_NAME as HALL_NAME,CHEF_NAME,COMMENT_RANK from dish_comment ' \
                          'join dish join chef join hall  on  dish.DISH_ID=dish_comment.COMMENT_DISHID and COMMENT_CHEFID=CHEF_ID ' \
                          'and hall.HALL_ID=chef.HALL_ID  AND chef.HALL_ID=\'%s\')a group by CHEF_NAME;' % hall_id
                    row = session.execute(sql0)
                    for r in row:
                        rank={
                            'hall_name':r[0],
                            'chef_name': r[1],
                            'rank': r[2]

                        }
                        k.append(rank)
                session.commit()
                session.close()
                return k

            except:
                print('查询失败')
                return [-999]
            pass
        else:
            print("请输入正确的managerid")

    #通过hallid获得管理的厨师的平均rank
    @staticmethod
    def get_chef_rank_from_hall_id(hallid):
        if isinstance(hallid, int):
            try:
                session = DBSession()
                sql = 'select   HALL_NAME,CHEF_NAME,avg(COMMENT_RANK) from ( select  hall.HALL_NAME as HALL_NAME,CHEF_NAME,COMMENT_RANK from dish_comment ' \
                      'join dish join chef join hall  on  dish.DISH_ID=dish_comment.COMMENT_DISHID and COMMENT_CHEFID=CHEF_ID ' \
                      'and hall.HALL_ID=chef.HALL_ID  AND chef.HALL_ID=\'%s\')a group by CHEF_NAME;' % hallid
                row = session.execute(sql)
                k = []
                for r in row:
                    a={
                        'hall_name':r[0],
                        'chef_name':r[1],
                        'rank':r[2]
                    }
                    k.append(a)
                session.commit()
                session.close()
                return k

            except:
                print('查询失败')
                return [-999]
            pass
        else:
            print("请输入正确的hallid")

    @staticmethod
    # 通过managerid获得管理的厨师的平均rank
    def get_dish_rank_from_manager_id(managerid):
        if isinstance(managerid, int):
            try:
                k = []
                session = DBSession()
                sql = 'select MANAGER_HALL_ID from manager  where MANAGER_ID=\'%s\';' % managerid
                hall_all_id = session.execute(sql)
                for hall in hall_all_id:
                    hall_id = hall[0]
                    sql1 = 'select   HALL_NAME,DISH_NAME,avg(COMMENT_RANK) from (select  hall.HALL_NAME as HALL_NAME,DISH_NAME,COMMENT_RANK from ' \
                          'dish_comment join dish join chef join hall  on ' \
                          'dish.DISH_ID=dish_comment.COMMENT_DISHID and COMMENT_CHEFID=CHEF_ID and hall.HALL_ID=chef.HALL_ID  AND chef.HALL_ID=\'%s\' )a group by DISH_NAME;' % hall_id
                    row = session.execute(sql1)
                    for r in row:
                        a = {
                            'hall_name': r[0],
                            'chef_name': r[1],
                            'rank': r[2]
                        }
                        k.append(a)
                session.commit()
                session.close()
                return k

            except:
                print('查询失败')
                return [-999]
            pass
        else:
            print("请输入正确的managerid")

    @staticmethod
    #通过hallid获得管理的厨师的平均rank
    def get_dish_rank_from_hall_id(hallid):
        if isinstance(hallid, int):
            try:
                session = DBSession()
                sql = 'select   HALL_NAME,DISH_NAME,avg(COMMENT_RANK) from (select  hall.HALL_NAME as HALL_NAME,DISH_NAME,COMMENT_RANK from ' \
                      'dish_comment join dish join chef join hall  on ' \
                      'dish.DISH_ID=dish_comment.COMMENT_DISHID and COMMENT_CHEFID=CHEF_ID and hall.HALL_ID=chef.HALL_ID  AND chef.HALL_ID=\'%s\' )a group by DISH_NAME;' % hallid
                row = session.execute(sql)
                k = []
                for r in row:
                    a = {
                        'hall_name': r[0],
                        'chef_name': r[1],
                        'rank': r[2]
                    }
                    k.append(a)
                session.commit()
                session.close()
                return k

            except:
                print('查询失败')
                return [-999]
            pass
        else:
            print("请输入正确的hallid")

    @staticmethod
    # 通过managerid获得剩余量
    def get_remain_from_manager_id(managerid):
        if isinstance(managerid, int):
            try:
                session = DBSession()
                sql = 'select DISTINCT  HALL_NAME,CHEF_NAME,DISH_NAME,REMAIN,dish.DISH_PRICE from (select HALL_NAME,CHEF_NAME,REMAIN,DISH_ID ' \
                      'from (select HALL_NAME,CHEF_NAME,CHEF_ID from (select HALL_ID,HALL_NAME from manager JOIN hall on MANAGER_HALL_ID=HALL_ID where MANAGER_ID=\'%s\')a ' \
                      'join (select CHEF_ID,CHEF_NAME,chef.HALL_ID AS HALL_ID from chef join hall on chef.HALL_ID=hall.HALL_ID )b on a.HALL_ID=b.HALL_ID )c' \
                      ' join chef_to_dish on c.CHEF_ID=chef_to_dish.CHEF_ID)d join dish on dish.DISH_ID=d.DISH_ID;' % managerid
                row = session.execute(sql)
                k = []
                for r in row:
                    a={
                        'hall_name':r[0],
                        'chef_name': r[1],
                        'dish_name': r[2],
                        'remain_name': r[3],
                        'dish_price': r[4],

                    }
                    k.append(a)
                session.commit()
                session.close()
                return k

            except:
                print('查询失败')
            pass
        else:
            print("managerid啊")

    @staticmethod
    #通过id和remain设置菜品剩余量
    def set_chef_to_dish_by_remain_id(remain,id):
        if isinstance(remain, int)or isinstance(id, int):
            sql='update chef_to_dish  set REMAIN= \'%s\' where ID = \'%s\';'%(remain,id)
            try:
                session = DBSession()
                # 执行sql语句
                session.execute(sql)
                # 提交到数据库执行
                session.commit()
                session.close()
            except:
                # Rollback in case there is any error
                session.rollback()
                print('修改失败')
            pass
        else:
            print("please check argument")

    @staticmethod
    #通过remain设置菜品剩余量
    def set_chef_to_dish_by_remain(remain):
        if isinstance(remain, int) :
            sql='update chef_to_dish set REMAIN=\'%s\' WHERE ID>=1;'%remain
            try:
                session = DBSession()
                session.execute(sql)
                # 提交到数据库执行
                session.commit()
                session.close()
            except:
                session.rollback()
                print('修改失败')
            pass
        else:
            print("please check argument")

    @staticmethod
    #通过id减少菜品数量1
    def set_chef_to_dish_by_id_change(id,add):
        if isinstance(add,int) or isinstance(id, int):
            session = DBSession()
            sql0='select REMAIN from chef_to_dish where ID=\'%s\';'%id
            row = session.execute(sql0)
            for r in row:
                number =r[0]
            number=number+add
            if number>=0 :
                sql = 'update chef_to_dish  set REMAIN= \'%s\' where ID = \'%s\';' % (number, id)
                session.execute(sql)

            else:
                print('减去后菜品数量小于0')
            session.commit()
            session.close()

            pass
        else:
            print("please input correct argument")



if __name__ == '__main__':

    result = Manager.set_chef_to_dish_by_id_change(1,1)
    # for i in result:
    #     print(i)

    # print(d1)

    # dish = {
    #     'id': i[1],
    #     'state': i[2],
    # }