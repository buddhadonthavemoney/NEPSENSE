import time
import pandas as pd
import requests
import sys
import re
import os
import json
import calendar
import math
import itertools
from datetime import datetime
from dateutil.parser import parse
from itertools import cycle
from tabulate import tabulate
from colorama import Fore, Style 
from nepsense.Stock import Stock
from nepsense.data import __Data

sectors = ["devbank", "banking", "finance", "hotels", "manufacture", "others",
           "hydropower", "trading", "nonlifeinsu", "devbank"]

class NEPSE(__Data):
    def __init__(self, _list):
        super().__init__()
        self.symbol_list = _list
        self.stocks_list = self.get_stocks_info()
        self.df = pd.DataFrame(columns=["Symbol", "LTP", "change", "%change",
            "Volume", "PC", "Open", "Close", "low - high", "52 weekrange", 
            "total shares","total public", "networth"])

    def get_stocks_info(self):
        return [Stock(i) for i in self.symbol_list]


    def scrape_stocks_prices(self):
        self._start_animation_thread("retrieving prices", hasCount=True)

        _remove_stock = list()
        for i in self.stocks_list:
            x = i.get_price_info()
            self._count = self.stocks_list.index(i)+1
            if not x:
                _remove_stock.append(i)
        for _ in _remove_stock:
            self.stocks_list.remove(_)

        self._stop_animation_thread()


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
            dict_ = {
                "Symbol": i.symbol,
                "LTP": i.ltp,
                "change": i.change,
                "%change": i.change_p,
                "PC": f"{Style.RESET_ALL}{i.PC}",
                "Volume" :i.volume,
                "Open": i.Open,
                "Close": i.Close,
                "low - high": f"{i.low}-{i.high}",
                "52 weekrange": f"{i.range_l}-{i.range_h}={i.range_h-i.range_l}",
                "total shares": i.total_listed,
                "total public": i.total_public,
                "networth": i.networth,
            }

            self.df = self.df.append(dict_, ignore_index=True)
        print(tabulate(self.df.sort_values("%change"), headers="keys",
                       tablefmt='pretty', showindex=False))
        # print(tabulate(self.df.sort_values("Volume"), headers="keys",
                       # tablefmt='pretty', showindex=False))

    def get_indices(self):
        self._start_animation_thread("getting indices", hasCount=False)

        r_indices = requests.get(
                self.url_index, 
                headers=self.alt_headers
            ).json()
        r_nepse= requests.get(
                self.url_nepse, 
                headers=self.alt_headers
            ).json()

        self._stop_animation_thread()

        r_nepse = [x for x in r_nepse if x["index"] == "NEPSE Index"]
        r_indices.append(r_nepse[0])
        df = pd.DataFrame(
            columns=["index", "change", "perChange", "currentValue"])
        self.nepse_df = df.copy()
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
                self.nepse_df = self.nepse_df.append(i, ignore_index=True)
                continue
            df = df.append(x, ignore_index=True)
        self.subindices_df = df


    def display_subindices(self):
        print(tabulate(self.subindices_df.sort_values("perChange", ascending=False),
                headers="keys", tablefmt='pretty', showindex=False)
            )


    def display_nepse_index(self):
        print(tabulate(self.nepse_df.dropna(axis=1), headers="keys",
            tablefmt='pretty', showindex=False))


    def get_market_summary(self):
        self._start_animation_thread("getting market summary", hasCount=False)

        x = requests.get(self.url_market_summary, headers = self.alt_headers).json()

        self._stop_animation_thread()

        self.market_summary = dict()
        for i in x:
            self.market_summary[f"{i['detail']}"] = i['value'] 


    def print_market_summary(self):
        for key, value in self.market_summary.items():
            print(f"{key} = {value}")

    def get_top_gainers(self):
        self._start_animation_thread("getting gainers", hasCount=False)

        re = requests.get(self.url_top_gainers, headers=self.alt_headers).json()

        self._stop_animation_thread()

        self.df_gainers = pd.DataFrame(re)
        df = self.df_gainers.rename(
                {
                    'symbol': f'{Fore.BLUE}symbol', 
                    'securityName': f'securityName{Style.RESET_ALL}'
                }, 
                axis=1, 
            )
        self._print_table(
            df.filter(
                items=[f"{Fore.BLUE}symbol","ltp","pointChange", 
                    "percentageChange", f"securityName{Style.RESET_ALL}"]
            ).head(20)
        )


    def get_top_losers(self):
        self._start_animation_thread("getting losers", hasCount=False)

        re = requests.get(self.url_top_losers, headers=self.alt_headers).json()

        self._stop_animation_thread()
        self.df_losers = pd.DataFrame(re)
        df = self.df_losers.rename(
                {'symbol': f'{Fore.RED}symbol', 'securityName': f'securityName{Style.RESET_ALL}'}, 
                axis=1, 
            )
        self._print_table(
            df.filter(
                items=[f"{Fore.RED}symbol","ltp","pointChange", "percentageChange", f"securityName{Style.RESET_ALL}"]
            ).head(20)
        )

    def get_top_turnover(self):
        self._start_animation_thread("getting turnover", hasCount=False)

        re = requests.get(self.url_top_turnover, headers=self.alt_headers).json()

        self._stop_animation_thread()
        self.df_turnover = pd.DataFrame(re)
        df = self.df_turnover.rename(
                {'symbol': f'{Fore.GREEN}symbol', 'closingPrice':'LTP', 'securityName': f'securityName{Style.RESET_ALL}'}, 
                axis=1, 
            )
        self._print_table(
            df.filter(
                items=[f"{Fore.GREEN}symbol","LTP","turnover", f"securityName{Style.RESET_ALL}"]
            ).head(20)
        )

    def get_top_volume(self):
        self._start_animation_thread("getting volume", hasCount=False)

        re = requests.get(self.url_top_volume, headers=self.alt_headers).json()

        self._stop_animation_thread()
        self.df_volume = pd.DataFrame(re)
        df = self.df_volume.rename(
                {'symbol': f'{Fore.CYAN}symbol', 'closingPrice':'LTP', 'securityName': f'securityName{Style.RESET_ALL}'}, 
                axis=1, 
            )
        self._print_table(
            df.filter(
                items=[f"{Fore.CYAN}symbol","LTP","shareTraded", f"securityName{Style.RESET_ALL}"]
            ).head(20)
        )

    def get_top_supplydemand(self, supply):
        re = requests.get(self.url_top_supplydemand, headers=self.alt_headers).json()
        if supply:
            self.df_supply = pd.DataFrame(re["supplyList"])
            df = self.df_supply
            color = Fore.RED
        else:
            self.df_demand = pd.DataFrame(re["demandList"])
            df = self.df_demand
            color = Fore.BLUE

        df = df.rename(
            {'symbol': f'{color}symbol', 'securityName': f'securityName{Style.RESET_ALL}'}, 
            axis=1, 
        )
        self._print_table(
            df.filter(
                items=[f"{color}symbol","totalOrder","totalQuantity", f"securityName{Style.RESET_ALL}"]
            ).head(20)
        )

    def get_top_transactions(self):
        self._start_animation_thread("getting top transactions", hasCount=False)

        re = requests.get(self.url_top_transactions, headers=self.alt_headers).json()
        
        self._stop_animation_thread()
        self.df_transactions = pd.DataFrame(re)
        df = self.df_transactions.rename(
                {'symbol': f'{Fore.CYAN}symbol', 'lastTradedPrice':'LTP', 'securityName': f'securityName{Style.RESET_ALL}'}, 
                axis=1, 
            )
        self._print_table(
            df.filter(
                items=[f"{Fore.CYAN}symbol","LTP","totalTrades", f"securityName{Style.RESET_ALL}"]
            ).head(20)
        )

    def save_floorsheet(self, path):
        self.get_market_summary()
        total_iteration = math.ceil(self.market_summary["Total Transactions"]/500)
        table_list = list()
        data = json.dumps({"id":self.get_index()})
        a=1
        
        self._start_animation_thread("Getting Today's floorsheet data", hasCount=True)
        for _ in range(0, total_iteration):
            url_floorsheet = ("https://newweb.nepalstock.com.np/api/nots/"
                    f"nepse-data/floorsheet?page={_}"
                    "&size=500&sort=contractId,desc")
            try:
                self._count = _+1
                r = requests.post(
                        url_floorsheet,
                        headers=self.headers,
                        data = data
                    ).json()
            except:
                time.sleep(0.4)
                r = requests.post(
                        url_floorsheet,
                        headers=self.headers,
                        data = data
                    ).json()
            try:
                floorsheet = r["floorsheets"]["content"]
            except:
                self._stop_animation_thread()
                print(("\nPlease change the index with -ci flag. "
                        "\nCheck https://github.com/buddha231/NEPSENSE for more info"))
                return

            for x in floorsheet:
                _time = parse(x["tradeTime"])
                tradeTime = _time.strftime("%H:%M:%S")
                dict_ = { 
                    "S.N.": a,
                    "contractId": x["contractId"],
                    "Symbol": x["stockSymbol"],
                    "Buyer": x["buyerMemberId"],
                    "Seller":x["sellerMemberId"],
                    "Quantity":x["contractQuantity"],
                    "Rate":x["contractRate"],
                    "Amount": x["contractAmount"],
                    "Time": tradeTime,
                    
                }
                a+=1
                table_list.append(dict_)
        self._stop_animation_thread()

        df = pd.DataFrame(table_list)
        date = datetime.now()
        weekday = calendar.day_name[date.weekday()]
        self.floorsheet = df
        filename = f"floorsheet_{date.date()}_{weekday}.csv"
        df.to_csv(f"{path}/{filename}", index=False)
        print(f"{filename} saved to {path}")

        # print(tabulate(df, headers="keys", tablefmt='pretty', showindex=False))

