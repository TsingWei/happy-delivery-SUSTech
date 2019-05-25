from flask_login import UserMixin, login_manager
from dao.User import User

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
    def __init__(self):
        UserMixin.__init__(self)
        self.curr_order = {
            '红烧茄子': 1,
            '馒头': 1
        }



# 用户记录表
users = [
    {'username': 'Tom', 'password': '111111'},
    {'username': 'Michael', 'password': '123456'}
]


# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(user_id):
    return User.find_user(user_id=user_id)

