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
sys.path.append("/home/buddha/Code/python/webautomation/nepse_floorsheet")
from hi import get_user_agent, get_stocks


sectors = ["devbank", "banking", "finance", "hotels", "manufacture", "others",
           "hydropower", "trading", "nonlifeinsu", "devbank"]
os.chdir("/home/buddha/Code/python/webautomation/nepse_floorsheet")


class Stock:
    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.df = pd.read_csv("datas/company_list.csv")
        self.c_id, self.sector, self.name = self.get_basic_info()
        self.is_company = True
        self.url_company = ("https://newweb.nepalstock.com.np/api/nots/"
                f"security/{self.c_id}")
        self.url_marketdepth = ("https://newweb.nepalstock.com.np/api/nots/"
                f"nepse-data/marketdepth/{self.c_id}")
        self.headers = {
             'Host': 'newweb.nepalstock.com.np',
             'User-Agent': get_user_agent(),
             'Accept': 'application/json, text/plain, */*',
             'Accept-Language': 'en-US,en;q=0.5',
             'Accept-Encoding': 'gzip, deflate, br',
             'Content-Type': 'application/json',
             'Content-Length': '10',
             'Origin': 'https://newweb.nepalstock.com.np',
             'Connection': 'keep-alive',
             'Referer': 'https://newweb.nepalstock.com.np/company/detail/131',
             'TE': 'Trailers'
             }

        self.alt_headers = {
            "Host": "newweb.nepalstock.com.np",
            "User-Agent" : get_user_agent(),
            "Accept" : "application/json, text/plain, */*",
            "Accept-Language" : "en-US,en;q=0.5",
            "Accept-Encoding" : "gzip, deflate, br",
            "Connection" : "keep-alive",
            "Referer" : "https://newweb.nepalstock.com.np/",
        }

    def __repr__(self):
        return self.symbol

    def get_basic_info(self):
        symbol = self.symbol.upper()
        condition = self.df["symbol"] == symbol
        c_name = re.sub(r'[0-9]', "", self.df[condition].company_name.to_string()).\
            strip()
        c_sector = re.sub(r'[0-9]', "", self.df[condition].sector_name.to_string()).\
            strip()
        x = self.df[condition].company_id.to_string()
        c_id = x.split(" ")[4]
        return c_id, c_sector, c_name

    def get_price_info(self, headers):
        data = json.dumps({"id":765})
        try:
            headers['user-agent'] = get_user_agent()
            x = requests.post(self.url_company, headers=headers, data=data).json()
        except:
            time.sleep(0.4)
            headers['user-agent'] = get_user_agent()
            x = requests.post(self.url_company, headers=headers, data=data).json()

        if self.is_company:
            detail = x["securityDailyTradeDto"]
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
        else:
            pass

        try:
            self.change = round(self.ltp-self.PC, 2)
            self.change_p = round((self.change)/self.PC*100, 1)
        except:
            print(f"{self.symbol} - {self.c_id} might be in merger or renamed to other company")
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


