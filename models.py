class BaseEntity:
    def get_keys_str(self):
        """
        To get string with keys to class
        :return: array to contains the keys
        """
        return ', '.join(map(str, vars(self).keys()))

    @property
    def get_keys_without_id_str(self):
        """
        To get string with keys to class without the *_id*
        :return:
        """
        keys = vars(self).keys()
        keys_without_id = [key for key in keys if key != '_id']
        return ', '.join(map(str, keys_without_id))

    def get_values_str(self):
        """
        To get string with the
        :return: array to contains the values
        """
        return ', '.join(map(str, vars(self).values()))

    def get_values_array(self):
        """
        To get values to class_
        :return: class_ values
        """
        return list(vars(self).values())


class Product(BaseEntity):
    def __init__(self, _id=0, name="", price=0.0, stock=100):
        self._id = _id
        self.name = name
        self.price = price
        self.stock = stock

    @staticmethod
    def columns_to_upd():
        return "name, price, stock"


class Client(BaseEntity):
    def __init__(self, _id=0, name=""):
        self._id = _id
        self.name = name

    @staticmethod
    def columns_to_upd():
        return "name"


class Shop(BaseEntity):
    def __init__(self, _id=0, id_client="", date_time=""):
        self._id = _id
        self.id_client = id_client
        self.date = date_time

    @staticmethod
    def columns_to_upd():
        return ""


class Detail(BaseEntity):
    def __init__(self, _id=0, id_shop="", id_product="", amount=""):
        self._id = _id
        self.id_shop = id_shop
        self.id_product = id_product
        self.amount = amount

    @staticmethod
    def columns_to_upd():
        return "id_product, amount"
