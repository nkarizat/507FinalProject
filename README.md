# SI 507 Project-Nkarizat

SI 507 Final Project Readme
Nadia Karizat 14616211

github repository: https://github.com/nkarizat/507FinalProject

# Project Summary
This program allows a user to see visitor/foot traffic of Michigan's Book Stores, Museums, Baked Goods Stores, and Retail Bakeries during the COVID-19 pandemic, since calls for social-distancing began to make their way in Michigan (Dec-Present). Users will be able to view foot traffic in a Flask App that allows them to filter by City and Business Industry, as well as to sort by a specific month's visits. They can view their results in either an HTML table, or a Plotly graph. 

This program also allows users to see the most frequently used words in tweets tagged with #COVID19. The information will be presented to them as a Word Cloud on a page of the Flask App. 

# Required Packages
To operate this program, you need to use the following packages (and some of their built-in packages): 
  1) sqlite3
  2) requests_oauthlib
  3) json
  4) requests
  5) nltk
  6) collections
  7) WordCloud
  8) Matplotlib.pyplot
  9) Flask
  10) plotly.graph_objects
  11) BytesIO
  12) base64

# Instructions
Before beginning to try and operate this program, a user needs to have access to Twitter's API. From this API, they need to obtain a:
  1) TWITTER_API_KEY
  2) TWITTER_API_SECRET
  3) TWITTER_ACCESS_TOKEN
  4) TWITTER_ACCESS_TOKEN_SECRET
 
These need to be compiled into a file named secrets.py that will be imported into the final.py document. This document contains the program that engages with the Twitter API by aggregating tweets, cleaning them, and prepping them to be turned into a word cloud.

Because the program relies on a successfuly created database, you want to make sure the mi_foot_traffic.db file is located in the directory before you run the program. If you would like to see how this file was created, you can view the code to create the database at mi_foot_traffic.sql. 

Once this secrets.py file is created in the same directory as final.py and app.py, you are ready to run app.py. In running this file, you open up the Flask App at http://127.0.0.1:5000/ and it is ready to be used. 

# Instructions

1) final.py
    
    final.py contains the program necessary to engage with the twitter API and produce the necessary input for generating a word cloud. It contains multiple functions, each serving an important purpose for aggregating, and cleaning tweets. 

 


