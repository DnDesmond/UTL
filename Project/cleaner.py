import random
from math import sin, pi
import json

def cleans(falsify=False, drought=False, humid=False, shivers=False):
    with open("Recieved_data.csv", "r") as file:
        handled = [x for x in file]
        filt = ""
        for x in handled:
            filt += x
        handled = filt.strip()
        handled = handled.replace(" ", "")
        while True:
            handled = handled.replace("\n", ",", 1)
            handled = handled.replace("\n", "", 1)
            if not "\n" in handled:
                break
        iter = 0
    cleanish = handled.split(",")
    lines = []
    line = []
    iter = 0
    sinus = []
    for x in range(0,3601):
        x = x/40
        x = (x*pi)/2
        sinus.append((((sin(0.3*x)+2))*100)+random.randint(-10,11))
    for num in cleanish:
        line.append(float(num))
        if iter > 1:
            if drought:
                line[0] -= 40
            if humid:
                line[0] += 30
                line[1] += 25
            if shivers:
                line[1] -= 42
            lines.append(line)
            line = []
            iter = 0
        elif iter == 1:
            if falsify:
                line.pop()
                line.append(sinus.pop(0))
            iter += 1
        else:
            iter += 1
    filed = json.dumps(lines)
    with open("Cleaned_data.json", "w") as file:
        file.write(filed)
    return lines

if __name__ == "__main__":
    cleans()