# SI 507 Project-Nkarizat

SI 507 Final Project Readme
Nadia Karizat 14616211

github repository: https://github.com/nkarizat/507FinalProject

# Project Summary
This program allows a user to see visitor/foot traffic of Michigan's Book Stores, Museums, Baked Goods Stores, and Retail Bakeries during the COVID-19 pandemic, since calls for social-distancing began to make their way in Michigan (Dec-Present). Users will be able to view foot traffic in a Flask App that allows them to filter by City and Business Industry, as well as to sort by a specific month's visits. They can view their results in either an HTML table, or a Plotly graph. 

This program also allows users to see the most frequently used words in tweets tagged with #COVID19. The information will be presented to them as a Word Cloud on a page of the Flask App. 

# Required Packages
To operate this program, you need to use the following packages (and some of their built-in packages): 
  sqlite3
  requests_oauthlib
  json
  requests
  nltk
  collections
  WordCloud
  Matplotlib.pyplot
  Flask
  plotly.graph_objects
  BytesIO
  base64

# Instructions
Before beginning to try and operate this program, a user needs to have access to Twitter's API. From this API, they need to obtain a:
  1) TWITTER_API_KEY
  2) TWITTER_API_SECRET
  3) TWITTER_ACCESS_TOKEN
  4) TWITTER_ACCESS_TOKEN_SECRET
 
These need to be compiled into a file named secrets.py that will be imported into the final.py document. This document contains the program that engages with the Twitter API by aggregating tweets, cleaning them, and prepping them to be turned into a word cloud. 
 


