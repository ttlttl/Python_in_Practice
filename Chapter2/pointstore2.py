"""
享元模式
"""
import os
import shelve
import tempfile
import atexit
import sys
import Qtrac
import time


class Point:
    __slots__ = ()
    # 所有实例共享__dbm静态变量
    __dbm = shelve.open(os.path.join(tempfile.gettempdir(), "point.db"))

    def __init__(self, x=0, y=0, z=0, color=None):
        self.x = x
        self.y = y
        self.z = z
        self.color = color

    def __key(self, name):
        return "{:X}:{}".format(id(self), name)

    def __getattr__(self, name):
        return Point.__dbm[self.__key(name)]

    def __setattr__(self, name, value):
        Point.__dbm[self.__key(name)] = value

    def __repr__(self):
        return "Point({0.x!r}, {0.y!r}, {0.z!r}, {0.color!r})".format(self)

    atexit.register(__dbm.close)


def main():
    regression = False
    size = int(1e3)
    if len(sys.argv) > 1 and sys.argv[1] == "-P":
        regression = True
        size = 20
    Qtrac.remove_if_exists(os.path.join(tempfile.gettempdir(), "point.db"))
    start = time.clock()
    points = []
    for i in range(size):
        points.append(Point(i, i ** 2, i // 2))
    end = time.clock() - start
    assert points[size - 1].x == size - 1
    print(len(points))
    if not regression: # wait until we can see how much memory is used
        print("took {} secs to create {:,} points".format(end, size))
        input("press Enter to finish")


if __name__ == "__main__":
    main()