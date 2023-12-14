import pandas as pd
import numpy as np
import json

PATH = "data/cmu/personas/out.phi.weights"

SAVE_PATH = "data/cmu/personas/persona_verbs.json"

def get_and_save_personas_verbs(verbose = False, save = False):
    
    persona_verbs = dict()

    with open(PATH, "r") as file:
        persona_id = 0
        verbs = pd.DataFrame(file.readline().split(sep=' '))

        for line in file.readlines(): 
            persona_id += 1
            freq = [float(x) for x in line.split(sep=' ')]
            top_id = np.argsort(freq)[-20:]
            top_verbs = verbs.iloc[top_id].values.flatten().tolist()

            if verbose:
                print(persona_id, top_verbs)
            persona_verbs[persona_id] = top_verbs
    if save:
        with open(SAVE_PATH, 'w', encoding='utf-8') as f:
            json.dump(persona_verbs, f, ensure_ascii=False, indent=4)