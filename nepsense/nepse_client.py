from nepse import Nepse as NepseBase
from typing import List, Dict, Any, Union
import sys
from datetime import datetime
import json
from functools import wraps
from pathlib import Path
from subprocess import run
from tqdm import tqdm
import time
from .utils import with_progress

def trace_api(func):
    """Decorator to trace API calls and responses
    
    Logs API method calls and their responses when tracing is enabled.
    
    Args:
        func: The API method to trace
        
    Returns:
        Wrapped function that includes tracing
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Get method name from the original function
        method = func.__name__
        
        # Log API call if trace enabled
        if self.trace:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"{timestamp} API Call: {method}({', '.join(map(str, args))})", 
                  file=sys.stderr)
        
        # Execute the API call
        result = func(self, *args, **kwargs)
        
        # Print debug info if trace enabled
        if self.trace:
            print("\nFull API Response:", file=sys.stderr)
            formatted_json = json.dumps(result, indent=2)
            print(formatted_json, file=sys.stderr)
            
        return result
    return wrapper

def with_loading(desc="Fetching data"):
    """Decorator to show loading animation during API calls
    
    Displays a progress bar while the API call is executing.
    
    Args:
        desc: Description to show in the progress bar
        
    Returns:
        Decorator function that adds loading animation
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with tqdm(total=100, desc=desc, bar_format='{desc}: {bar}| {percentage:3.0f}%') as pbar:
                # Start the loading animation
                pbar.update(10)
                try:
                    result = func(*args, **kwargs)
                    pbar.update(90)  # Complete the progress
                    return result
                except Exception as e:
                    pbar.close()
                    raise e
        return wrapper
    return decorator