class NEPSE:
    def __init__(self, _list):
        self.headers = {
             'Host': 'newweb.nepalstock.com.np',
             'User-Agent': get_user_agent(),
             'Accept': 'application/json, text/plain, */*',
             'Accept-Language': 'en-US,en;q=0.5',
             'Accept-Encoding': 'gzip, deflate, br',
             'Content-Type': 'application/json',
             'Content-Length': '10',
             'Origin': 'https://newweb.nepalstock.com.np',
             'Connection': 'keep-alive',
             'Referer': 'https://newweb.nepalstock.com.np/company/detail/131',
             'TE': 'Trailers'
             }
        self.alt_headers = {
            "Host": "newweb.nepalstock.com.np",
            "User-Agent" : get_user_agent(),
            "Accept" : "application/json, text/plain, */*",
            "Accept-Language" : "en-US,en;q=0.5",
            "Accept-Encoding" : "gzip, deflate, br",
            "Connection" : "keep-alive",
            "Referer" : "https://newweb.nepalstock.com.np/",
        }
        self.url_index = "https://newweb.nepalstock.com.np/api/nots"
        self.url_nepse = "https://newweb.nepalstock.com.np/api/nots/nepse-index"
        self.url_market_summary = ("https://newweb.nepalstock.com.np/api/"
        "nots/market-summary/")
        self.symbol_list = _list
        self.stocks_list = self.get_stocks_info()
        self.df = pd.DataFrame(columns=["Symbol", "LTP", "change", "%change",
            "Volume", "PC", "Open", "Close", "low - high", "52 weekrange", 
            "total shares","total public", "networth"])

    def get_stocks_info(self):
        return [Stock(i) for i in self.symbol_list]

    def scrape_stocks_prices(self):
        _remove_stock = list()
        for i in self.stocks_list:
            print(f"{self.stocks_list.index(i)+1}", end="\r")
            x = i.get_price_info(self.headers)
            if not x:
                _remove_stock.append(i)
        for _ in _remove_stock:
            self.stocks_list.remove(_)


    def _print_table(self, df):
        print(tabulate(df, headers="keys",
                       tablefmt='pretty', showindex=False))
    
    def print_stocks_prices(self):
        # self.scrape_stocks_prices()
        if len(self.stocks_list)==0: return
        for i in self.stocks_list:
            if i.change < 0:
                i.ltp = f"{i.ltp}{Fore.RED}"
            elif i.change > 0:
                i.ltp = f"{i.ltp}{Fore.GREEN}"
            else:
                pass
            if i.is_company:
                dict_ = {
                    "Symbol": i.symbol,
                    "LTP": i.ltp,
                    "change": i.change,
                    "%change": i.change_p,
                    "Volume" :f"{Style.RESET_ALL}{i.volume}",
                    "PC": i.PC,
                    "Open": i.Open,
                    "Close": i.Close,
                    "low - high": f"{i.low}-{i.high}",
                    "52 weekrange": f"{i.range_l}-{i.range_h}={i.range_h-i.range_l}",
                    "total shares": i.total_listed,
                    "total public": i.total_public,
                    "networth": i.networth,
                }
            else:
                dict_ = {
                    "Symbol": i.symbol,
                    "LTP": i.ltp,
                    "change": i.change,
                    "%change": i.change_p,
                    "PC": f"{Style.RESET_ALL}{i.PC}",
                    "Close": i.Close,
                    "low - high": f"{i.low}-{i.high}",
                    "52 weekrange": f"{i.range_l}-{i.range_h}={i.range_h-i.range_l}",
                }

            self.df = self.df.append(dict_, ignore_index=True)
        print(tabulate(self.df.sort_values("%change"), headers="keys",
                       tablefmt='pretty', showindex=False))
        # print(tabulate(self.df.sort_values("public"), headers="keys",
                       # tablefmt='pretty', showindex=False))
        print(f"total trading scripts: {len(self.stocks_list)}")

    def get_subindices(self):
        r_indices = requests.get(self.url_index, headers=self.alt_headers).json()
        r_nepse= requests.get(self.url_nepse, headers=self.alt_headers).json()[3]
        r_indices.append(r_nepse)
        df = pd.DataFrame(
            columns=["index", "change", "perChange", "currentValue"])
        copy_df = df.copy()
        for i in r_indices:
            x = dict()
            x["perChange"] = i["perChange"]
            x["change"] = i["change"]
            if i["change"] < 0:
                x["index"] = str(i["index"]) + f"{Fore.RED}"
                x["currentValue"] = f"{Style.RESET_ALL}" + \
                    str(i["currentValue"])
            if i["change"] > 0:
                x["index"] = str(i["index"]) + f"{Fore.GREEN}"
                x["currentValue"] = f"{Style.RESET_ALL}" + \
                    str(i["currentValue"])

            if i["index"] == "NEPSE Index":
                i["change"] = x["change"]
                i["index"] = x["index"]
                i["currentValue"] = x["currentValue"]
                copy_df = copy_df.append(i, ignore_index=True)
                continue
            df = df.append(x, ignore_index=True)
        #for nepse
        x = requests.get(self.url_nepse, headers=self.alt_headers).json()
        
        # print(df["index"])
        print(tabulate(df.sort_values("perChange", ascending=False),
                headers="keys", tablefmt='pretty', showindex=False)
            )

        print(tabulate(copy_df.dropna(axis=1), headers="keys",
            tablefmt='pretty', showindex=False))


    def get_market_summary(self):
        x = requests.get(self.url_market_summary, headers = self.alt_headers).json()
        self.market_summary = dict()
        for i in x:
            self.market_summary[f"{i['detail']}"] = i['value'] 
            print(f"{i['detail']} = {i['value']}")

    def __get_total_transaction(self):
        pass

    def save_floorsheet(self):
        self.get_market_summary()
        columns = ['S.N.','Symbol', 'Buyer',
                   'Seller', 'Quantity', 'Rate', 'Amount']
        total_iteration = math.ceil(self.market_summary["Total Transactions"]/500)
        table_list = list()
        data = json.dumps({"id":765})
        for _ in range(0, total_iteration):
            url_floorsheet = ("https://newweb.nepalstock.com.np/api/nots/nepse-data"
                f"/floorsheet?page={_}&size=500&sort=contractId,desc")
            try:
                print(f"{_+1}", end = "\r")
                r = requests.post(url_floorsheet, headers=self.headers, data = data).json()
            except:
                time.sleep(0.4)
                r = requests.post(url_floorsheet, headers=self.headers, data = data).json()
            floorsheet = r["floorsheets"]["content"]
            for x in floorsheet:
                dict_ = { 
                    "S.N.": _+1,
                    "Symbol": x["stockSymbol"],
                    "Buyer": x["buyerMemberId"],
                    "Seller":x["sellerMemberId"],
                    "Quantity":x["contractQuantity"],
                    "Rate":x["contractRate"],
                    "Amount": x["contractAmount"],
                    }
                table_list.append(dict_)
        df = pd.DataFrame(table_list, columns=columns)
        date = datetime.now()
        weekday = calendar.day_name[date.weekday()]
        self.floorsheet = df
        df.to_csv(f"/home/buddha/Code/python/webautomation/nepse_floorsheet/datas/floorsheet_{date.date()}_{weekday}.csv")

        # print(tabulate(df, headers="keys", tablefmt='pretty', showindex=False))

