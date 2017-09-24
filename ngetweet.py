# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 09:36:17 2017

@author: Ivan Achlaqullah

Script for tweeting what the bot are doing
"""

import tweepy
import config

## Insert twitter api
CONSUMER_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ACCESS_KEY = 'XXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ACCESS_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

## Load key, only load if not in testing
if config.testing != 1:
    auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
    apitweet = tweepy.API(auth)

def tweet(pesan):
    if config.testing != 1:
        apitweet.update_status(pesan)
    
