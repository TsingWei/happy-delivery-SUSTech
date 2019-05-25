import pymysql
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


def check():
    try:
        # 查询
        row = session.execute('select * from dish;')
        for r in row:
            print(r)
    except:
        print('查询失败')
    pass


def add():
    USER_NAME='test'
    USER_GENDER='M'
    USER_SID='11111111'
    USER_PHONE='11111111'
    USER_TYPE='STUDENT'
    sql='insert into user (USER_NAME, USER_GENDER, USER_SID, USER_PHONE, USER_TYPE)values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');'%(USER_NAME,USER_GENDER,USER_SID,USER_PHONE,USER_TYPE)
    try:
        # 执行sql语句
        session.execute(sql)
        # 提交到数据库执行
        session.commit()
    except:
        # Rollback in case there is any error
        session.rollback()
        print('插入失败')
    pass


def delete():
    TABLE = 'user'
    USER_SID='11111111'
    sql='delete from %s where USER_SID = \'%s\';'%(TABLE,USER_SID)

    try:
        # 执行sql语句
        session.execute(sql)
        # 提交到数据库执行
        session.commit()
    except:
        # Rollback in case there is any error
        session.rollback()
        print('删除失败')
    pass


def update():
    TABLE = 'user'
    USER_SID='11111111'
    MODIFY_COLUMN = 'USER_NAME'
    MODIFY_VALUE = 'haha'
    sql='update %s set %s = \'%s\' where USER_SID = \'%s\';'%(TABLE,MODIFY_COLUMN,MODIFY_VALUE,USER_SID)

    try:
        # 执行sql语句
        session.execute(sql)
        # 提交到数据库执行
        session.commit()
    except:
        # Rollback in case there is any error
        session.rollback()
        print('修改失败')
    pass

#======================食堂负责人部分开始=================================================

def get_order_id_from_hall_name(hall):
    try:
        result=[]
        for h in hall:
            # 查询
            sql ='select DISTINCT  ORDER_ID from (select CHEF_ID,HALL_NAME from chef join hall on chef.HALL_ID=hall.HALL_ID )a join (select  DISTINCT ORDER_ID,CHEF_ID from order_to_remain join chef_to_dish on order_to_remain.CHEF_TO_DISH_ID=chef_to_dish.ID ORDER by order_to_remain.ORDER_ID)b on a.CHEF_ID=b.CHEF_ID and HALL_NAME=\'%s\'order by ORDER_ID;'%h
            row = session.execute(sql)

            for r in row:
                result.append(r[0])
        return result
    except:
        print('查询失败')
    pass

#通过managerid获得这个manager所属的食堂名字,return 一个第一个获得的字符串
def get_hall_name_from_manager_id(managerid):
    try:
        # 查询 select HALL_NAME from manager JOIN hall on MANAGER_HALL_ID=HALL_ID where MANAGER_ID="4";
        sql ='select HALL_NAME from manager JOIN hall on MANAGER_HALL_ID=HALL_ID where MANAGER_ID=\'%s\';'%managerid
        row = session.execute(sql)
        k=[]
        for r in row:
            k.append(r[0])
        return k

    except:
        print('查询失败')

    pass

#通过orderid获得订单信息，包括送餐地点，外卖人员等,适合少量查询
def get_order_from_order_id(orderid):
    try:
        for o in orderid:
            # 查询 select HALL_NAME from manager JOIN hall on MANAGER_HALL_ID=HALL_ID where MANAGER_ID="4";
            sql ='select ORDER_ID,ORDER_STATE,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,' \
                 'ADDRESS_NAME,UID,ADDRESS_PHONE,DELIVERY_NAME,DELIVERY_PHONE from `order`join address join delivery on DELIVERY_ID=ORDER_DELIVERY_ID ' \
                 'and ORDER_ADDRESS_ID=ADDRESS_ID where ORDER_ID=\'%s\';'%o
            # sql='select ORDER_ID,ORDER_STATE,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,ADDRESS_NAME,UID,ADDRESS_PHONE,DELIVERY_NAME,DELIVERY_PHONE from `order`join address join delivery on DELIVERY_ID=ORDER_DELIVERY_ID and ORDER_ADDRESS_ID=ADDRESS_ID where ORDER_ID=\'222\';'
            row = session.execute(sql)
            k=[]
            for r in row:
                k.append(r)
        return k

    except:
        print('查询失败')

    pass

