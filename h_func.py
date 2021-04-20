import math

def distance(rect1, rect2):
    x1, y1 = rect1.center
    x1b, y1b = rect1.bottomright
    x2, y2 = rect2.topleft
    x2b, y2b = rect2.bottomright
    left = x2b < x1
    right = x1b < x2
    top = y2b < y1
    bottom = y1b < y2
    if bottom and left:
        return math.hypot(x2b-x1, y2-y1b)
    elif left and top:
        return math.hypot(x2b-x1, y2b-y1)
    elif top and right:
        return math.hypot(x2-x1b, y2b-y1)
    elif right and bottom:
        return math.hypot(x2-x1b, y2-y1b)
    elif left:
        return x1 - x2b
    elif right:
        return x2 - x1b
    elif top:
        return y1 - y2b
    elif bottom:
        return y2 - y1b
    else:  # rectangles intersect
        return 0