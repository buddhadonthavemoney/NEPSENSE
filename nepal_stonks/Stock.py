import time
import pandas as pd
import requests
import sys
import re
import os
import json
import calendar
import math
from datetime import datetime
from itertools import cycle
from tabulate import tabulate
from colorama import Fore, Style 
from nepal_stonks.data import __Data

sectors = ["devbank", "banking", "finance", "hotels", "manufacture", "others",
           "hydropower", "trading", "nonlifeinsu", "devbank"]


class Stock(__Data):
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol.upper()
        self.df = pd.read_csv("company_list.csv")
        self.c_id, self.sector, self.name = self.get_basic_info()
        self.url_company = ("https://newweb.nepalstock.com.np/api/nots/"
                f"security/{self.c_id}")
        self.url_marketdepth = ("https://newweb.nepalstock.com.np/api/nots/"
                f"nepse-data/marketdepth/{self.c_id}")
        self.today_price = ("https://newweb.nepalstock.com.np/api/nots/"
                "nepse-data/today-price?&size=500&businessDate=2021-06-23")

    def __repr__(self):
        return f"{self.symbol}: {self.name}"


    def get_basic_info(self):
        symbol = self.symbol.upper()
        condition = self.df["symbol"] == symbol
        c_name = re.sub(
                r'[0-9]', "", 
                self.df[condition].company_name.to_string()
            ).strip()
        c_sector = re.sub(
                r'[0-9]', "", 
                self.df[condition].sector_name.to_string()
            ).strip()
        _x = self.df[condition].company_id.to_string()
        c_id = _x.split(" ")[4]
        return c_id, c_sector, c_name

    def get_price_info(self):
        data = json.dumps({"id":int(self.get_index())})
        try:
            self.headers['user-agent'] = self.get_user_agent()
            x = requests.post(
                    self.url_company, 
                    headers=self.headers, 
                    data=data
                ).json()
        except:
            time.sleep(0.4)
            self.headers['user-agent'] = self.get_user_agent()
            x = requests.post(
                    self.url_company,
                    headers=self.headers,
                    data=data
                ).json()

        try:
            detail = x["securityDailyTradeDto"]
        except:
            print("Please change the index with -ci flag.")
            sys.exit()
            return
        self.ltp = detail["lastTradedPrice"]
        self.Open = detail["openPrice"]
        self.PC = detail["previousClose"]
        self.Close = detail["closePrice"]
        self.high = detail['highPrice']
        self.low = detail['lowPrice']
        self.range_h = detail["fiftyTwoWeekHigh"]
        self.range_l = detail["fiftyTwoWeekLow"]
        self.volume = detail["totalTradeQuantity"]
        self.networth = x['security']['networthBasePrice']
        self.total_listed = x["publicShares"] + x["promoterShares"]
        self.total_public = x["publicShares"]
        try:
            self.change = round(self.ltp-self.PC, 2)
            self.change_p = round((self.change)/self.PC*100, 2)
        except:
            print((f"{self.symbol} - {self.c_id} might be in merger or "
                "renamed to other company"))
            self.change = 0
            self.change_p = 0
            return False
        return True
    
    def get_market_depth(self):
        response = requests.get(self.url_marketdepth, headers=self.alt_headers)
        self.market_depth = response.json()
        df_buy = pd.DataFrame()
        df_sell = pd.DataFrame()
        _buy = list()
        for x in self.market_depth["marketDepth"]["buyMarketDepthList"]:
            a={
                f"{Fore.BLUE}Buy orders": x["orderCount"],
                "Buy Quantity": x["quantity"],
                f"Buy Price{Style.RESET_ALL}" : x["orderBookOrderPrice"]
            }
            _buy.append(a)
        self.df_buy=df_buy.append(_buy, ignore_index=False)

        _sell = list()
        for x in self.market_depth["marketDepth"]["sellMarketDepthList"]:
            a={
                f"{Fore.RED}Sell orders": x["orderCount"],
                "Sell Quantity": x["quantity"],
                f"Sell Price{Style.RESET_ALL}" : x["orderBookOrderPrice"]
            }
            _sell.append(a)
        self.df_sell=df_sell.append(_sell, ignore_index=False)
        print(tabulate(self.df_buy, headers="keys",
                       tablefmt='pretty', showindex=False))
        total_buy = self.market_depth["totalBuyQty"]
        print(f"total_buy = {total_buy}")

        print(tabulate(self.df_sell, headers="keys",
                       tablefmt='pretty', showindex=False))
        total_sell = self.market_depth["totalSellQty"]
        print(f"total_sell = {total_sell}")


