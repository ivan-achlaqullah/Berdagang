# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 16:36:27 2017

@author: Ivan Achlaqullah
"""

## Berdagang.py, Cryptocurrency Trading Bot with Automatic Tweet Support##
## Made by Ivan Achlaqullah

import time
import krakenex

## Import another script
import config    ## Skrip pengaturan
import ngetweet  ## Skrip integrasi twitter

## Import trading strategy
import strategy.smamacd as strategy

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

    global statusPosition
    statusPosition = 0

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

    global statusPosition
    statusPosition = 0

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

    global statusPosition
    if statusPosition == 1:
        closeshort(posisinya)

    print (str(ohlc['result'][tpair][posisinya][0]) + " " + str(posisinya) +
           " OPEN Long, Price : " + ohlc['result'][tpair][posisinya][4])

    global testing
    global balance
    global leverage

    if testing == 0:
        ngetweet.tweet(str(ohlc['result'][tpair][posisinya][0]) + " " + str(posisinya) +
               " OPEN Long, Price : " + ohlc['result'][tpair][posisinya][4])

        ticker = k.query_public('Ticker', req = {'pair': tpair})

        while True:
            harga = (balance * 0.95 * leverage) / float(ticker['result'][tpair]['c'][0])
            beli = k.query_private('AddOrder',
                            {'pair': tpair,
                             'type': 'buy',
                             'ordertype': 'market',
                             'volume': str(harga),
                             'leverage': str(leverage)})
            time.sleep(1)
            if len(beli['error']) == 0:
                break

    statusPosition = 2

def bukashort(posisinya) :

    global statusPosition
    if statusPosition == 2:
        closelong(posisinya)

    print (str(ohlc['result'][tpair][posisinya][0]) + " " + str(posisinya) +
           " OPEN Short, Price : " + ohlc['result'][tpair][posisinya][4])

    global testing
    global balance
    global leverage

    if testing == 0:
        ngetweet.tweet(str(ohlc['result'][tpair][posisinya][0]) + " " + str(posisinya) +
               " OPEN Short, Price : " + ohlc['result'][tpair][posisinya][4])

        ticker = k.query_public('Ticker', req = {'pair': tpair})

        while True:
            harga = (balance * 0.95 * leverage) / float(ticker['result'][tpair]['c'][0])
            beli = k.query_private('AddOrder',
                            {'pair': tpair,
                             'type': 'sell',
                             'ordertype': 'market',
                             'volume': str(harga),
                             'leverage': str(leverage)})
            time.sleep(1)
            if len(beli['error']) == 0:
                break

    statusPosition = 1

## Act based on strategy result
def decide(order, pos):

    global statusPosition

    if order == 'long':
        if statusPosition != 2:
            bukalong(pos)
    elif order == 'short':
        if statusPosition != 1:
            bukashort(pos)

## Decide whatever to do Backtesting, or start trading normaly.

if testing == 0:
    order1 = strategy.calculate(lastclose-1, tpair, ohlc)
    decide(order1, lastclose-1)
else :
    statusPosition = 0
    print('Backtest Start !!!')
    for x in range(lastclose - 200):
        cobahitung = x + 200
        order1 = strategy.calculate(cobahitung, tpair, ohlc)
        decide(order1, cobahitung)

## Give indication if all calculation are done
print("------------------------DONE------------------------")
