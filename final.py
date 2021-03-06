# github repository: https://github.com/nkarizat/507FinalProject
# Uniqname: nkarizat
# Name: Nadia Karizat

import sqlite3
from requests_oauthlib import OAuth1
import json
import requests
import secrets #file containing my twitter API
import nltk
import re
from nltk.corpus import stopwords
from nltk import word_tokenize, pos_tag
from collections import defaultdict
import collections
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

CACHE_FILENAME = "tweets_cache.json"
CACHE_DICT = {}

client_key = secrets.TWITTER_API_KEY
client_secret = secrets.TWITTER_API_SECRET
access_token = secrets.TWITTER_ACCESS_TOKEN
access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

oauth = OAuth1(client_key,
            client_secret=client_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret)



def test_oauth():
    ''' Helper function that returns an HTTP 200 OK response code and a 
    representation of the requesting user if authentication was 
    successful; returns a 401 status code and an error message if 
    not. Only use this method to test if supplied user credentials are 
    valid. Not used to achieve the goal of this assignment.'''

    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    auth = OAuth1(client_key, client_secret, access_token, access_token_secret)
    authentication_state = requests.get(url, auth=auth).json()
    return authentication_state

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''

    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f"{k}_{params[k]}")
    param_strings.sort()
    unique_key = baseurl + connector + connector.join(param_strings)
    return unique_key

def make_request(url,params):
    '''Make a request to the Web API using the baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the data returned from making the request in the form of 
        a dictionary
    '''
    response = requests.get(url, params=params, auth=oauth)
    return response.json()

def make_request_with_cache(baseurl, hashtag, num_results=10000, lang="en"):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint

    hashtag: string
    - hashtag search

    num_results: int
    - The number of tweets to retrieve
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    params={"q":f"{hashtag}", "count":f'{num_results}', "lang":f'{lang}'}
    request_key = construct_unique_key(baseurl, params)
    if request_key in CACHE_DICT.keys():
        print("cache hit!", request_key)
        return CACHE_DICT[request_key]
    else:
        print("cache miss!", request_key)
        CACHE_DICT[request_key] = make_request(baseurl,params)
        save_cache(CACHE_DICT)
        return CACHE_DICT[request_key]

def compile_tweets(tweet_data):
    ''' creates a list of tweets from dictionary

    Parameters
    ----------
    tweet_data: dict
        Twitter data as a dictionary for a specific query

    Returns
    -------
    a list
        a list of strings of all the tweets in the tweet_data

    '''
    list_of_tweets=[]
    for k,v in tweet_data.items():
        if k == 'statuses':
            for tweet in v:
                list_of_tweets.append(tweet['text'])
    return list_of_tweets

def clean_tweets(list_of_tweets):
    ''' creates a list of tweets from dictionary

    Parameters
    ----------
    tweet_data: dict
        Twitter data as a dictionary for a specific query

    Returns
    -------
    a list
        a list of cleaned tokens from all the tweets in the tweet_data

    '''
    #remove "@" (all twitter handles) from tweets
    list_wo_handles=[]
    for x in list_of_tweets:
        list_of_words=[] 
        lists=x.split(" ")
        for word in lists:
            if "@" not in word:
                list_of_words.append(word)
        list_wo_handles.append(list_of_words)


    #creates a list of tweets without their handles
    list_of_tweets_=[]
    for x in list_wo_handles:
        list_of_tweets_.append(' '.join(x))

    #creates a list of tokens w/o stopwords, punctuation, as well as certain words like rt, https, http, etc to clean things up as much as possible. 
    list_of_tokens=[]
    for text in list_of_tweets_:
        words=nltk.word_tokenize(text.lower())
        S = set(stopwords.words('english'))
        tokens_stop_removed = []
        for token in words:
            if not token.lower() in S:
                tokens_stop_removed.append(token)
        stop_removed = ' '.join(tokens_stop_removed)
        summary_words = nltk.word_tokenize(stop_removed)
        also_remove= ["rt", 'https', 'http']
        word = [word for word in summary_words if word not in also_remove]
        words=[word.lower() for word in word if word.isalpha()]
        list_of_tokens.append(words)
    flatList = [ item for elem in list_of_tokens for item in elem]
    list_of_tweets=str(flatList)

    return list_of_tweets

def generate_word_cloud(list_of_tweets):
    ''' creates a word cloud from a string of tweets

    Parameters
    ----------
    list_of_tweets: list
        list of tweets that are tokenized

    Returns
    -------
    a word cloud
        a word cloud of the 50 most-frequently used tokens in the list of tweets

    '''
    wordcloud_spam = WordCloud(background_color="white", max_font_size=50, max_words=50).generate(list_of_tweets)
    plt.figure(figsize = (15,15))
    plt.imshow(wordcloud_spam, interpolation='bilinear')
    plt.axis("off")

CACHE_DICT = open_cache()
baseurl = "https://api.twitter.com/1.1/search/tweets.json"
hashtag="#COVID19"