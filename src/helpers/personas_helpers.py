import pandas as pd
import numpy as np
import json

PATH = "data/cmu/personas/out.phi.weights"

N_TOP_TOPICS = 2
N_TOP_WORDS = 5

def extract_top_words(coefficients):
    """
    Extract the top words for each persona from the coefficients of the LDA model
    :param coefficients: the coefficients of the LDA model
    :return: a dict of the top words for each persona
    """

    f = open("data/cmu/personas/topic_words.json")
    topic_words = json.load(f) # topic_words is a dict

    persona_agent_words = dict()

    for i, topic_vectors in enumerate(coefficients):
        # For persona i
        sorted_coeff = np.argsort(topic_vectors)
        selected_topics = sorted_coeff[-N_TOP_TOPICS:]

        selected_words = []
        for t in selected_topics:
            selected_words += topic_words[str(t + 1)][: N_TOP_WORDS]

        persona_agent_words[i] = selected_words
    
    return persona_agent_words

def extract_top_agent_words():
    """
    Extract the top agent words for each persona from the coefficients of the LDA model
    :param coefficients: the coefficients of the LDA model
    :return: a dict of the top words for each persona
    """

    with open("data/cmu/personas/finalLAgentsFile", "r") as f:
        
        topics = [int(x) for x in f.readline().split(" ")]
        lines = f.readlines()
        
        coefficients = []
        for l in lines:
            temp = []
            for x in l.split():
                temp.append(float(x))
            coefficients.append(temp)
            
    coefficients = np.array(coefficients)
    topics = np.array(topics)

    persona_agent_words = extract_top_words(coefficients)
    return persona_agent_words


def extract_top_patient_words():
    """
    Extract the top patient words for each persona from the coefficients of the LDA model
    :param coefficients: the coefficients of the LDA model
    :return: a dict of the top words for each persona
    """

    with open("data/cmu/personas/finalLPatientsFile", "r") as f:
        
        topics = [int(x) for x in f.readline().split(" ")]
        lines = f.readlines()
        
        coefficients = []
        for l in lines:
            temp = []
            for x in l.split():
                temp.append(float(x))
            coefficients.append(temp)
            
    coefficients = np.array(coefficients)
    topics = np.array(topics)

    persona_patient_words = extract_top_words(coefficients)
    return persona_patient_words


def extract_top_modifiee_words():
    """
    Extract the top podifiee words for each persona from the coefficients of the LDA model
    :return: a dict of the top words for each persona
    """


    with open("data/cmu/personas/finalLModFile", "r") as f:
    
        topics = [int(x) for x in f.readline().split(" ")]
        lines = f.readlines()
        
        coefficients = []
        for l in lines:
            temp = []
            for x in l.split():
                temp.append(float(x))
            coefficients.append(temp)
            
    coefficients = np.array(coefficients)
    topics = np.array(topics)

    persona_mod_words = extract_top_words(coefficients)
    return persona_mod_words


# If in this script is run
if __name__ == "__main__":
    persona_words = dict()

    persona_agent_words = extract_top_agent_words()
    persona_patient_words = extract_top_patient_words()
    persona_mod_words = extract_top_modifiee_words()


    for p_id in range(1, 51):
        persona_words[p_id] = dict()
        
        persona_words[p_id]["agent"] = persona_agent_words[p_id - 1]
        persona_words[p_id]["patient"] = persona_patient_words[p_id - 1]
        persona_words[p_id]["modifiee"] = persona_mod_words[p_id - 1]

    with open("data/cmu/personas/personas_words.json", "w") as outfile:
        json.dump(persona_words, outfile) 