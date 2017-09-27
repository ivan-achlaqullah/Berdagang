# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 09:36:17 2017

@author: Ivan Achlaqullah

Script for tweeting what the bot are doing
"""

import tweepy
import config

## Load key, only load if not in testing
if config.testing != 2:
    auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth.set_access_token(config.ACCESS_KEY, config.ACCESS_SECRET)
    apitweet = tweepy.API(auth)

def tweet(pesan):
    if config.testing != 2:
        apitweet.update_status(pesan)
