import sys
import argparse
from nepal_stonks.Stock import Stock
from nepal_stonks.Nepse import NEPSE 
import argparse
import pathlib
import os

def main():
    parse = argparse.ArgumentParser(
            description = "STONK, complete NEPSE solution in command line", 
            prog="priceof"
        )
    parse.add_argument(
            '-c' , '--company', metavar='', 
            help="symbols of companies seperated by space", nargs='*'
        )
    parse.add_argument(
            '-f', '--floorsheet', action='store_true',
            help = "get floorsheet"
        )
    parse.add_argument(
            '-n', '--nepse',  action='store_true',
            help="get NEPSE index"
        )
    parse.add_argument(
            '-s', '--sub-indices',  action='store_true',
            help="get subindices"
        )
    parse.add_argument(
            '-m', '--market_depth', 
            help = "get market depth of the company(enter symbol)", metavar='',

        )
    parse.add_argument(
            '-ms', '--market_summary', 
            help = "get market summary", action='store_true' 
        )
    parse.add_argument(
            '-d', '--get_detail', metavar='', 
            help = "get the non price related detail of the company"
        )
    parse.add_argument(
            '-cu', '--custom', metavar='', 
            help="custom list in data.py"
        )
    parse.add_argument(
            '-ci', '--change_index', metavar='',
            help="change the value of id sent as a payload in the post request"
        )
    parse.add_argument(
            '--losers', action='store_true',
            help="get the top losers"
        )
    parse.add_argument(
            '--gainers', action='store_true',
            help="get the top gainers"
        )
    parse.add_argument(
            '--supply', action='store_true',
            help="get the scripts with maximum supply"
        )
    parse.add_argument(
            '--demand', action='store_true',
            help="get the scripts with maximum demand"
        )
    parse.add_argument(
            '--turnover', action='store_true',
            help="get the scripts with maximum turnover"
        )

    parse.add_argument(
            '--volume', action='store_true',
            help="get the scripts with maximum volume"
        )
    parse.add_argument(
            '--transactions', action='store_true',
            help="get the scripts with maximum transactions"
        )

    args = parse.parse_args()

    comp_list = args.company
    if comp_list:
        stocks = NEPSE(args.company)
        stocks.scrape_stocks_prices()
        stocks.print_stocks_prices()

    if args.nepse:
        stocks = NEPSE([])
        stocks.get_indices()
        stocks.display_nepse_index()

    if args.sub_indices:
        if args.nepse:
            stocks.display_nepse_index()
        else:
            stocks = NEPSE([])
            stocks.get_indices()
            stocks.display_subindices()

    market_depth = args.market_depth
    if market_depth:
        stock = Stock(market_depth)
        stock.get_market_depth()

    if args.get_detail:
        stock = Stock(args.get_detail)
        c_id, sector, name = stock.get_basic_info()
        print(f" id ={c_id}, \n sector = {sector}, \n company_name = {name}")

    if args.custom:
        __ = NEPSE([])
        stocks = NEPSE(__.get_stocks(args.custom))
        stocks.scrape_stocks_prices()
        stocks.print_stocks_prices()

    if args.floorsheet:
        stocks = NEPSE([])
        stocks.save_floorsheet()

    if args.market_summary:
        stocks = NEPSE([])
        stocks.get_market_summary()

    if args.change_index:
        stocks = NEPSE([])
        stocks.change_index(args.change_index)

    if args.gainers:
        stocks = NEPSE([])
        stocks.get_top_gainers()

    if args.losers:
        stocks = NEPSE([])
        stocks.get_top_losers()

    if args.turnover:
        stocks = NEPSE([])
        stocks.get_top_turnover()

    if args.volume:
        stocks = NEPSE([])
        stocks.get_top_volume()

    if args.transactions:
        stocks = NEPSE([])
        stocks.get_top_transactions()

    if args.supply:
        stocks = NEPSE([])
        stocks.get_top_supplydemand(supply=True)

    if args.demand:
        stocks = NEPSE([])
        stocks.get_top_supplydemand(supply=False)

if __name__ == "__main__":
    main()
