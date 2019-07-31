# AMLI-Final-Project - Analyzing Yelp Data 

Team: Xijie Guo, Marissa Kelley, Marc Mascarenhas, and Jesse Stewart

July 2019

## Overview:
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