#通过managerid 获得订单信息
def get_order_from_manager_id(managerid):
    try:
        sql='select DISTINCT e.ORDER_ID,ORDER_STATE,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,ADDRESS_NAME,UID,ADDRESS_PHONE,DELIVERY_NAME,DELIVERY_PHONE ' \
            'from (select DISTINCT ORDER_ID,ORDER_STATE,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,ADDRESS_NAME,UID,ADDRESS_PHONE,DELIVERY_NAME,DELIVERY_PHONE from `' \
            'order`join address join delivery on DELIVERY_ID=ORDER_DELIVERY_ID and ORDER_ADDRESS_ID=ADDRESS_ID order by ORDER_ID)e join (select DISTINCT ORDER_ID from ' \
            '(select HALL_NAME from manager JOIN hall on MANAGER_HALL_ID=HALL_ID where MANAGER_ID=\'%s\')c join (select HALL_NAME,ORDER_ID from (select CHEF_ID,HALL_NAME from ' \
            'chef join hall on chef.HALL_ID=hall.HALL_ID )a join (select  DISTINCT ORDER_ID,CHEF_ID from order_to_remain join chef_to_dish ' \
            'on order_to_remain.CHEF_TO_DISH_ID=chef_to_dish.ID ORDER by order_to_remain.ORDER_ID)b on a.CHEF_ID=b.CHEF_ID ORDER BY ORDER_ID)d on c.HALL_NAME=d.HALL_NAME )f ' \
            'on e.ORDER_ID=f.ORDER_ID order by e.ORDER_ID;'%managerid
        row = session.execute(sql)
        k=[]
        for r in row:
            print(r)
            k.append(r)
        return k

    except:
        print('查询失败')
        return [-999]
    pass

#通过managerid 获得对应食堂的菜品评论信息
def get_dish_comment_from_manager_id(managerid):
    try:
        sql='select DISTINCT  MANAGER_ID, HALL_NAME,CHEF_NAME,DISH_NAME,COMMENT_RANK,COMMENT_DETAILS ' \
            'from (select * from dish_comment join dish join chef on dish.DISH_ID=dish_comment.COMMENT_DISHID ORDER BY' \
            ' chef.HALL_ID,DISH_NAME)a join  (select HALL_ID, HALL_NAME,MANAGER_ID from manager JOIN hall' \
            ' on MANAGER_HALL_ID=HALL_ID where MANAGER_ID=\'%s\')b on a.HALL_ID=b.HALL_ID;'%managerid
        row = session.execute(sql)
        k=[]
        for r in row:
            k.append(r)
        return k

    except:
        print('查询失败')
        return [-999]
    pass

#通过managerid 获得对应食堂的总平均评论rank
def get_dish_comment_rank_from_manager_id(managerid):
    try:
        sql='select DISTINCT  MANAGER_ID, HALL_NAME,avg(COMMENT_RANK) ' \
            'from (select * from dish_comment join dish join chef on dish.DISH_ID=dish_comment.COMMENT_DISHID ORDER BY' \
            ' chef.HALL_ID,DISH_NAME)a join  (select HALL_ID, HALL_NAME,MANAGER_ID from manager JOIN hall' \
            ' on MANAGER_HALL_ID=HALL_ID where MANAGER_ID=\'%s\')b on a.HALL_ID=b.HALL_ID;'%managerid
        row = session.execute(sql)
        k=[]
        for r in row:
            k.append(r)
        return k

    except:
        print('查询失败')
        return [-999]
    pass

#通过managerid获得管理的厨师的平均rank
def get_chef_rank_from_manager_id(managerid):
    try:
        k = []
        sql = 'select MANAGER_HALL_ID from manager  where MANAGER_ID=\'%s\';' % managerid
        hall_all_id= session.execute(sql)
        for hall in hall_all_id:
            hall_id=hall[0]
            a=get_chef_rank_from_hall_id(hall_id)
            for aa in a :
                k.append(aa)

        return k

    except:
        print('查询失败')
        return [-999]
    pass

#通过hallid获得管理的厨师的平均rank
def get_chef_rank_from_hall_id(hallid):
    try:
        sql = 'select   HALL_NAME,CHEF_NAME,avg(COMMENT_RANK) from ( select  hall.HALL_NAME as HALL_NAME,CHEF_NAME,COMMENT_RANK from dish_comment ' \
              'join dish join chef join hall  on  dish.DISH_ID=dish_comment.COMMENT_DISHID and COMMENT_CHEFID=CHEF_ID ' \
              'and hall.HALL_ID=chef.HALL_ID  AND chef.HALL_ID=\'%s\')a group by CHEF_NAME;' % hallid
        row = session.execute(sql)
        k = []
        for r in row:
            k.append(r)
        return k

    except:
        print('查询失败')
        return [-999]
    pass

