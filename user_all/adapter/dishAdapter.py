from user_all.bean.dish import Dish
from user_all.dao.Hall import Hall
from user_all.dao.Manager import Manager
def getAlldish(hallID):
    dishes = []
    remains={}
    # print(hallID)
    remainss = Manager.get_remain_from_manager_id_group(hallID)
    for item in remainss:
        remains[item['dish_id']] = item['remain']
    for dish in Hall.get_dishes(int(hallID)):
        dishBean = Dish(dish['dish_id'],
                        dish['dish_name'],
                        dish['dish_image_path'],
                        dish['dish_price'],
                        dish['hall_id'],
                        dish['dish_description'],
                        remains[dish['dish_id']])
        dishes.append(dishBean)
    return dishes
