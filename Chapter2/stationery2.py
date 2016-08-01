"""
组合模式
用一个类来表示组合体与非组合体
"""

import itertools
import sys


def main():
    pencil = Item.create("Pencil", 0.40)
    ruler = Item.create("Ruler", 1.60)
    eraser = make_item("Eraser", 0.20)
    pencilSet = Item.compose("Pencil Set", pencil, ruler, eraser)
    box = Item.create("Box", 1.00)
    boxedPencilSet = make_composite("Boxed Pencil Set", box, pencilSet)
    boxedPencilSet.add(pencil)
    for item in (pencil, ruler, eraser, pencilSet, boxedPencilSet):
        item.print()
    assert not pencil.composite
    pencil.add(eraser, box)
    assert pencil.composite
    pencil.print()
    pencil.remove(eraser)
    assert pencil.composite
    pencil.remove(box)
    assert not pencil.composite
    pencil.print()


class Item:
    def __init__(self, name, *items, price=0.00):
        self.name = name
        self.price = price
        self.children = []
        if items:
            self.add(*items)

    @classmethod
    def create(cls, name, price):
        return cls(name, price=price)

    @classmethod
    def compose(cls, name, *items):
        return cls(name, *items)

    @property
    def composite(self):
        return bool(self.children)

    def add(self, first, *items):
        self.children.extend(itertools.chain((first,), items))

    def remove(self, item):
        self.children.remove(item)

    def __iter__(self):
        return iter(self.children)

    @property
    def price(self):
        return (sum(item.price for item in self) if self.children else self.__price)

    @price.setter
    def price(self, price):
        self.__price = price

    def print(self, indent="", file=sys.stdout):
        print("{}${:.2f} {}".format(indent, self.price, self.name), file=file)
        for child in self:
            child.print(indent + "    ")


def make_item(name, price):
    return Item(name, price=price)


def make_composite(name, *items):
    return Item(name, *items)


if __name__ == "__main__":
    main()