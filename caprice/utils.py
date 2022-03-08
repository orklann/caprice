from .primitives import GArray, GNumber

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
