import os
from primitives import GArray, GNumber

def rect_primitive(rect):
    """Construct GArray reprents the rectangle
    """
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    rect = GArray()
    rect.append(GNumber(x))
    rect.append(GNumber(y))
    rect.append(GNumber(w))
    rect.append(GNumber(h))
    return rect

def padding_10_xref(number):
    string = str(number)
    repeats = 10 - len(string)
    return "0" * repeats + string

def join_paths(*args):
    path = ""
    for comp in args:
        path = os.path.join(path, comp)
    return path
