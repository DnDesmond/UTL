def picks(point, width, range):
    greens = width//3
    blues = (width//3)*2
    reds1 = 0
    reds2 = width
    x = point[0]
    green = calcs(x, greens, range)
    blue = calcs(x, blues, range)
    if x < width//2:
        red = calcs(x, reds1, range)
    else:
        red = calcs(x, reds2, range)
    return (red,green,blue)

def calcs(x, bar, range=255):
    if x <= bar:
        res = x-(bar-range)
    elif x >= bar:
        res = (bar+range)-x
    mod = res/abs(range+1)
    res = mod*255
    if res > range:
        res = range
    if res < 0:
        res = 1
    return res