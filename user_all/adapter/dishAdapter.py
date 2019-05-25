from user_all.bean.dish import Dish
from user_all.dao.Hall import Hall

def getAlldish(hallID):
    dishes = []
    # print(hallID)
    for dish in Hall.get_dishes(int(hallID)):
        dishBean = Dish(dish['dish_id'],
                        dish['dish_name'],
                        dish['dish_image_path'],
                        dish['dish_price'],
                        dish['hall_id'],
                        dish['dish_description'])
        dishes.append(dishBean)
    return dishes
