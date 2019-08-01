# AMLI-Final-Project - Analyzing Yelp Data 

Team: 
- [Xijie Guo](https://www.linkedin.com/in/xijie-guo/) 
- [Marissa Kelley](https://www.linkedin.com/in/marissa-kelley/)
- [Marc Mascarenhas](https://www.linkedin.com/in/marc-mascarenhas/)
- [Jesse Stewart](https://www.linkedin.com/in/jesse-stewart-413391156/) 

July 2019

## Overview:
"A recommender system that helps you find restaurants in a city that are similar to a given restaurant in another city.” 

EatLike is a recommendation engine based on topic modeling, the Natural Language Toolkit (NLTK), and sentiment analysis. EatLike provides users with a selection of restaurants ordered by their topic similarity to a given query restaurant. Furthermore, EatLike allows users to see the top positive and negative statements about a given restaurant.

## 1. Dataset
www.yelp.com/dataset

9 GB unzipped
Files: 
  - reviews.json
  - business.json
  - users.json
  - checkin.json
  - tips.json

Currently, the Flask site only inputs data from three cities: Mesa,AZ, Pittsburgh, PA, and Charlotte, NC. 

## 2. Topic Models
Instead of looking at the star ratings on Yelp, EatLike pulls topics from the Yelp reviews and offers sentiment analysis on the reviews as well. Five randomly selected positive and negative sentences across all of the reviews of a restaurant are selected as highlights. 

## 3. The Machine Learning model
EatLike uses latent dirichlet allocation implemented in the Python package genism to extract topics from restaurant reviews. 

Gensim was particularly essential for constructing the EatLike topic model.
Topic models are used in statistical data modeling to predict the topic(s) of a given corpus. Three variations of topic models were explored for the purpose of developing EatLike: Latent Dirichlet Allocation (LDA), Hierarchical Dirichlet Process (HDP), and Latent Semantic Index (LSI).

## 4. Installation and Running Locally 
Please see the requirements.txt file 

(Create a new environment until you add files, then freeze it and get the requirements txt.???) 

## 5. Replicating Code
- Step 1: Go to www.yelp.com/dataset and download zipped json files
- Step 2: Upload files to Google Cloud Bucket
- Step 3: Run "yelp_query.ipynb":This creates 3 datasets (of 3 cities) and filters out restaurants in those cities with>100 reviews. 
- Step 4: Run "preprocessing on the 3 csv's.
This outputs 3 csv files: "mesa_reviews_5000.csv","pittsburgh_reviews_5000.csv" & "charlotte_reviews_5000.csv"
- Step 4: "topic_modeling.ipynb" contains code which was used to fine tune LDA, HDP & LSI models. Results from this process can be found in the folder "plots. LSI had the best coherence results, however, we weren't able to get the topic distribution using Gensim. We decided to use LDA - it was much more interpretable and easy to visualize using pyLDAvis
- Step 5: Run ".ipynb". This creates pickled files of the model, dictionary of words & document topic distribution for each of the cities
- Step 6: The APP file uses these pickled files and csv files to run a flask application

