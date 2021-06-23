# STONK

## Installation
```console
pip install nepal_stonks
````
After the installation you can use the cli application with the priceof command

## Usage
```console
usage: priceof [-h] [-c [...]] [-f] [-n] [-s] [-m] [-ms] [-d] [-cu] [-ci] [--losers]
               [--gainers] [--supply] [--demand] [--turnover] [--volume] [--transactions]

optional arguments:
  -h, --help            show this help message and exit
  -c [ ...], --company [ ...]
                        symbols of companies
  -f, --floorsheet      get floorsheet
  -n, --nepse           save NEPSE index
  -s, --sub_indices     get subindices
  -m , --market_depth   get subindices
  -ms, --market_summary
                        get market summary
  -d , --get_detail     get the non price related detail of the company
  -cu , --custom        custom list in hi.py
  -ci , --change_index 
                        change the value of id sent as a payload in the post request
  --losers              get the top losers
  --gainers             get the top gainers
  --supply              get the shares with maximum supply
  --demand              get the share with maximum demand
  --turnover            get the shares with maximum turnover
  --volume              get the shares with maximum volume
  --transactions        get the shares with maximum transactions
  ```
