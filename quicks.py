import random

nums = [random.randint(0,2000) for x in range(0,10000)]

def swap(loist, a, b):
    t = loist[a]
    loist[a] = loist[b]
    loist[b] = t
    return loist

def ordered(l):
    for num in range(len(l[:-1])):
        if l[num] > l[num+1]:
            return False
    return True

def is_fed(l):
    piv = l[-1]
    for num in l:
        if num > piv:
            return False
    return True

def swapify(l, piv, pivind):
    point1 = None
    point2 = None
    ind = 0
    for num in l:
        if num > piv and point1 == None:
            point1 = ind
        point2 = pivind-1
        if point1 != None:
            basel = l.copy()
            l = swap(l, point1, point2)
            l = swap(l, point2, pivind)
            break
        ind += 1
    return l

def quicks(l):
    if is_fed(l):
        l = swap(l, -1, -2)
    piv = l[-1]
    pivind = -1
    werk = False
    while werk == False:
        l = swapify(l, piv, pivind)
        pivind -= 1
        werk = True
        for num in l[:pivind]:
            if num > l[pivind]:
                werk = False
    if not ordered(l):
        if len(l[:pivind]) > 1:
            l[:pivind] = quicks(l[:pivind])
        if len(l[pivind:]) > 1:
            l[pivind:] = quicks(l[pivind:])
    return l

print(nums)
nums = quicks(nums)
print(nums)
for num in range(0,2001):
    if num not in nums:
        # print(num)
        import quicks