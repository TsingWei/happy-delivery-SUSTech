from cook_all.bean.dish import Dish
from cook_all.dao.Chef import Chef
from cook_all.dao.Dish import Dish as DaoDish


def getalldish(chefid):
    dishes = []
    # print(hallID)
    for dish in Chef.get_dish_comment_from_chef_id(int(chefid)):
        dish_id = dish['dish_id']
        dishd = DaoDish.find_dish(dish_id=dish_id)
        dish_bean = Dish(dishd['dish_id'],
                         dishd['dish_name'],
                         dishd['dish_description'],
                         dishd['dish_image_path'],
                         dishd['dish_price'],)
        dishes.append(dish_bean)
    return dishes
