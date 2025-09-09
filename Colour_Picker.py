def picks(point, width, range, inverse_channels=[0,0,0,0,0,0]):
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
    if inverse_channels[0]==1:
        red = 255-red
    if inverse_channels[1]==1:
        green = 255-green
    if inverse_channels[2]==1:
        blue = 255-blue
    if inverse_channels[3]==1:
        temp = red
        red = green
        green = temp
    if inverse_channels[4]==1:
        temp = red
        red = blue
        blue = temp
    if inverse_channels[5]==1:
        temp = blue
        blue = green
        green = temp
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