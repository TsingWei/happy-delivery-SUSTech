from bean.dish import Dish
from dao.Hall import Hall

def getalldish(hallid):
    dishes = []
    # print(hallID)
    for dish in Hall.get_dishes(int(hallid)):
        dish_bean = Dish(dish['dish_id'],
                        dish['dish_name'],
                        dish['dish_image_path'],
                        dish['dish_price'],
                        dish['hall_id'],
                        dish['dish_description'])
        dishes.append(dish_bean)
    return dishes
