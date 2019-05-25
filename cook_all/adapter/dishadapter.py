from cook_all.bean.dish import Dish
from cook_all.dao.Chef import Chef
from cook_all.dao.Dish import Dish as DaoDish
from cook_all.dao.ChefToDish import ChefToDish


def getalldish(chefid):
    dishes = []
    for dish in Chef.get_dish_rank_from_chef_id(int(chefid)):
        dish_id = dish['dish_id']
        dishd = DaoDish.find_dish(dish_id=dish_id)[0]
        remain = ChefToDish.find_connect(dish_id=dish_id, chef_id=chefid)[0]['remain']
        dish_bean = Dish(dishd['dish_id'],
                         dishd['dish_name'],
                         dishd['dish_description'],
                         dishd['dish_image_path'],
                         dishd['dish_price'],
                         dish['rank'],
                         remain)
        dishes.append(dish_bean)
    return dishes
