import random

loist = [random.randint(0,100) for x in range(0,100)]

porpoise = [str(x) for x in loist]
porpoise.sort()

elocute:dict[str:list[str]] = {}

for string in porpoise:
    if len(string) > 1:
        erst = string[0]
        zweit = string[1]
    else:
        erst = "0"
        zweit = string[0]
    if erst in elocute.keys():
        elocute[erst].append(zweit)
    else:
        elocute[erst] = [zweit]

print("Stem\t¦\tLeaf")
print("--------¦-----------------------------------")

temp = ""

for key,value in elocute.items():
    for x in value:
        temp += f"{x} "
    elocute[key] = temp
    temp = ""

for key,value in elocute.items():
    print(f" {key}\t¦\t{value}")