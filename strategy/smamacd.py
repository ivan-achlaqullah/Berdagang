# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 19:34:12 2017

@author: Ivan Achlaqullah
"""

#### Strategy Start HERE ####

## Define Lenth to calculate MACD
fastLength = 12
slowLength = 26
signalLength = 9
veryslowLength = 200

## Function to calculate SMA
def sma(posisi, banyak, tpair, ohlc):
    tetsx = 0
    for x in range(banyak):
        tetsx = tetsx + float(ohlc['result'][tpair][posisi - x][4])
    tetsx = tetsx / banyak
    return tetsx

def hitungsignal(posisi, tpair, ohlc):
    hasilsignal = 0
    for x in range(signalLength):
        hasilsignal = hasilsignal + sma(posisi - x, fastLength, tpair, ohlc) - sma(posisi - x, slowLength, tpair, ohlc)
    hasilsignal = hasilsignal / signalLength
    return hasilsignal

## Main logic for strategy

def calculate(posisinya, tpair, ohlc):

    ## Calculate Moving Average BEFORE the current bar
    fastMA = sma(posisinya-1, fastLength, tpair, ohlc)
    slowMA = sma(posisinya-1, slowLength, tpair, ohlc)
    veryslowMA = sma(posisinya-1, veryslowLength, tpair, ohlc)
    macd = fastMA - slowMA
    signal = hitungsignal(posisinya-1, tpair, ohlc)
    hist_old = macd - signal

    ## Calculate current Moving Average
    fastMA = sma(posisinya, fastLength, tpair, ohlc)
    slowMA = sma(posisinya, slowLength, tpair, ohlc)
    veryslowMA = sma(posisinya, veryslowLength, tpair, ohlc)
    macd = fastMA - slowMA
    signal = hitungsignal(posisinya, tpair, ohlc)
    hist = macd - signal


    ## If crossover, open LONG
    if hist_old < 0 :
        if hist > 0 :
            if macd > 0 :
                if fastMA > slowMA :
                    if float(ohlc['result'][tpair][posisinya - slowLength][4]) > veryslowMA :
                        ## CALL LONG
                        return 'long'

    ## If crossunder, open SHORT
    elif hist_old > 0 :
        if hist < 0 :
            if macd < 0 :
                if fastMA < slowMA :
                    if float(ohlc['result'][tpair][posisinya - slowLength][4]) < veryslowMA :
                        ## CALL SHORT
                        return 'short'

    else:
        return 'none'