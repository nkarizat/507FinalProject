# SI 507 Project-Nkarizat

SI 507 Final Project
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
 
These need to be compiled into a file named secrets.py that will be imported into the final.py document. This document contains the program that engages with the Twitter API by aggregating tweets, cleaning them, and prepping them to be turned into a word cloud. You also want to make sure you put secrets.py in the gitignore file, along with __pycache__. 

Because the program relies on a successfuly created database, you want to make sure the mi_foot_traffic.db file is located in the directory before you run the program. If you would like to see how this file was created, you can view the code to create the database at mi_foot_traffic.sql. 

Once this secrets.py file is created in the same directory as final.py and app.py, you are ready to run app.py. In running this file, you open up the Flask App at http://127.0.0.1:5000/ and it is ready to be used. 

# How It Works

1) final.py
    
    final.py contains the program necessary to engage with the twitter API and produce the necessary input for generating a word cloud. It contains multiple functions, each serving an important purpose for aggregating, and cleaning tweets. The program contains several functions, but I will highlight the most important. 
    
    A) make_request_with_cache(baseurl, hashtag, num_results=10000, lang='en')

            Role: Check the cache for a saved result for this baseurl+params:values 
            combo. If the result is found, return it. Otherwise send a new request, save it, then return it.

            Parameters
            ----------
            baseurl: string
              The URL for the API endpoint
            hashtag: string
              hashtag search

            num_results: int
              The number of tweets to retrieve
            Returns
            -------
            dict
              the results of the query as a dictionary loaded from cache JSON

    B) compile_tweets(tweet_data)

            Role: creates a list of tweets from dictionary

            Parameters
            ----------
            tweet_data: dict
              Twitter data as a dictionary for a specific query

            Returns
            -------
            a list of strings of all the tweets in the tweet_data

    C) clean_tweets(list_of_tweets)

            Role: creates a list of tweets from dictionary

            Parameters
            ----------
            tweet_data: dict
              Twitter data as a dictionary for a specific query

            Returns
            -------
            a list of cleaned tokens from all the tweets in the tweet_data
            
2) app.py
    
    app.py is where the flask app is created and ties in the various html tables in the templates directory! It contains a function that allows queries to be made in the mi_foot_traffic database, as well as a function that generates a word_cloud. app.py calls on functions located in final.py 
    
# Data Sources

  1) SafeGraph's Michigan Foot Traffic Data: I have been able to retrieve 4 CSV files from https://www.safegraph.com/ that show visitor information and foot traffic for all retail bakeries, baked goods stores, book stores and museums in Michigan! There are roughly 900 records for each month (Dec-March) and roughly 1,100 records for all collective places of interest. Each monthly record contains specific information regarding the number of visits for that month, as well as the number of unique visitors to a place of interest. 
 2) Michigan Foot Traffic DataBase: The data stored in the CSV files mentioned above was turned into a SQL database [contained in mi_foot_traffic.db]. The entity relationship diagram that shows the relationships between the several tables is located in the file of the repository called [Final Project 507 ERD.pdf]. Foreign Keys and Primary Keys, as well as the overall schema for this database is shown in the entity relationship diagram. However, below are the 'Create Table' statements for this database: 
                           
                           CREATE TABLE "category" (
                          "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                          "naics_code"	INTEGER,
                          "top_category"	TEXT,
                          "sub_category"	TEXT
                        )

                        CREATE TABLE "december_visitor_data" (
                          "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                          "safegraph_place_id"	TEXT,
                          "date_range_start"	TEXT,
                          "date_range_end"	TEXT,
                          "raw_visit_counts"	INTEGER,
                          "raw_visitor_counts"	INTEGER,
                          FOREIGN KEY("safegraph_place_id") REFERENCES "places_of_interest"("safegraph_place_id")
                        )

                        CREATE TABLE "february_visitor_data" (
                          "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                          "safegraph_place_id"	TEXT,
                          "date_range_start"	TEXT,
                          "date_range_end"	TEXT,
                          "raw_visit_counts"	INTEGER,
                          "raw_visitor_counts"	INTEGER,
                          FOREIGN KEY("safegraph_place_id") REFERENCES "places_of_interest"("safegraph_place_id")
                        )

                        CREATE TABLE "january_visitor_data" (
                          "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                          "safegraph_place_id"	TEXT,
                          "date_range_start"	TEXT,
                          "date_range_end"	TEXT,
                          "raw_visit_counts"	INTEGER,
                          "raw_visitor_counts"	INTEGER,
                          FOREIGN KEY("safegraph_place_id") REFERENCES "places_of_interest"("safegraph_place_id")
                        )

                        CREATE TABLE "march_visitor_data" (
                          "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                          "safegraph_place_id"	TEXT,
                          "date_range_start"	TEXT,
                          "date_range_end"	TEXT,
                          "raw_visit_counts"	INTEGER,
                          "raw_visitor_counts"	INTEGER,
                          FOREIGN KEY("safegraph_place_id") REFERENCES "places_of_interest"("safegraph_place_id")
                        )

                        CREATE TABLE "places_of_interest" (
                          "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                          "naics_code"	INTEGER,
                          "safegraph_place_id"	TEXT,
                          "location_name"	TEXT,
                          "street_address"	TEXT,
                          "city"	TEXT,
                          "region"	TEXT,
                          "postal_code"	INTEGER,
                          "country"	TEXT,
                          "phone"	TEXT,
                          "latitude"	REAL,
                          "longitude"	REAL,
                          FOREIGN KEY("naics_code") REFERENCES "category"("naics_code")
                        )
 3) Twitter's API: The program accesses Twitter's API to pull 10,000 tweets in english that are tagged with #COVID19. When this is retrieved, it’s put into a JSON file. The program pulls the tweets necessary and caches them. Evidence of that is in my code, as well as in the terminal with my program printing “cache hit!” if the cache has already been created, or "cache miss!" if it needs to re-pull the tweets.
 
 Note: I was told on Piazza that even though this is technically 2 data sources, that "Actually, we [the teaching team] had a discussion. We wanted to encourage you to go ahead with it as it is, especially given that it examines the impact of COVID19." For that reason, I didn't use additional data sources. 
 
# Interaction and Presentation Options 
  1) Flask Tables and/or Plotly Graphs:
  A user has the option to present their foot traffic search results in HTML tables using Flask, as well as a Plotly graph.
    They have the option to sort by:
        1) December Visits
        2) January Visits
        3) February Visits
        4) March Visits
    as well as to sort from: 
          1) High to Low
          2) Low to High
    as well as to filter by: 
          1) City
          and/or
          2) Business Industry
    
  2) Word Cloud
      -They also have the option to view up to 100 of the most frequently used words in tweets containing #COVID19. 
  
# Demo Link: https://www.youtube.com/watch?v=IzAhXUtNlus
 
 

    



