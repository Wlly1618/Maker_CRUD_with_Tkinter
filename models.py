from crud import CRUD

crud_instance = CRUD("db_test_2")


class BaseEntity:
    def get_keys_str(self):
        return ', '.join(map(str, vars(self).keys()))

    def get_values_array(self):
        return list(vars(self).values())

    def get_keys_without_id_str(self):
        data = self.get_keys_str()
        data = data[4:]
        return data

    def get_keys_array(self):
        return vars(self).keys()


def model_methods(cls):
    class DecoratedClass(cls):
        @classmethod
        def create(cls, **kwargs):
            instance = cls(**kwargs)
            column = cls.__name__.lower()
            header = instance.get_keys_str()
            data = instance.get_values_array()
            result = crud_instance.create(column, header, data)

            if result:
                instance.set_id(result)
                return instance
            else:
                return None

        @classmethod
        def get_by_id(cls, **kwargs):
            instance = cls(**kwargs)
            column = cls.__name__.lower()
            data = crud_instance.read_with_id(instance.get_id(), column)
            if data:
                instance = cls(*data)
                return instance
            else:
                return None

        @classmethod
        def get(cls):
            instance = []
            column = cls.__name__.lower()
            data = crud_instance.read(column)

            if data:
                for item in data:
                    instance.append(cls(*item))

                return instance
            else:
                return None

    DecoratedClass.__name__ = cls.__name__
    return DecoratedClass


@model_methods
class Product(BaseEntity):
    def __init__(self, _id=None, name="", price=0.0, stock=100):
        self.id = _id
        self.name = name
        self.price = price
        self.stock = stock

    def get_id(self):
        return self.id

    def set_id(self, _id):
        self.id = _id
