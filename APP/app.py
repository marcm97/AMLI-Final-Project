from flask import Flask, render_template, flash, request, jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from config import Config
from forms import LoginForm,ReusableForm

import pickle
import pandas as pd
from scipy.stats import entropy
import numpy as np

from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons 


# create the application object
app = Flask(__name__)
app.config.from_object(Config)
app.config['GOOGLEMAPS_KEY'] = "  <script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCjmRF-E30xmEShihkMA8thF9nGiLqUtNY&callback=initMap"type="text/javascript"></script>" 
GoogleMaps(app)

mesa_lda = pickle.load(open("mesa_lda.pkl","rb"))
mesa_tfidf = pickle.load(open("mesa_tfidf.pkl","rb"))
mesa_dictionary = pickle.load(open("mesa_dictionary.pkl","rb"))
mesa_doc_topic_dist = pickle.load(open("mesa_doc_topic_dist.pkl","rb"))



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


def get_top_ten(departure,destination,restaurant):
    query = pd.read_csv(departure +'_cleaned.csv')
    destination = pd.read_csv("reviews"+"_"+destination+ ".csv")
    df = destination.head()

    query = query[query["name"] == restaurant]
    #get the ids of the most similar businesses
    new_bow = mesa_dictionary.doc2bow(eval(query.iloc[0,3]))
    new_doc_distribution = np.array([tup[1] for tup in mesa_lda.get_document_topics(bow=mesa_tfidf[new_bow])])
    most_sim_ids = get_most_similar_documents(new_doc_distribution,mesa_doc_topic_dist)

    # print the results
    most_similar_df = destination[destination.index.isin(most_sim_ids)]
    return(most_similar_df)

@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('index2.html')

@app.route('/test')
def map():
    return render_template('results.html')


@app.route("/map", methods=['POST', 'GET'])
def get_information():
    form = ReusableForm(request.form)
    print (form.errors)

    mymap = Map(
        identifier="view-side",
        lat=33.4227198,
        lng= -111.79821229999999,
        markers=[(33.4227198, -111.79821229999999),
 (33.383889224200004, -111.85933446930001),
 (33.3840839, -111.84369640000001),
 (33.374984999999995, -111.68716299999998),
 (33.415843699999996, -111.6688207)],
        style="width:100%; height:400px;"
     )

    if request.method == 'POST':
        departure=request.form['departure']
        destination=request.form['destination']
        restaurant=request.form['restaurant']

        most_similar_df = get_top_ten(departure,destination,restaurant)[["name"]]
        
        return render_template('simple.html',  tables=[most_similar_df.to_html(classes='data')], titles=most_similar_df.columns.values,map=mymap)
        #return render_template('results.html',  search_term=search_term, departure=departure, destination=destination)
    else:
        return render_template('index.html', form=form,map = mymap)

# Run the app from here
if __name__ == '__main__':
    app.run(debug = True)