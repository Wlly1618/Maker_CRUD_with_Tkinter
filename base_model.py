from crud import CRUD

crud_instance = CRUD("db_test_2")
crud_instance.begin_transaction()


class BaseEntity:
    def get_keys_array(self):
        return list(vars(self).keys())[:-1]

    def get_values_array(self):
        return list(vars(self).values())[:-1]

    def get_keys_str(self):
        return ', '.join(self.get_keys_array())


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
        def get_by_id(cls, _id):
            column = cls.__name__.lower()
            data = crud_instance.read_with_id(_id, column)
            if data:
                return cls(*data)
            else:
                return None

        @classmethod
        def get_all(cls):
            column = cls.__name__.lower()
            data = crud_instance.read(column)

            if data:
                return [cls(*item) for item in data]
            else:
                return None

        @classmethod
        def update(cls, **kwargs):
            instance = cls(**kwargs)
            column = cls.__name__.lower()
            attr = instance.modifiable
            if attr:
                data = [getattr(instance, item) for item in attr]
                response = crud_instance.update(column, attr, instance.id, data)

                if response:
                    return instance
                else:
                    return None

        @classmethod
        def delete(cls, _id):
            column = cls.__name__.lower()
            response = crud_instance.delete(column, _id)
            if response:
                return _id
            else:
                return None

    DecoratedClass.__name__ = cls.__name__
    return DecoratedClass
