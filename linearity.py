from math import sqrt

def eqs(point, point_2):
    x1,y1 = point
    x2,y2 = point_2
    slope = (y2-y1)/(x2-x1)
    coy = 1
    if slope%1 != 0:
        mult = 1
        while True:
            if (slope*mult)%1 == 0:
                slope = slope*mult
                y1 = y1*mult
                coy = mult
                break
            mult+=1
    slope = round(slope)
    eq = {"coy":coy, "cofx":-slope, "c":round((-y1)+(slope*x1))}
    # print(f"{coy}y +{eq['cofx']}x + {eq["c"]} = 0")
    return eq

def length(point, point_2):
    x1,y1 = point
    x2,y2 = point_2
    tot = sqrt(((x2-x1)**2)+((y2-y1)**2))
    return tot

def dotxline(point, cap, cap_2):
    full = length(cap, cap_2)
    half = length(cap, point)
    halved = length(cap_2, point)
    if half + halved >= full-2 and half + halved <= full+2:
        return True
    else:
        return False

def other(cofw, cofh, valh, c):
    multi = cofh * valh
    try:
        valw = (-(multi+c))/cofw
    except ZeroDivisionError:
        valw = (-c)/cofh
    return valw