#通过managerid获得管理的厨师的平均rank
def get_dish_rank_from_manager_id(managerid):
    try:
        k = []
        sql = 'select MANAGER_HALL_ID from manager  where MANAGER_ID=\'%s\';' % managerid
        hall_all_id= session.execute(sql)
        for hall in hall_all_id:
            hall_id=hall[0]
            a=get_dish_rank_from_hall_id(hall_id)
            for aa in a :
                k.append(aa)

        return k

    except:
        print('查询失败')
        return [-999]
    pass

#通过hallid获得管理的厨师的平均rank
def get_dish_rank_from_hall_id(hallid):
    try:
        sql = 'select   HALL_NAME,DISH_NAME,avg(COMMENT_RANK) from (select  hall.HALL_NAME as HALL_NAME,DISH_NAME,COMMENT_RANK from ' \
              'dish_comment join dish join chef join hall  on ' \
              'dish.DISH_ID=dish_comment.COMMENT_DISHID and COMMENT_CHEFID=CHEF_ID and hall.HALL_ID=chef.HALL_ID  AND chef.HALL_ID=\'%s\' )a group by DISH_NAME;' % hallid
        row = session.execute(sql)
        k = []
        for r in row:
            k.append(r)
        return k

    except:
        print('查询失败')
        return [-999]
    pass

#通过managerid获得剩余量
def get_remain_from_manager_id(managerid):
    try:
        sql = 'select DISTINCT  HALL_NAME,CHEF_NAME,DISH_NAME,REMAIN,dish.DISH_PRICE from (select HALL_NAME,CHEF_NAME,REMAIN,DISH_ID ' \
              'from (select HALL_NAME,CHEF_NAME,CHEF_ID from (select HALL_ID,HALL_NAME from manager JOIN hall on MANAGER_HALL_ID=HALL_ID where MANAGER_ID=\'%s\')a ' \
              'join (select CHEF_ID,CHEF_NAME,chef.HALL_ID AS HALL_ID from chef join hall on chef.HALL_ID=hall.HALL_ID )b on a.HALL_ID=b.HALL_ID )c' \
              ' join chef_to_dish on c.CHEF_ID=chef_to_dish.CHEF_ID)d join dish on dish.DISH_ID=d.DISH_ID;' % managerid
        row = session.execute(sql)
        k = []
        for r in row:
            k.append(r)
        return k

    except:
        print('查询失败')
        return [-999]
    pass

#通过id和remain设置菜品剩余量
def set_chef_to_dish_by_remain_id(remain,id):
    sql='update chef_to_dish  set REMAIN= \'%s\' where ID = \'%s\';'%(remain,id)
    try:
        # 执行sql语句
        session.execute(sql)
        # 提交到数据库执行
        session.commit()
    except:
        # Rollback in case there is any error
        session.rollback()
        print('修改失败')
    pass

#通过remain设置菜品剩余量
def set_chef_to_dish_by_remain(remain):

    sql='update chef_to_dish set REMAIN=\'%s\' WHERE ID>=1;'%remain
    try:
        session.execute(sql)
        # 提交到数据库执行
        session.commit()

    except:
        session.rollback()
        print('修改失败')
    pass

#通过id减少菜品数量1
def set_chef_to_dish_by_id_reduce(id,sub):

    sql0='select REMAIN from chef_to_dish where ID=\'%s\';'%id
    row = session.execute(sql0)
    for r in row:
        number =r[0]
    number=number-sub
    if number<0 :
        print('减去后菜品数量小于0')
        return [0]
    set_chef_to_dish_by_remain_id(number, id)
    pass

#通过id增加菜品数量1
def set_chef_to_dish_by_id_increase(id,add):

    sql0='select REMAIN from chef_to_dish where ID=\'%s\';'%id
    row = session.execute(sql0)
    for r in row:
        number =r[0]
    number=number+add
    set_chef_to_dish_by_remain_id(number, id)
    pass

#======================食堂负责人部分结束=================================================
#==========================厨师部分开始================================
#通过chefid 获得厨师的评论
def get_dish_comment_from_chef_id(chefid):
    try:
        sql='select CHEF_NAME,DISH_NAME,COMMENT_DETAILS,COMMENT_RANK from (select * from dish_comment join chef join dish on ' \
            'COMMENT_CHEFID=CHEF_ID and COMMENT_DISHID=DISH_ID  where COMMENT_CHEFID=\'%s\' order by DISH_NAME)a ' \
            'join (select DISH_ID from chef_to_dish where CHEF_ID=\'%s\')b on a.DISH_ID=b.DISH_ID;'%(chefid,chefid)
        row = session.execute(sql)
        k=[]
        for r in row:
            k.append(r)
        return k

    except:
        print('查询失败')
        return [-999]
    pass

