#!/usr/bin/env python3
import sys
import argparse
sys.path.append("/home/buddha/Code/python/webautomation/nepse_floorsheet/NEPSE")
from Stock import NEPSE, Stock
from hi import get_stocks
import argparse


def main():
    parse = argparse.ArgumentParser(description = "STONK", prog="priceof")
    parse.add_argument(
            '-c' , '--company', metavar='', 
            help="symbols of companies", nargs='*'
        )
    parse.add_argument(
            '-f', '--floorsheet', action='store_true',
            help = "get floorsheet"
        )
    parse.add_argument(
            '-n', '--nepse',  action='store_true',
            help="save NEPSE index"
        )
    parse.add_argument(
            '-s', '--sub_indices', action='store_true', 
            help = "get subindices" 
        )
    parse.add_argument(
            '-m', '--market_depth', 
            help = "get subindices", metavar=''
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
            help="custom list in hi.py"
        )
    args = parse.parse_args()
    comp_list = args.company

    if comp_list:
        stocks = NEPSE(args.company)
        stocks.scrape_stocks_prices()
        stocks.print_stocks_prices()

    if args.nepse:
        stocks = NEPSE([])
        stocks.get_subindices()

    if args.sub_indices:
        stocks = NEPSE([])
        stocks.get_subindices()

    if args.market_depth:
        stock = Stock(args.market_depth)
        stock.get_market_depth()

    if args.get_detail:
        stock = Stock(args.get_detail)
        c_id, sector, name = stock.get_basic_info()
        print(f" id ={c_id}, \n sector = {sector}, \n company_name = {name}")

    if args.custom:
        stocks = NEPSE(get_stocks(args.custom))
        stocks.scrape_stocks_prices()
        stocks.print_stocks_prices()

    if args.floorsheet:
        stocks = NEPSE([])
        stocks.save_floorsheet()

    if args.market_summary:
        stocks = NEPSE([])
        stocks.get_market_summary()


if __name__ == "__main__":
    main()
