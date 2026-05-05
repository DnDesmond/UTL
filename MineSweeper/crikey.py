import json
import os
os.chdir("C:/Users/Computer Science 8/UTL/MineSweeper")
deus = {}

counts = 5
tiers = 1
diagonals = False
counter = 0
tritia = {"counts":counts,"tiers":tiers,"diagonals":diagonals,"counter":counter, "hidden":[]}
deus["-1"] = tritia.copy()

counts = 3
tiers = 3
diagonals = True
counter = 1
hidden = []
tritia = {"counts":counts,"tiers":tiers,"diagonals":diagonals,"counter":counter, "hidden":hidden}
deus[0] = tritia.copy()

counts = 5
tiers = 2
diagonals = False
counter = 0
hidden = [(1,2)]
tritia = {"counts":counts,"tiers":tiers,"diagonals":diagonals,"counter":counter, "hidden":hidden}
deus[1] = tritia.copy()

counts = 3
tiers = 2
diagonals = True
counter = 3
hidden = []
tritia = {"counts":counts,"tiers":tiers,"diagonals":diagonals,"counter":counter, "hidden":hidden}
deus[2] = tritia.copy()

counts = 5
tiers = 3
diagonals = True
counter = 0
hidden = [[0,0],[0,1],[0,3],[0,4],[1,0],[1,4]]
tritia = {"counts":counts,"tiers":tiers,"diagonals":diagonals,"counter":counter,"hidden":hidden}
deus[3] = tritia.copy()

with open("loaf.json", "w") as file:
    txt = json.dumps(deus)
    file.write(f"{txt}\n")