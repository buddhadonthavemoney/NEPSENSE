# NEPSENSE

A command-line tool for accessing real-time NEPSE (Nepal Stock Exchange) market data.

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

## Features
- Real-time stock prices and market depth
- Company details and sector information
- NEPSE index and sub-indices
- Market summary and sector-wise data
- Top gainers and losers
- Floorsheet download (via nepse-cli)

## Usage

### Basic Stock Price Lookup
```bash
priceof NABIL          # Single company
priceof NABIL NBL ADBL # Multiple companies
```

### Company Details
```bash
priceof -d NABIL          # Single company details
priceof -d NABIL NBL ADBL # Multiple company details
```

### Market Data
```bash
priceof -n           # NEPSE index
priceof -s           # Sub-indices
priceof -sec         # Sector-wise summary
priceof -ms          # Market summary
priceof --gainers    # Top gainers
priceof --losers     # Top losers
priceof -m NABIL     # Market depth for NABIL
```

### Floorsheet Download
```bash
priceof -f           # Download floorsheet to current directory
priceof -f /path/to  # Download to specific directory
```
Note: Floorsheet download requires nepse-cli

### Debug Mode
```bash
priceof NABIL --trace  # Show API calls and responses
```

## Sample Output

### Stock Prices
```
+---------+--------+--------+---------+--------+--------+--------+--------+---------------+------------+
| Symbol  | LTP    | Change | %Change | Open   | High   | Low    | Volume | Turnover     | Prev Close |
+---------+--------+--------+---------+--------+--------+--------+--------+---------------+------------+
| NABIL   | 495.00 | -3.10  | -0.62%  | 498.00 | 502.00 | 493.00 | 53,038 | 26,253,810   | 498.10     |
+---------+--------+--------+---------+--------+--------+--------+--------+---------------+------------+
```

### Company Details
```
Company Information
+---------+--------------------+------------------+--------+--------+---------+----------------+---------------+-----------+-------------+
| Symbol  | Name               | Sector           | LTP    | Change | %Change | Market Cap     | Listed Shares | Public %  | Promoter % |
+---------+--------------------+------------------+--------+--------+---------+----------------+---------------+-----------+-------------+
| NABIL   | Nabil Bank Limited | Commercial Banks | 495.00 | -3.10  | -0.62%  | 133,932,142,080| 270,569,984   | 41.56%    | 58.44%     |
+---------+--------------------+------------------+--------+--------+---------+----------------+---------------+-----------+-------------+
```

## Dependencies
- Python 3.11+
- nepse-cli(actual data fetcher lbrary)
- tabulate, colorama, pandas

## License
MIT License

## Acknowledgments
Uses the unofficial NEPSE API by [basic-bgnr](https://github.com/basic-bgnr/NepseUnofficialApi)

https://user-images.githubusercontent.com/52292457/123535784-e636d300-d745-11eb-9fe3-3ad4b8e21078.mp4

```

