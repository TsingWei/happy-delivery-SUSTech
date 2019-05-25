from flask_login import UserMixin
from dao.Chef import Chef

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
        self.curr_order = {}
        if dic is not None:
            self.user_id = dic['user_id']
            self.user_name = dic['user_name']
            self.user_gender = dic['user_gender']
            self.user_sid = dic['user_sid']
            self.user_phone = dic['user_phone']
            self.user_type = dic['user_type']



# 用户记录表
users = [
    {'username': 'Tom', 'password': '111111'},
    {'username': 'Michael', 'password': '123456'}
]


# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(user_id):
    return Chef.find_chef(chef_id=int(user_id))

