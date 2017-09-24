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
leverage = 5
balance = 0.0

## Cek isi ballance
def cekdompet():
    dompet = k.query_private('TradeBalance')
    global balance
    balance = float(dompet['result']['eb'])
    #print('Balance : ' + str(balance))
    time.sleep(2)
    
cekdompet()

## Cek chart ETH/USD 15 Menit
ohlc = k.query_public('OHLC', req = {'pair': 'ETHUSD', 'interval': '15'})
time.sleep(2)
#print(ohlc)

## Cek posisi terakhir dari data yang didapat
lastclose = len(ohlc['result']['XETHZUSD'])
lastclose = lastclose - 1
#print(lastclose)

## Cek posisi apakah ada open position
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

## Fungsi buat CLOSE position

def closelong(posisinya) :
    print(str(ohlc['result']['XETHZUSD'][posisinya][0]) + " " + str(posisinya) + 
          " STOP Long : " + ohlc['result']['XETHZUSD'][posisinya][4])

    global testing
    if testing == 0:
        ngetweet.tweet(str(ohlc['result']['XETHZUSD'][posisinya][0]) + " " + str(posisinya) + 
              " STOP Long : " + ohlc['result']['XETHZUSD'][posisinya][4])
        
        while True:
            beli = k.query_private('AddOrder',
                            {'pair': 'ETHUSD',
                             'type': 'sell',
                             'ordertype': 'market',
                             'volume': '0',
                             'leverage': str(leverage)})
            time.sleep(2)
            if len(beli['error']) == 0:
                break
        
        cekdompet()
        
def closeshort(posisinya) :
    print(str(ohlc['result']['XETHZUSD'][posisinya][0]) + " " + str(posisinya) + 
          " STOP Short : " + ohlc['result']['XETHZUSD'][posisinya][4])

    global testing
    if testing == 0:
        ngetweet.tweet(str(ohlc['result']['XETHZUSD'][posisinya][0]) + " " + str(posisinya) + 
              " STOP Short : " + ohlc['result']['XETHZUSD'][posisinya][4])
    
        while True:
            beli = k.query_private('AddOrder',
                            {'pair': 'ETHUSD',
                             'type': 'buy',
                             'ordertype': 'market',
                             'volume': '0',
                             'leverage': str(leverage)})
            time.sleep(2)
            if len(beli['error']) == 0:
                break

        cekdompet()
        
## Fungsi buat OPEN position
        
def bukalong(posisinya) :
    print (str(ohlc['result']['XETHZUSD'][posisinya][0]) + " " + str(posisinya) +
           " OPEN Long, Price : " + ohlc['result']['XETHZUSD'][posisinya][4])

    global testing
    global balance
    global leverage
    
    if testing == 0:
        ngetweet.tweet(str(ohlc['result']['XETHZUSD'][posisinya][0]) + " " + str(posisinya) +
               " OPEN Long, Price : " + ohlc['result']['XETHZUSD'][posisinya][4])
        
        while True:
            harga = (balance * 0.95 * leverage) / float(ohlc['result']['XETHZUSD'][posisinya][4])
            beli = k.query_private('AddOrder',
                            {'pair': 'ETHUSD',
                             'type': 'buy',
                             'ordertype': 'market',
                             'volume': str(harga),
                             'leverage': str(leverage)})
            time.sleep(1)
            if len(beli['error']) == 0:
                break

def bukashort(posisinya) :
    print (str(ohlc['result']['XETHZUSD'][posisinya][0]) + " " + str(posisinya) +
           " OPEN Short, Price : " + ohlc['result']['XETHZUSD'][posisinya][4])
    
    global testing
    global balance
    global leverage
    
    if testing == 0:
        ngetweet.tweet(str(ohlc['result']['XETHZUSD'][posisinya][0]) + " " + str(posisinya) +
               " OPEN Short, Price : " + ohlc['result']['XETHZUSD'][posisinya][4])
        
        while True:
            harga = (balance * 0.95 * leverage) / float(ohlc['result']['XETHZUSD'][posisinya][4])
            beli = k.query_private('AddOrder',
                            {'pair': 'ETHUSD',
                             'type': 'sell',
                             'ordertype': 'market',
                             'volume': str(harga),
                             'leverage': str(leverage)})
            time.sleep(1)
            if len(beli['error']) == 0:
                break

#### Strategy Start HERE ####

## definisikan seberapa lama length untuk menghitung MACD
fastLength = 12
slowLength = 26
signalLength = 9
veryslowLength = 200


## Buat fungsi untuk menghitung SMA
def sma(posisi,banyak):
    tetsx = 0
    for x in range(banyak):
        tetsx = tetsx + float(ohlc['result']['XETHZUSD'][posisi - x][4])
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
    
    ## Sekarang hitung Moving Averagenya SEBELUM
    fastMA = sma(posisinya-1, fastLength)
    slowMA = sma(posisinya-1, slowLength)
    veryslowMA = sma(posisinya-1, veryslowLength)
    macd = fastMA - slowMA
    signal = hitungsignal(posisinya-1)
    hist_old = macd - signal

    ## Sekarang hitung Moving Averagenya SESUDAH
    fastMA = sma(posisinya, fastLength)
    slowMA = sma(posisinya, slowLength)
    veryslowMA = sma(posisinya, veryslowLength)
    macd = fastMA - slowMA
    signal = hitungsignal(posisinya)
    hist = macd - signal
    

    ## Cek apakah crossover, buka posisi Long
    if hist_old < 0 :
        if hist > 0 :
            if macd > 0 :
                if fastMA > slowMA :
                    if float(ohlc['result']['XETHZUSD'][posisinya - slowLength][4]) > veryslowMA :
                        ## STOP SHORT
                        if statusPosition == 1:
                            closeshort(posisinya)
                        ## CALL LONG
                        if statusPosition != 2:
                            statusPosition = 2
                            bukalong(posisinya)

    ## Cek apakah crossunder, buka posisi short
    if hist_old > 0 :
        if hist < 0 :
            if macd < 0 :
                if fastMA < slowMA :
                    if float(ohlc['result']['XETHZUSD'][posisinya - slowLength][4]) < veryslowMA :
                        ## STOP LONG
                        if statusPosition == 2:
                            closelong(posisinya)
                        ## CALL SHORT
                        if statusPosition != 1:
                            statusPosition = 1
                            bukashort(posisinya)


                            
## Buat cek, jika testing maka akan jalan ratusan kali
## Jika tidak, maka akan jalan sekali + eksekusi order

if testing == 0:
    berhitung(lastclose-1) ## Jika bukan test
else :
    statusPosition = 0 ## Jika sedang test
    print('Backtest Start !!!')
    for x in range(lastclose - 200):
        cobahitung = x + 200
        berhitung(cobahitung)
        
## Berikan tanda bahwa perhitungan sudah selesai
print("------------------------DONE------------------------")
