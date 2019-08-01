import pandas as pd
import numpy as np

import pickle 
from scipy.stats import entropy

from flask import render_template
import matplotlib.pyplot as plt
from gensim.matutils import kullback_leibler




def get_most_similar_documents(query, corpus, dictionary, k=10):
    distances = []
    for c in corpus:
        distances.append(kullback_leibler(query, c, num_features=len(dictionary)))
    
    indices = np.array(distances).argsort()[:k]
    return indices


def get_most_similar_businesses(query_data, corpus, dictionary, model):
    query_bow = dictionary.doc2bow(query_data)
    most_sim_ids = get_most_similar_documents(model[query_bow], model[corpus], dictionary)
    return most_sim_ids


def get_topic_dist(model, corpus):
    doc_topic_dist = np.array([[tup[1] for tup in lst] for lst in model[corpus]])
    return doc_topic_dist

def get_top_ten(query,departure,destination):

    lda = pickle.load(open("pickled3/" + destination + "_lda.pkl","rb"))
    dictionary = pickle.load(open("pickled3/" + destination + "_dictionary.pkl","rb"))
    corpus = pickle.load(open("pickled3/" + destination + "_corpus.pkl","rb"))

    

    destination = pd.read_csv("csv/" +destination+ ".csv")
    #get the ids of the most similar businesses
    most_sim_ids = get_most_similar_businesses(eval(query.iloc[0]['tokenized']), corpus, dictionary,lda)


    # print the results
    most_similar_df = destination.iloc[most_sim_ids,:]
    return most_similar_df


