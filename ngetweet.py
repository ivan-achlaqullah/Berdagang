# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 09:36:17 2017

@author: Ivan Achlaqullah

Script for tweeting what the bot are doing
"""

import tweepy

## Insert twitter api
CONSUMER_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ACCESS_KEY = 'XXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ACCESS_SECRET = 'wXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

## Load key 
auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
apitweet = tweepy.API(auth)

def tweet(pesan):
    apitweet.update_status(pesan)
    
