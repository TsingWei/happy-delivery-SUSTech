from flask_login import UserMixin
from delivery_all.dao.Delivery import Delivery

# class User:
#     def __init__(self, sid, name, address):
#         self.sid = sid
#         self.name = name
#         self.address = address
#         self.is_authenticated = True
#         self.is_active = False
#         self.is_anonymous = False
#
#     def get_id(self):
#         return str(self.sid).encode("utf-8").decode("utf-8")


class User(UserMixin):
    def __init__(self, dic=None):
        UserMixin.__init__(self)
        self.get_order = []
        if dic is not None:
            # print("111111111111111111111111111111")
            self.delivery_id= dic['delivery_id']
            self.delivery_name= dic['delivery_name']
            self.delivery_path = dic['delivery_path']
            self.delivery_service_year= dic['delivery_year']
            self.delivery_phone = dic['delivery_phone']
            self.delivery_rank = dic['delivery_rank']



# 用户记录表
users = [
    {'username': 'Tom', 'password': '111111'},
    {'username': 'Michael', 'password': '123456'}
]


# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(user_id):
    return Delivery.get_delivery_info(int(user_id))
    # return None

