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

def dotxline(point, cap, cap_2, tol=2):
    full = length(cap, cap_2)
    half = length(cap, point)
    halved = length(cap_2, point)
    if half + halved >= full-tol and half + halved <= full+tol:
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

def simuls(static_1:dict, static_2:dict):
    a1,b1,c1 = static_1.values()
    a2,b2,c2 = static_2.values()
    if a1 != a2:
        t = a1
        a1 *= a2
        b1 *= a2
        c1 *= a2
        a2 *= t
        b2 *= t
        c2 *= t
    if a1 > 0 and a2 > 0:
        a1 *= -1
        b1 *= -1
        c1 *= -1
        
    x = b1+b2
    if x != 0:
        valx = (-c1-c2)/x
    else:
        valx = 0
    valy = (-c1-(valx*b1))/a1
    
    # print(valx)
    # print(valy)

    col = (valx, valy)

    return col