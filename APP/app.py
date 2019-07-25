from flask import Flask, render_template, flash, request, jsonify
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from config import Config
from forms import ReusableForm

import pandas as pd
import numpy as np

from flask_googlemaps import GoogleMaps,Map

from functions import jensen_shannon,get_most_similar_documents,get_top_ten


# create the application object
app = Flask(__name__)
app.config.from_object(Config)
app.config['GOOGLEMAPS_KEY'] = "key"
GoogleMaps(app)
        

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('base.html')

@app.route('/<destination>/<some_place>')
def home2(some_place,destination):
    data = pd.read_csv("csv/reviews" + "_" + destination + ".csv")
    text = data[data.name ==some_place].text.values

    return render_template('base2.html',place = some_place,place2 = destination,text=text)


@app.route("/map", methods=['POST', 'GET'])
def get_information():
    form = ReusableForm(request.form)
    print (form.errors)


    if request.method == 'POST':
        try:
            departure=request.form['departure']
            destination=request.form['destination']
            restaurant=request.form['restaurant']

            most_similar_df = get_top_ten(departure,destination,restaurant)
            latitudes = most_similar_df.latitude.tolist()
            names =  most_similar_df.name.tolist()
        
            
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
            return render_template('base.html')


    else:
        return render_template('base.html', form=form,map = mymap)

if __name__ == '__main__':
    app.run(debug = True)