class NepseClient:
    """Client wrapper for accessing NEPSE market data
    
    Provides high-level methods to fetch various market data including:
    - Stock prices and trading info
    - Market indices
    - Company details
    - Market depth
    - Top gainers/losers
    
    Attributes:
        client: Underlying NEPSE API client
        trace: Whether to enable API call tracing
    """
    
    def __init__(self, trace=False):
        self.client = NepseBase()
        self.client.setTLSVerification(False)  # Required until NEPSE fixes SSL
        self.trace = trace
        
    def _trace(self, method: str, *args):
        """Log API calls if trace mode is enabled"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"{timestamp} API Call: {method}({', '.join(map(str, args))})", 
              file=sys.stderr)
    
    def _debug(self, message: str = None, data: Any = None):
        """Print debug information if trace mode is enabled
        
        Args:
            message: Optional message to print
            data: Optional data to inspect
        """
        if not self.trace:
            return
        
        if message:
            print(f"\n{message}", file=sys.stderr)
        
        if data:
            print("\nFull API Response:", file=sys.stderr)
            if isinstance(data, list):
                formatted_json = json.dumps(data, indent=2)
                print(formatted_json, file=sys.stderr)
            else:
                formatted_json = json.dumps(data, indent=2)
                print(formatted_json, file=sys.stderr)

    def _print_debug(self):
        """Print stored debug output"""
        if self.trace and hasattr(self, 'debug_output'):
            print(*self.debug_output, sep='\n', file=sys.stderr)
            delattr(self, 'debug_output')
    
    @trace_api
    @with_progress("Fetching stock prices")
    def get_stock_prices(self, symbol: Union[str, List[str]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Get current price for a stock symbol"""
        details = self.client.getCompanyDetails(symbol)
        if details and 'securityDailyTradeDto' in details:
            trade = details['securityDailyTradeDto']
            ltp = trade.get('lastTradedPrice', 0)
            prev_close = trade.get('previousClose', 0)
            change = ltp - prev_close if ltp and prev_close else 0
            
            return {
                'Symbol': symbol,
                'LTP': ltp,
                'change': change,
                '%change': (change / prev_close * 100) if prev_close else 0,
                'Open': trade.get('openPrice', 0),
                'High': trade.get('highPrice', 0),
                'Low': trade.get('lowPrice', 0),
                'Volume': trade.get('totalTradeQuantity', 0),
                'Turnover': trade.get('totalTradeValue', 0) or (trade.get('totalTradeQuantity', 0) * ltp),
                'Prev Close': prev_close
            }
        return None

    @trace_api
    def get_nepse_index(self) -> Dict[str, Any]:
        """Get current NEPSE index"""
        data = self.client.getNepseIndex()
        if isinstance(data, list) and data:
            current = data[0].get('currentValue', 0)
            prev = data[0].get('previousClose', 0)
            # Calculate changes
            change = current - prev if current and prev else 0
            pct_change = (change / prev * 100) if prev else 0
            
            return {
                'index': 'NEPSE',
                'currentValue': current,
                'change': change,
                'perChange': pct_change,
                'high': data[0].get('high'),
                'low': data[0].get('low'),
                'previousClose': data[0].get('previousClose')
            }
        return data
    
    @trace_api
    def get_sub_indices(self) -> List[Dict[str, Any]]:
        """Get all sub-indices"""
        data = self.client.getNepseSubIndices()
        if isinstance(data, list):
            return [{
                'index': item.get('index'),
                'currentValue': item.get('currentValue'),
                'change': item.get('change'),
                'perChange': item.get('perChange')
            } for item in data]
        return data
        
    @trace_api
    def get_market_depth(self, symbol: str) -> Dict[str, Any]:
        """Get market depth for a symbol"""
        details = self.client.getCompanyDetails(symbol)
        if not details:
            return {}
            
        depth = details.get('marketDepth', {})
        return {
            'buyMarketDepthList': depth.get('buyMarketDepthList', []),
            'sellMarketDepthList': depth.get('sellMarketDepthList', []),
            'totalBuyQty': sum(item.get('orderQuantity', 0) 
                             for item in depth.get('buyMarketDepthList', [])),
            'totalSellQty': sum(item.get('orderQuantity', 0) 
                              for item in depth.get('sellMarketDepthList', []))
        }
        
    @trace_api
    def get_top_gainers(self) -> List[Dict[str, Any]]:
        """Get top gaining stocks"""
        data = self.client.getTopGainers()
        
        if isinstance(data, list):
            return [{
                'Symbol': item.get('symbol', ''),
                'LTP': item.get('lastTradedPrice', ''),
                'Change': item.get('pointChange', ''),
                '%Change': item.get('percentageChange', ''),
                'Open': item.get('openPrice', ''),
                'High': item.get('highPrice', ''),
                'Low': item.get('lowPrice', ''),
                'Volume': item.get('quantity', ''),
                'Turnover': item.get('amount', '')
            } for item in data]
        return data
        
    @trace_api
    def get_top_losers(self) -> List[Dict[str, Any]]:
        """Get top losing stocks"""
        data = self.client.getTopLosers()
        if isinstance(data, list):
            return [{
                'Symbol': item.get('symbol', ''),
                'LTP': item.get('lastTradedPrice', ''),
                'Change': item.get('pointChange', ''),
                '%Change': item.get('percentageChange', ''),
                'Open': item.get('openPrice', ''),
                'High': item.get('highPrice', ''),
                'Low': item.get('lowPrice', ''),
                'Volume': item.get('totalTradeQuantity', ''),
                'Turnover': item.get('totalTradeValue', '')
            } for item in data]
        return data

    @trace_api
    def get_floorsheet(self, output_path: Path = None) -> None:
        """Get today's floorsheet using nepse-cli"""
        # Default to current directory if no path specified
        output_file = output_path / "floorsheet.json" if output_path else Path("floorsheet.json")
        
        # Run nepse-cli command
        cmd = ["nepse-cli", "--get-floorsheet", "--output-file", str(output_file)]
        run(cmd)

    @trace_api
    def get_market_summary(self) -> Dict[str, Any]:
        """Get market summary data"""
        data = self.client.getMarketSummary()
        return {
            'totalTurnover': data.get('totalTurnover', 0),
            'totalTradedShares': data.get('totalTradedShares', 0),
            'totalTransactions': data.get('totalTransactions', 0),
            'totalScripTraded': data.get('totalScripTraded', 0),
            'totalMarketCap': data.get('totalMarketCap', 0)
        }

    @trace_api
    @with_progress("Fetching company details")
    def get_company_details(self, symbol: Union[str, List[str]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Get detailed company information"""
        return self.client.getCompanyDetails(symbol)

    @trace_api
    def get_sector_summary(self) -> List[Dict[str, Any]]:
        """Get sector-wise market summary"""
        data = self.client.getNepseSubIndices()
        
        result = []
        if isinstance(data, list):
            result = [{
                'Sector': item.get('index', ''),
                'Value': item.get('currentValue', 0),
                'Change': item.get('change', 0),
                '%Change': item.get('perChange', 0)
            } for item in data]
        
        return result