#通过chefid 获得厨师的评分  \'%s\'
def get_chef_rank_from_chef_id(chefid):
    try:
        sql='select CHEF_NAME,avg(COMMENT_RANK) from(select * from dish_comment join chef join dish on ' \
            'COMMENT_CHEFID=CHEF_ID and COMMENT_DISHID=DISH_ID  where COMMENT_CHEFID=\'%s\' order by DISH_NAME)a ' \
            'join (select DISH_ID from chef_to_dish where CHEF_ID=\'%s\')b on a.DISH_ID=b.DISH_ID ;'%(chefid,chefid)
        row = session.execute(sql)
        k=[]
        for r in row:
            k.append(r)
        return k

    except:
        print('查询失败')
        return [-999]
    pass

#通过chefid 获得厨师的菜的评分  \'%s\'
def get_dish_rank_from_chef_id(chefid):
    try:
        sql = 'select CHEF_NAME,avg(COMMENT_RANK) from(select * from dish_comment join chef join dish on ' \
              'COMMENT_CHEFID=CHEF_ID and COMMENT_DISHID=DISH_ID  where COMMENT_CHEFID=\'%s\' order by DISH_NAME)a ' \
              'join (select DISH_ID from chef_to_dish where CHEF_ID=\'%s\')b on a.DISH_ID=b.DISH_ID group by DISH_NAME ;' % (
              chefid, chefid)
        row = session.execute(sql)
        k=[]
        for r in row:
            k.append(r)
        return k

    except:
        print('查询失败')
        return [-999]
    pass

#通过CHEFid设置厨师所属食堂
def set_chef_hall_by_chef_id(chefid,hallid):

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
        reutrn [-999]

    try:
        sql = 'update chef set HALL_ID=\'%s\' WHERE CHEF_ID=\'%s\';' % (hallid, chefid)
        session.execute(sql)
        session.commit()
    except:
        session.rollback()
        print('查询失败')
        return [-999]
    return [1]
    pass

#通过DISHID 设置菜品价格
def set_dish_price_by_dish_id(dishid,price):
    try:
        sql = 'update dish set DISH_PRICE=\'%s\' WHERE DISH_ID=\'%s\';' % (price, dishid)
        session.execute(sql)
        session.commit()
    except:
        session.rollback()
        print('查询失败')
        return [-999]
    return [1]
    pass

#通过DISHID 设置菜品描述
def set_dish_description_by_dish_id(dishid,description):
    try:
        sql = 'update dish set DISH_DESCRIPTION=\'%s\' WHERE DISH_ID=\'%s\';' % (description, dishid)
        session.execute(sql)
        session.commit()
    except:
        session.rollback()
        print('查询失败')
        return [-999]
    return [1]
    pass

#通过chefid ,dishid 为厨师添加菜品
def add_dish_from_chef_id(chefid,dishid):
    sql = 'insert into chef_to_dish  (CHEF_ID,DISH_ID,REMAIN,`RANK`)VALUES(\'%s\',\'%s\',0,0);' % (chefid, dishid)
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
    pass

#通过chefid ,dishid 为厨师删除菜品
def delete_dish_from_chef_id(chefid,dishid):
    sql = 'delete from chef_to_dish where CHEF_ID=\'%s\' AND DISH_ID=\'%s\';' % (chefid, dishid)
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
    pass

#===========================厨师部分完毕=============================

if __name__ == '__main__':
    HOST = '129.204.93.30'
    PORT = '3306'
    DATABASE = 'cs307'
    USERNAME = 'user_cs307'
    PASSWORD = '!2345678'
    DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset-utf8".format(username=USERNAME, password=PASSWORD,host=HOST,port=PORT,db=DATABASE)
    # 创建一个引擎
    engine = create_engine(DB_URI)
    Session_class = sessionmaker(bind=engine)  # 创建用于数据库session的类
    session = Session_class()
    result=delete_dish_from_chef_id(6,50)
    for i in result:
        print(i)
    print('length is ',len(result))
    # set_chef_to_dish_by_remain(7)
    # set_chef_to_dish_by_id_reduce(2,3)
