import pickle
from RP import resource_path as r

def premiere(save=1):
    full_run = {"hide0_0_1":True,
                "hide0_0_2":True,
                "hide0_0_3":True,
                "wall0_1_1":True,
                "foe2_0_1":True,
                "foe3_0_1":True,
                "foe3_0_2":True}

    with open(r(f"Relevents{save}.pickle"), 'wb') as file:
        pickle.dump(full_run, file)

if __name__ == "__main__":
    premiere(1)