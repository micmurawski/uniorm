from .conditions import Condition


class FieldMeta(type):
    pass


class Field(Condition, metaclass=FieldMeta):
    ty = object

    def __init__(self, *, name=None, required=True) -> None:
        self.name = name
        self.required = required

    # def __get__(self, instance, cls):
    #    if instance is None:
    #        return None
    #    return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not self.required and value is None:
            pass
        elif not isinstance(value, self.ty):
            raise TypeError(f"Expected {self.ty}")
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class StringField(Field):
    ty = str


class IntField(Field):
    ty = int


class ObjectField(Field):
    ty = dict


TYPE_MAP = {
    'string': StringField,
    'integer': IntField,
    'object': ObjectField,
}
