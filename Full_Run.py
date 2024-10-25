import pickle
from RP import resource_path as r

def premiere(save=1):
    full_run = {}
    
    full_run |= faux(2,0,1)
    full_run |= faux(3,0,2) 
    full_run |= pelt(0,0,3)
    full_run |= choice(0,1,1)

    with open(r(f"Relevents{save}.pickle"), 'wb') as file:
        pickle.dump(full_run, file)

def swiftininatator(flavour, level, count, full_run=list):
    for num in range(1, count+1):
        full_run[(f"{flavour}{level}_{num}")] = True
    return full_run

def faux(x, y, count):
    sum = {}
    for num in range(1, count+1):
        sum[(f"foe{x}_{y}_{num}")] = True
    return sum

def pelt(x, y, count):
    sum = {}
    for num in range(1, count+1):
        sum[(f"hide{x}_{y}_{num}")] = True
    return sum

def choice(x, y, count):
    sum = {}
    for num in range(1, count+1):
        sum[(f"wall{x}_{y}_{count}")] = True
    return sum

if __name__ == "__main__":
    premiere(1)