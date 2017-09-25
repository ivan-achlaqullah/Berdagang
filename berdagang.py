# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 16:36:27 2017

@author: Ivan Achlaqullah
"""

## Berdagang.py, Cryptocurrency Trading Bot with Automatic Tweet Support##
## Made by Ivan Achlaqullah

import time
import krakenex

## Import script buatan sendiri
import config    ## Skrip pengaturan
import ngetweet  ## Skrip integrasi twitter

k = krakenex.API()
k.load_key('kraken.key')

## Load settings from config.py
testing = config.testing

## IMPORTANT INT
statusPosition = 0 ## 0 = no position, 1 = short, 2 = long
leverage = config.leverage
balance = 0.0

## Cek isi ballance
def cekdompet():
    if testing == 0:
        dompet = k.query_private('TradeBalance')
        global balance
        balance = float(dompet['result']['eb'])
        #print('Balance : ' + str(balance))
        time.sleep(2)

cekdompet()

## Get OHLC data from kraken
ohlc = k.query_public('OHLC', req = {'pair': config.pair, 'interval': config.chart_interval})
time.sleep(2)

## Get offical trading pair name from kraken
tpair = ''
for key, value in ohlc['result'].items():
    if key != 'last':
        tpair = key

## Get the lastets closing price from OHLC
lastclose = len(ohlc['result'][tpair])
lastclose = lastclose - 1

## Check if there is open positions in the account.
if testing == 0 :
    buka = k.query_private('OpenPositions')
    time.sleep(2)
    
    if len(buka['result']) == 0 :
        statusPosition = 0
    else :
        bukastatusid = ''
        for key, value in buka['result'].items() :
            bukastatusid  = key
            
        if buka['result'][bukastatusid]['type'] == 'buy':
            statusPosition = 2
            #print('long')
        if buka['result'][bukastatusid]['type'] == 'sell':
            statusPosition = 1
            #print('short')

## Function to CLOSE open position

def closelong(posisinya) :
    print(str(ohlc['result'][tpair][posisinya][0]) + " " + str(posisinya) +
          " STOP Long : " + ohlc['result'][tpair][posisinya][4])

    global testing
    if testing == 0:
        ngetweet.tweet(str(ohlc['result'][tpair][posisinya][0]) + " " + str(posisinya) +
              " STOP Long : " + ohlc['result'][tpair][posisinya][4])
        
        while True:
            beli = k.query_private('AddOrder',
                            {'pair': tpair,
                             'type': 'sell',
                             'ordertype': 'market',
                             'volume': '0',
                             'leverage': str(leverage)})
            time.sleep(2)
            if len(beli['error']) == 0:
                break
        
        cekdompet()
        
def closeshort(posisinya) :
    print(str(ohlc['result'][tpair][posisinya][0]) + " " + str(posisinya) + 
          " STOP Short : " + ohlc['result'][tpair][posisinya][4])

    global testing
    if testing == 0:
        ngetweet.tweet(str(ohlc['result'][tpair][posisinya][0]) + " " + str(posisinya) + 
              " STOP Short : " + ohlc['result'][tpair][posisinya][4])
    
        while True:
            beli = k.query_private('AddOrder',
                            {'pair': tpair,
                             'type': 'buy',
                             'ordertype': 'market',
                             'volume': '0',
                             'leverage': str(leverage)})
            time.sleep(2)
            if len(beli['error']) == 0:
                break

        cekdompet()
        
## Function to OPEN new position
        
def bukalong(posisinya) :
    print (str(ohlc['result'][tpair][posisinya][0]) + " " + str(posisinya) +
           " OPEN Long, Price : " + ohlc['result'][tpair][posisinya][4])

    global testing
    global balance
    global leverage
    
    if testing == 0:
        ngetweet.tweet(str(ohlc['result'][tpair][posisinya][0]) + " " + str(posisinya) +
               " OPEN Long, Price : " + ohlc['result'][tpair][posisinya][4])
        
        while True:
            harga = (balance * 0.95 * leverage) / float(ohlc['result'][tpair][posisinya][4])
            beli = k.query_private('AddOrder',
                            {'pair': tpair,
                             'type': 'buy',
                             'ordertype': 'market',
                             'volume': str(harga),
                             'leverage': str(leverage)})
            time.sleep(1)
            if len(beli['error']) == 0:
                break

def bukashort(posisinya) :
    print (str(ohlc['result'][tpair][posisinya][0]) + " " + str(posisinya) +
           " OPEN Short, Price : " + ohlc['result'][tpair][posisinya][4])
    
    global testing
    global balance
    global leverage
    
    if testing == 0:
        ngetweet.tweet(str(ohlc['result'][tpair][posisinya][0]) + " " + str(posisinya) +
               " OPEN Short, Price : " + ohlc['result'][tpair][posisinya][4])
        
        while True:
            harga = (balance * 0.95 * leverage) / float(ohlc['result'][tpair][posisinya][4])
            beli = k.query_private('AddOrder',
                            {'pair': tpair,
                             'type': 'sell',
                             'ordertype': 'market',
                             'volume': str(harga),
                             'leverage': str(leverage)})
            time.sleep(1)
            if len(beli['error']) == 0:
                break

#### Strategy Start HERE ####

## Define Lenth to calculate MACD
fastLength = 12
slowLength = 26
signalLength = 9
veryslowLength = 200


## Function to calculate SMA
def sma(posisi,banyak):
    tetsx = 0
    for x in range(banyak):
        tetsx = tetsx + float(ohlc['result'][tpair][posisi - x][4])
    tetsx = tetsx / banyak
    return tetsx

def hitungsignal(posisi):
    hasilsignal = 0
    for x in range(signalLength):
        hasilsignal = hasilsignal + sma(posisi - x, fastLength) - sma(posisi - x, slowLength)
    hasilsignal = hasilsignal / signalLength
    return hasilsignal
            
## Main logic for strategy

def berhitung(posisinya):
    
    ## ITS GLOBAL PYTHON !!!!
    global statusPosition
    
    #print(str(posisinya)+ " " + str(statusPosition))
    
    ## Calculate Moving Average BEFORE the current bar
    fastMA = sma(posisinya-1, fastLength)
    slowMA = sma(posisinya-1, slowLength)
    veryslowMA = sma(posisinya-1, veryslowLength)
    macd = fastMA - slowMA
    signal = hitungsignal(posisinya-1)
    hist_old = macd - signal

    ## Calculate current Moving Average
    fastMA = sma(posisinya, fastLength)
    slowMA = sma(posisinya, slowLength)
    veryslowMA = sma(posisinya, veryslowLength)
    macd = fastMA - slowMA
    signal = hitungsignal(posisinya)
    hist = macd - signal
    

    ## If crossover, open LONG
    if hist_old < 0 :
        if hist > 0 :
            if macd > 0 :
                if fastMA > slowMA :
                    if float(ohlc['result'][tpair][posisinya - slowLength][4]) > veryslowMA :
                        ## STOP SHORT
                        if statusPosition == 1:
                            closeshort(posisinya)
                        ## CALL LONG
                        if statusPosition != 2:
                            statusPosition = 2
                            bukalong(posisinya)

    ## If crossunder, open SHORT
    if hist_old > 0 :
        if hist < 0 :
            if macd < 0 :
                if fastMA < slowMA :
                    if float(ohlc['result'][tpair][posisinya - slowLength][4]) < veryslowMA :
                        ## STOP LONG
                        if statusPosition == 2:
                            closelong(posisinya)
                        ## CALL SHORT
                        if statusPosition != 1:
                            statusPosition = 1
                            bukashort(posisinya)


                            
## Decide whatever to do Backtesting, or start trading normaly.

if testing == 0:
    berhitung(lastclose-1)
else :
    statusPosition = 0
    print('Backtest Start !!!')
    for x in range(lastclose - 200):
        cobahitung = x + 200
        berhitung(cobahitung)
        
## Give indication if all calculation are done
print("------------------------DONE------------------------")
