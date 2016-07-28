"""
原型模式
"""

import sys
import copy


class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


def make_object(cls, *args, **kwargs):
    return cls(*args, **kwargs)


p1 = Point(1, 2)

p2 = eval("{}({}, {})".format("Point", 2, 3))

p3 = getattr(sys.modules[__name__], "Point")(3, 4)

p4 = globals()["Point"](4, 5)

p5 = make_object(Point, 5, 6)

# Prototype
p6 = copy.deepcopy(p5)
p6.x = 6
p6.y = 7

p7 = p1.__class__(7, 8)