##Libraries
from flask import Flask, render_template, flash, request, jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from config import Config
from forms import ReusableForm

#csv/df manipulations
import pandas as pd
import numpy as np

#maps
from flask_googlemaps import GoogleMaps,Map

#custom functions from functions.py
from functions import jensen_shannon,get_most_similar_documents,get_top_ten

#libraries for rendering images
import requests
import json

# for using pickled files and creating graphs
import pickle
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


# create the application object
app = Flask(__name__)
app.config.from_object(Config)
app.config['GOOGLEMAPS_KEY'] = ""
GoogleMaps(app)

#yelp api key
api_key=""
        

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/vis/<id2>/<id>', methods=['GET', 'POST'])
def vis(id,id2):
    return render_template('vis.html',id = id,id2 = id2)

@app.route('/<dept_restaurant>/<departure>/<destination>/<dest_restaurant>')
def restaurant_reviews(dept_restaurant,departure,destination,dest_restaurant):
    #input: restaurant, destination
    #output: passes info to restaurant.html
    #info obtained from yelp api + cleaned csv files

    #data -> restaurant in destination city
    #data_original -> restaurant to be replicated

    data = pd.read_csv("csv/"+ destination + ".csv")
    data = data[data.name ==dest_restaurant].reset_index(drop=True)
    id = data.loc[0,"business_id"]

    data_original = pd.read_csv("csv/"+ departure + ".csv")
    data_original = data_original[data_original.name ==dept_restaurant].reset_index(drop=True)
    id2 = data_original.loc[0,"business_id"]
    
    #getting top 5 positive/negative sentimemts
    positive = eval(data.loc[0,"postive_reviews"])[:5]
    negative = eval(data.loc[0,"negative_reviews"])[:5]
    
    #stars
    stars = data.loc[0,"stars"]

    #yelp api call
    headers = {'Authorization': 'Bearer %s' % api_key}
    url='https://api.yelp.com/v3/businesses/' + id
    req=requests.get(url, params={'location':destination}, headers=headers)
    
    phone = req.json()["display_phone"]
    image = requests.get(req.json()["image_url"])
    yelp_website = req.json()["url"]
        
    with open("static/images_" + id +".jpg", 'wb') as f:
        f.write(image.content)
    
    #creating visualization of topic distribution for query
    lda = pickle.load(open("pickled/" + destination + "_lda.pkl","rb"))
    dictionary = pickle.load(open("pickled/" + destination + "_dictionary.pkl","rb"))
    new_bow = dictionary.doc2bow(eval(data.iloc[0,-3]))
    new_bow_dept = dictionary.doc2bow(eval(data_original.iloc[0,-3]))


    new_doc_distribution = np.array([tup[1] for tup in lda.get_document_topics(bow=new_bow)])
    new_doc_distribution_dept = np.array([tup[1] for tup in lda.get_document_topics(bow=new_bow_dept)])
    labels = [' Topic1',' Topic2',' Topic3',' Topic4',' Topic5',' Topic6']
    angle=np.linspace(0, 2*np.pi, len(labels), endpoint=False)


    stats=np.concatenate((new_doc_distribution,[new_doc_distribution[0]]))
    stats2=np.concatenate((new_doc_distribution_dept,[new_doc_distribution_dept[0]]))

    angles=np.concatenate((angle,[angle[0]]))
    plt.polar(angles,stats,label = dest_restaurant)
    plt.fill_between(angles, stats, 'b', alpha=0.4)



    plt.polar(angles,stats2,label = dept_restaurant)
    plt.fill_between(angles, stats2, 'b', alpha=0.4)
    plt.xticks(angles[:-1], labels)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.savefig('static/'+id2+"_" +id+'.png')
    plt.show()
    plt.close()

    return render_template('restaurant.html',restaurant = dest_restaurant, destination = destination,negative = negative,positive = positive,stars = stars, id = id, id2 = id2,phone = phone,graph = 'graph_'+id+".png" ,image ='images_'+id+".jpg",yelp_website = yelp_website)

@app.route("/map", methods=['POST', 'GET'])
def get_information():
    #Takes in information from form, 
    #Outputs Map, along with hyperlinks of top 10 similar restaurants
    form = ReusableForm(request.form)
    print (form.errors)


    if request.method == 'POST':

        try:
            departure=request.form['departure']
            destination=request.form['destination']
            restaurant=request.form['restaurant']
            query = pd.read_csv("csv/" + departure +'.csv')
            query = query[query["name"] == restaurant]

            # if more than one business has the same name
            if query.shape[0]>1:
                address = query.address.values
                #let user select which address is being referred to
                return render_template('address.html', restaurant = restaurant, address = address, departure = departure, destination =destination )
            
            else:
                most_similar_df = get_top_ten(query,departure,destination)
                names =  most_similar_df.name.tolist()
                latitudes = most_similar_df.latitude.tolist()
                longitudes = most_similar_df.longitude.tolist()
                locations = list(zip(latitudes,longitudes,names))
                
                mymap = Map(
                    identifier="view-side",
                    lat=33.4227198,
                    lng= -111.79821229999999,
                    markers = [{"lat":loc[0], "lng":loc[1], "infobox": loc[2]} for loc in locations],
                    fit_markers_to_bounds = True,
                    style="width:100%; height:100%;"
                )
            
                return render_template('map.html', names = names ,map=mymap,destination = destination,restaurant = restaurant,departure = departure)
        except:
            return render_template('error.html')

@app.route('/map2', methods=['POST', 'GET'])
def get_information2():
    #If more than 2 locations with same name
    if request.method == 'POST':
        address=request.form['address']
        departure = request.form['departure']
        destination = "mesa"
        query = pd.read_csv("csv/" + departure +'.csv')
        query = query[query["address"] == address]
        restaurant = query.name.values[0]

        most_similar_df = get_top_ten(query,departure,destination)

        
        names =  most_similar_df.name.tolist()
        latitudes = most_similar_df.latitude.tolist()
        longitudes = most_similar_df.longitude.tolist()
        locations = list(zip(latitudes,longitudes,names))
        


        mymap = Map(
        identifier="view-side",
        lat=33.4227198,
        lng= -111.79821229999999,
        markers = [{"lat":loc[0], "lng":loc[1], "infobox": loc[2]} for loc in locations],
        fit_markers_to_bounds = True,
        style="width:100%; height:100%;"
        )
        

        return render_template('map.html', names = names ,map=mymap,destination = destination,restaurant = restaurant)
        


    else:
        return render_template('base.html', form=form,map = mymap)

if __name__ == '__main__':
    app.run(debug = True)