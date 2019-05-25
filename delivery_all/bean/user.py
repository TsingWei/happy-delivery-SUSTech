from flask_login import UserMixin
from dao.User import User as DaoUser

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
            self.delivery_id= dic['delivery_id']
            self.delivery_name= dic['delivery_name']
            self.delivery_path = dic['delivery_path']
            self.delivery_service_year= dic['delivery_service_year']
            self.delivery_phone = dic['delivery_phone']
            self.delivery_rank = dic['delivery_rank']



# 用户记录表
users = [
    {'username': 'Tom', 'password': '111111'},
    {'username': 'Michael', 'password': '123456'}
]


# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(user_id):
    return DaoUser.find_user(user_id=int(user_id))

