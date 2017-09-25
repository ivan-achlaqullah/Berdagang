# -*- coding: utf-8 -*-
"""
Created on Thu Sep 21 17:18:46 2017

@author: Ivan Achlaqullah

CONFIG FILE FOR THE BOT
"""

testing = 1
## Config value for testing :
## 0 = Send Trade Order to Kraken, and when it does, tweet it.
## 1 = Backtest using OHLC provided from Kraken

pair = 'XBTUSD' # Trading Pair name, full list: https://www.kraken.com/help/fees
chart_interval = '60' ## Interval in minutes

leverage = 5