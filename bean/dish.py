class Dish:
    def __init__(self, _id, _name, _image_url, _price):
        self.id = _id
        self.name = _name
        self.image_url = _image_url
        self.price = _price


dishes = [
    Dish(0, "黄焖鸡", None, 20.0),
    Dish(1, "红烧茄子", None, 3.0),
    Dish(2, "番茄炒蛋", None, 3.0),
    Dish(3, "猪扒", None, 10.0)
    # Dish(3, "猪扒", None, 10.0),
    # Dish(0, "黄焖鸡", None, 20.0),
    # Dish(1, "红烧茄子", None, 3.0),
    # Dish(2, "番茄炒蛋", None, 3.0),
    # Dish(3, "猪扒", None, 10.0),
    # Dish(3, "猪扒", None, 10.0),
    # Dish(0, "黄焖鸡", None, 20.0),
    # Dish(1, "红烧茄子", None, 3.0),
    # Dish(2, "番茄炒蛋", None, 3.0),
    # Dish(3, "猪扒", None, 10.0),
    # Dish(3, "猪扒", None, 10.0)
]
