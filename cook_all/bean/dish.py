class Dish:
    def __init__(self, _id, _name, _description, _image_url, _price, _rank, _remain):
        self.id = _id
        self.name = _name
        self.description = _description
        self.image_url = _image_url
        self.price = _price
        self.rank = round(_rank, 2)
        self.remain = _remain
