from flask_login import UserMixin
from cook_all.dao.Chef import Chef

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


class Cook(UserMixin):
    def __init__(self, dic=None):
        UserMixin.__init__(self)
        self.curr_order = {}
        if dic is not None:
            self.chef_id = dic['chef_id']
            self.chef_service_year = dic['chef_service_year']
            self.chef_name = dic['chef_name']
            self.chef_rank = dic['chef_rank']
            self.hall_id = dic['hall_id']



# 用户记录表
users = [
    {'username': 'Tom', 'password': '111111'},
    {'username': 'Michael', 'password': '123456'}
]


# 通过用户名，获取用户记录，如果不存在，则返回None
def query_user(chefid):
    return Chef.find_chef(chef_id=int(chefid))

