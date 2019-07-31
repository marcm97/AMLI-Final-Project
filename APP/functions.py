import pandas as pd
import numpy as np

import pickle 
from scipy.stats import entropy

from flask import render_template
import matplotlib.pyplot as plt



def jensen_shannon(query, matrix):
    """
    This function implements a Jensen-Shannon similarity
    between the input query (an LDA topic distribution for a document)
    and the entire corpus of topic distributions.
    It returns an array of length M where M is the number of documents in the corpus
    """
    # lets keep with the p,q notation above
    p = query[None,:].T # take transpose
    q = matrix.T # transpose matrix
    m = 0.5*(p + q)
    return np.sqrt(0.5*(entropy(p,m) + entropy(q,m)))

def get_most_similar_documents(query,matrix,k=10):
    """
    This function implements the Jensen-Shannon distance above
    and retruns the top k indices of the smallest jensen shannon distances
    """
    sims = jensen_shannon(query,matrix) # list of jensen shannon distances
    return sims.argsort()[:k] # the top k positional index of the smallest Jensen Shannon distances




def get_top_ten(query,departure,destination):

    lda = pickle.load(open("pickled/" + destination + "_lda.pkl","rb"))
    dictionary = pickle.load(open("pickled/" + destination + "_dictionary.pkl","rb"))
    doc_topic_dist = pickle.load(open("pickled/" + destination + "_dist.pkl","rb"))

    destination = pd.read_csv("csv/" +destination+ ".csv")
    #get the ids of the most similar businesses
    new_bow = dictionary.doc2bow(eval(query.iloc[0,-3]))
    new_doc_distribution = np.array([tup[1] for tup in lda.get_document_topics(bow=new_bow)])
    most_sim_ids = get_most_similar_documents(new_doc_distribution,doc_topic_dist)

    # print the results
    most_similar_df = destination.iloc[most_sim_ids,:]
    return most_similar_df


