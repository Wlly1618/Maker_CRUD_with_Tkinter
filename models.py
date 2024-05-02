from base_model import *


@model_methods
class Product(BaseEntity):
    def __init__(self, _id=None, name="", price=0.0, stock=100):
        self.id = _id
        self.name = name
        self.price = price
        self.stock = stock
        self.modifiable = ["name", "price", "stock"]

    def set_id(self, _id):
        self.id = _id


@model_methods
class Client(BaseEntity):
    def __init__(self, _id=None, name=""):
        self.id = _id
        self.name = name
        self.modifiable = ["name"]

    def set_id(self, _id):
        self.id = _id
