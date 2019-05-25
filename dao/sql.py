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

#   address
#   insert IGNORE into address  (UID,ADDRESS_NAME,ADDRESS_PHONE)VALUES(1,"荔园9栋",13789086438);
#   chef
#   insert into chef  (CHEF_SERVICE_YEAR,CHEF_NAME,CHEF_RANK,HALL_ID)VALUES(6,"厨凌柏",5,1);
#   chef to dish
#   insert IGNORE into chef_to_dish  (CHEF_ID,DISH_ID,REMAIN,`RANK`)VALUES(1,50,52,5);
#   delivery
#   insert IGNORE into delivery  (DELIVERY_NAME,DELIVERY_PHONE,DELIVERY_PATH,DELIVERY_RANK,DELIVERY_SERVICE_YEAR)VALUES("外卖梦琪","13284832937","delivery_path0",1,3);
#   delivery comment
#   insert IGNORE into delivery_comment  (COMMENT_USERID,COMMENT_DELIVERYID,COMMENT_DETAILS,COMMENT_RANK)VALUES(0,142,"delivery_path1",0);
#   dish comment
#   insert IGNORE into dish_comment  (COMMENT_USERID,COMMENT_CHEFID,COMMENT_DISHID,COMMENT_DETAILS,COMMENT_RANK)VALUES(1,1,79,"菜品评论1",5);
#   manager
#   insert into manager (MANAGER_NAME,MANAGER_PHONE,MANAGER_HALL_ID)VALUES("春柏",13786597371,1);
#   order
#   insert IGNORE into `order` (ORDER_ADDRESS_ID,ORDER_DELIVERY_ID,ORDER_PRICE,ORDER_START_TIME,ORDER_END_TIME,ORDER_REMARK,ORDER_STATE)VALUES(1,104,-1.0,"6:4",NULL,"order_remark1","AC");
#   order to remain
#   insert IGNORE into order_to_remain  (ORDER_ID,CHEF_TO_DISH_ID)VALUES(1,945);
#   user
#   insert  IGNORE into user  (USER_NAME,USER_GENDER,USER_SID,USER_PHONE,USER_TYPE)VALUES("用户寄云","F","11427152","13500793654","STUDENT");

#查询食堂所属的所有订单的id
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
    result=get_remain_from_manager_id(4)
    for i in result:
        print(i)
    print('length is ',len(result))
    # set_chef_to_dish_by_remain(7)
    # set_chef_to_dish_by_id_reduce(2,3)
