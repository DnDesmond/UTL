import pickle
from RP import resource_path as r

full_run = {"hide0_0_1":True,
            "hide0_0_2":True,
            "wall0_1_1":True,
            "foe2_0_1":True,
            "foe3_0_1":False,
            "foe3_0_2":True}

with open(r("Relevents.pickle"), 'wb') as file:
    pickle.dump(full_run, file)