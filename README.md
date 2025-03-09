# NEPSENSE

A cli application for most of your basic NEPSE usecases. This tool provides a simpler interface to the [NepseUnofficialApi](https://github.com/basic-bgnr/NepseUnofficialApi) with formatted output.


## Installation

### Prerequisites
First, install nepse-cli which is required for data fetching:
```bash
pip install nepse-cli
```

### Install from Source
```bash
git clone https://github.com/buddhathapa12/NEPSENSE.git
cd NEPSENSE
pip install -e .
```

After installation, the `priceof` command will be available in your terminal.

## Usage

### Stock Price Lookup
```console
$ priceof NABIL         
+--------+--------+--------+---------+--------+--------+--------+--------+---------------+------------+                                                                                         
| Symbol | LTP    | change | %change | Open   | High   | Low    | Volume | Turnover      | Prev Close |
+--------+--------+--------+---------+--------+--------+--------+--------+---------------+------------+
| NABIL  | 495.00 | -3.10  | -0.62%  | 498.00 | 502.00 | 493.00 | 53,038 | 26,253,810.00 | 498.10     |
+--------+--------+--------+---------+--------+--------+--------+--------+---------------+------------+

$ priceof NABIL NBL ADBL
+--------+--------+--------+---------+--------+--------+--------+--------+---------------+------------+                                                                                         
| Symbol | LTP    | change | %change | Open   | High   | Low    | Volume | Turnover      | Prev Close |
+--------+--------+--------+---------+--------+--------+--------+--------+---------------+------------+
| NABIL  | 495.00 | -3.10  | -0.62%  | 498.00 | 502.00 | 493.00 | 53,038 | 26,253,810.00 | 498.10     |
| NBL    | 260.00 | -1.20  | -0.46%  | 260.00 | 275.00 | 257.10 | 66,079 | 17,180,540.00 | 261.20     |
| ADBL   | 297.00 | -4.00  | -1.33%  | 300.00 | 305.00 | 296.00 | 24,088 | 7,154,136.00  | 301.00     |
+--------+--------+--------+---------+--------+--------+--------+--------+---------------+------------+
```

### Company Details
```console
$ priceof -d NABIL         
                                                                                                                                                                                                
Company Information
+--------+--------------------+------------------+--------+--------+---------+-----------------+---------------+----------+------------+
| Symbol | Name               | Sector           | LTP    | Change | %Change | Market Cap      | Listed Shares | Public % | Promoter % |
+--------+--------------------+------------------+--------+--------+---------+-----------------+---------------+----------+------------+
| NABIL  | Nabil Bank Limited | Commercial Banks | 495.00 | -3.10  | -0.62%  | 133,932,142,080 | 270,569,984   | 41.56%   | 58.44%     |
+--------+--------------------+------------------+--------+--------+---------+-----------------+---------------+----------+------------+

$ priceof -d NABIL NBL ADBL
                                                                                                                                                                                                
Company Information
+--------+---------------------------------------+------------------+--------+--------+---------+-----------------+---------------+----------+------------+
| Symbol | Name                                  | Sector           | LTP    | Change | %Change | Market Cap      | Listed Shares | Public % | Promoter % |
+--------+---------------------------------------+------------------+--------+--------+---------+-----------------+---------------+----------+------------+
| NABIL  | Nabil Bank Limited                    | Commercial Banks | 495.00 | -3.10  | -0.62%  | 133,932,142,080 | 270,569,984   | 41.56%   | 58.44%     |
| NBL    | Nepal Bank Limited                    | Commercial Banks | 260.00 | -1.20  | -0.46%  | 38,204,459,800  | 146,940,230   | 49.00%   | 51.00%     |
| ADBL   | Agricultural Development Bank Limited | Commercial Banks | 297.00 | -4.00  | -1.33%  | 41,150,016,468  | 138,552,244   | 49.00%   | 51.00%     |
+--------+---------------------------------------+------------------+--------+--------+---------+-----------------+---------------+----------+------------+
```

### Market Data
```console
$ priceof -n           # NEPSE index
     
+-------+--------------+---------------------+---------------------+----------+----------+---------------+
| index | currentValue | change              | perChange           | high     | low      | previousClose |
+-------+--------------+---------------------+---------------------+----------+----------+---------------+
| NEPSE | 187.52       | -3.1526999999999816 | -1.6534616649368168 | 190.8764 | 187.1536 | 190.6727      |
+-------+--------------+---------------------+---------------------+----------+----------+---------------+

$ priceof --gainers        

Gainers
+-----------+-----+---------+---------+------+------+-----+--------+----------+
| Symbol    | LTP | Change  | %Change | Open | High | Low | Volume | Turnover |
+-----------+-----+---------+---------+------+------+-----+--------+----------+
| GMLI      |     | +167.20 | +10.00% |      |      |     |        |          |
| ICFCD88   |     | +100.00 | +10.00% |      |      |     |        |          |
| BEDC      |     | +74.30  | +9.99%  |      |      |     |        |          |
| NIBLGF    |     | +0.34   | +3.93%  |      |      |     |        |          |
| SJCL      |     | +13.00  | +3.70%  |      |      |     |        |          |
| NICAD8283 |     | +38.40  | +3.47%  |      |      |     |        |          |
| DOLTI     |     | +24.10  | +3.32%  |      |      |     |        |          |
| BNHC      |     | +13.50  | +2.50%  |      |      |     |        |          |
| ILBS      |     | +25.00  | +2.44%  |      |      |     |        |          |
| IHL       |     | +16.00  | +2.21%  |      |      |     |        |          |
| BARUN     |     | +11.00  | +2.06%  |      |      |     |        |          |
| ADBLD83   |     | +21.60  | +2.00%  |      |      |     |        |          |
| LBBLD89   |     | +23.10  | +1.98%  |      |      |     |        |          |
| SAPDBL    |     | +23.90  | +1.95%  |      |      |     |        |          |
| NABBC     |     | +25.00  | +1.39%  |      |      |     |        |          |
| NICL      |     | +11.00  | +1.11%  |      |      |     |        |          |
| UNL       |     | +500.00 | +1.08%  |      |      |     |        |          |
| CMF2      |     | +0.10   | +1.05%  |      |      |     |        |          |
| MEHL      |     | +6.00   | +1.00%  |      |      |     |        |          |
| KPCL      |     | +4.90   | +0.87%  |      |      |     |        |          |
| RFPL      |     | +6.90   | +0.85%  |      |      |     |        |          |
| CORBL     |     | +16.00  | +0.82%  |      |      |     |        |          |
| PBLD87    |     | +8.00   | +0.78%  |      |      |     |        |          |
| SBCF      |     | +0.06   | +0.66%  |      |      |     |        |          |
| H8020     |     | +0.06   | +0.58%  |      |      |     |        |          |
| MFLD85    |     | +5.50   | +0.52%  |      |      |     |        |          |
| PBD84     |     | +5.50   | +0.52%  |      |      |     |        |          |
| MND84/85  |     | +5.00   | +0.49%  |      |      |     |        |          |
| PBD88     |     | +5.00   | +0.46%  |      |      |     |        |          |
| TRH       |     | +5.00   | +0.45%  |      |      |     |        |          |
| NLG       |     | +4.00   | +0.44%  |      |      |     |        |          |
| USHL      |     | +3.00   | +0.39%  |      |      |     |        |          |
| LUK       |     | +0.03   | +0.31%  |      |      |     |        |          |
| PRSF      |     | +0.03   | +0.29%  |      |      |     |        |          |
| GMFBS     |     | +5.00   | +0.28%  |      |      |     |        |          |
| EBLD85    |     | +3.00   | +0.27%  |      |      |     |        |          |
| GRDBL     |     | +2.00   | +0.15%  |      |      |     |        |          |
| MLBSL     |     | +2.80   | +0.12%  |      |      |     |        |          |
| CKHL      |     | +0.90   | +0.11%  |      |      |     |        |          |
| SANIMA    |     | +0.20   | +0.06%  |      |      |     |        |          |
| GBBD85    |     | +0.50   | +0.05%  |      |      |     |        |          |
+-----------+-----+---------+---------+------+------+-----+--------+----------+
```

### Floorsheet Download
```console
$ priceof -f           # Download floorsheet to current directory
$ priceof -f /path/to  # Download to specific directory
```

### Debug Mode
```console
$ priceof NBL NABIL --trace 
23:25:05 API Call: get_stock_prices(['NBL', 'NABIL'])
                                                                                                                                                                                                
Full API Response:
[
  {
    "Symbol": "NBL",
    "LTP": 260.0,
    "change": -1.1999999999999886,
    "%change": -0.4594180704440998,
    "Open": 260.0,
    "High": 275.0,
    "Low": 257.1,
    "Volume": 66079,
    "Turnover": 17180540.0,
    "Prev Close": 261.2
  },
  {
    "Symbol": "NABIL",
    "LTP": 495.0,
    "change": -3.1000000000000227,
    "%change": -0.6223649869504161,
    "Open": 498.0,
    "High": 502.0,
    "Low": 493.0,
    "Volume": 53038,
    "Turnover": 26253810.0,
    "Prev Close": 498.1
  }
]
+--------+--------+--------+---------+--------+--------+--------+--------+---------------+------------+
| Symbol | LTP    | change | %change | Open   | High   | Low    | Volume | Turnover      | Prev Close |
+--------+--------+--------+---------+--------+--------+--------+--------+---------------+------------+
| NBL    | 260.00 | -1.20  | -0.46%  | 260.00 | 275.00 | 257.10 | 66,079 | 17,180,540.00 | 261.20     |
| NABIL  | 495.00 | -3.10  | -0.62%  | 498.00 | 502.00 | 493.00 | 53,038 | 26,253,810.00 | 498.10     |
+--------+--------+--------+---------+--------+--------+--------+--------+---------------+------------+
```

The `--trace` flag shows:
- Timestamp and API method called
- Full JSON response from the API
- Final formatted output

This is useful for:
- Debugging API issues
- Understanding the raw data structure
- Verifying data transformations

## Dependencies
- Python 3.11+
- nepse-cli (actual data fetcher library)
- tabulate, colorama, pandas

## License
MIT License

## Acknowledgments
This is just a CLI wrapper around the unofficial NEPSE API by [basic-bgnr](https://github.com/basic-bgnr/NepseUnofficialApi). All the actual data fetching is handled by that library.

