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
import cv2 as cv

import pickle
import matplotlib.pyplot as plt






# create the application object
app = Flask(__name__)
app.config.from_object(Config)
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDtYp6V7WFFzm5JpAGBYwIXnayqN4E-Z1Q"
GoogleMaps(app)

#yelp api key
api_key="CjSlZf6-T83KQTmcssS499VYq6bzAICqtwPfk0zz7tFOtBfV1uNROedPiXJaCduFfBAHAfKKijOWtwUnBnI5_am4eBdE3tPqDVJ0NiTAOBAnFrs2cp967NQWfpBrW3Yx"
        

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/vis/test/<id>', methods=['GET', 'POST'])
def vis(id):
    return render_template('vis.html',id = id)


@app.route('/<destination>/<restaurant>')
def restaurant_reviews(restaurant,destination):
    #input: restaurant, destination
    #output: passes info to restaurant.html
    #info obtained from yelp api + cleaned csv files
    data = pd.read_csv("csv/"+ destination + ".csv")
    data = data[data.name ==restaurant].reset_index(drop=True)
    id = data.loc[0,"business_id"]
    
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
    
    lda = pickle.load(open("pickled/" + destination + "_lda.pkl","rb"))
    dictionary = pickle.load(open("pickled/" + destination + "_dictionary.pkl","rb"))
    new_bow = dictionary.doc2bow(eval(data.iloc[0,-3]))
    new_doc_distribution = np.array([tup[1] for tup in lda.get_document_topics(bow=new_bow)])
    labels = ['topic1','topic2','topic3','topic4','topic5','topic6']
    angle=np.linspace(0, 2*np.pi, len(labels), endpoint=False)

    vals = new_doc_distribution

    stats=np.concatenate((vals,[vals[0]]))
    angles=np.concatenate((angle,[angle[0]]))
    plt.polar(angles,stats)
    # for i in range(vals):
    #     plt.text(0.05,0.95-i,vals[i])
    plt.savefig('static/'+ id+'.png')
    plt.show()

    
    

    with open("static/images_" + id +".jpg", 'wb') as f:
        f.write(image.content)

    return render_template('restaurant.html',restaurant = restaurant, destination = destination,negative = negative,positive = positive,stars = stars, id = id, phone = phone,graph = 'graph_'+id+".png" ,image ='images_'+id+".jpg",yelp_website = yelp_website)


@app.route("/map", methods=['POST', 'GET'])
def get_information():
    
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
            
                return render_template('map.html', names = names ,map=mymap,destination = destination,restaurant = restaurant)
        except:
            return render_template('error.html')


@app.route('/map2', methods=['POST', 'GET'])

def get_information2():


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