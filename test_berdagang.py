# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 19:19:32 2017

@author: Ivan Aclaqullah
"""

from berdagang import *
import ngetweet

def test_cekdompet():
    cekdompet()

def test_tweet():
    ngetweet.tweet('test')

def test_strategy():
    testorder = strategy.calculate(lastclose-1, tpair, ohlc)

    if testorder == 'none':
        print('Strategy test succes')
    if testorder == 'long':
        print('Strategy test succes')
    if testorder == 'short':
        print('Strategy test succes')