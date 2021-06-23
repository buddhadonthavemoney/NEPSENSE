# STONK

## Installation
```console
pip install nepal_stonks
````
After the installation you can use the cli application with the priceof command

## Usage
```console
usage: priceof [-h] [-c [...]] [-f] [-n] [-m] [-ms] [-d] [-cu] [-ci]
               [--losers] [--gainers] [--supply] [--demand] [--turnover]
               [--volume] [--transactions]

STONK, complete NEPSE solution in command line

optional arguments:
  -h, --help            show this help message and exit
  -c [ ...], --company [ ...]
                        symbols of companies seperated by space
  -f, --floorsheet      get floorsheet
  -n, --nepse           get NEPSE index and subindices
  -m , --market_depth   get market depth of the company(enter symbol)
  -ms, --market_summary get market summary
  -d , --get_detail     get the non price related detail of the company
  -cu , --custom        custom list in data.py
  -ci , --change_index  change the value of id sent as a payload in the post
                        request
  --losers              get the top losers
  --gainers             get the top gainers
  --supply              get the scripts with maximum supply
  --demand              get the scripts with maximum demand
  --turnover            get the scripts with maximum turnover
  --volume              get the scripts with maximum volume
  --transactions        get the scripts with maximum transactions
  ```

