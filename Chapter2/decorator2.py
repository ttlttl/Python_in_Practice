"""
类装饰器
"""
from .decorator1 import is_in_range, is_non_empty_str

class Ensure:
    def __init__(self, validate, doc=None):
        self.validate = validate
        self.doc = doc


def do_ensure(Class):
    def make_property(name, attribute):
        privateName = "__" + name
        def getter(self):
            return getattr(self, privateName)
        def setter(self,value):
            attribute.validate(name, value)
            setattr(self, privateName, value)
        return property(getter, setter, doc=attribute.doc)
    for name, attribute in Class.__dict__.items():
        if isinstance(attribute, Ensure):
            setattr(Class, name, make_property(name, attribute))
    return Class


@do_ensure
class Book:
    title = Ensure(is_non_empty_str)
    isbn = Ensure(is_non_empty_str)
    price = Ensure(is_in_range(1, 10000))
    quantity = Ensure(is_in_range(1, 1000000))

    def __init__(self, title, isbn, price, quantity):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.quantity = quantity

    @property
    def value(self):
        return self.price * self.quantity

