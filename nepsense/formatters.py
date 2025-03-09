from tabulate import tabulate
from colorama import Fore, Style
import pandas as pd
from typing import Dict, List, Any, Union
from datetime import datetime
import calendar

"""
Formatting utilities for NEPSE market data

This module handles formatting and display of market data in tables
and other human-readable formats. Supports colored output for price
changes and customizable table layouts.

Classes:
    TableFormatter: Main formatter class for market data
"""

class TableFormatter:
    """Handles formatting and display of market data
    
    Formats various types of market data into readable tables with:
    - Colored price changes (green for positive, red for negative)
    - Aligned columns
    - Customizable headers
    - Different layouts for different data types
    
    Methods:
        print_table: Generic table printer
        print_stock_prices: Format stock price data
        print_company_details: Format detailed company info
        print_market_depth: Format market depth data
        print_top_list: Format top gainers/losers lists
    """
    
    def __init__(self):
        self.style = {
            'up': Fore.GREEN,
            'down': Fore.RED,
            'neutral': Fore.CYAN,
            'reset': Style.RESET_ALL
        }

    def _format_table(self, df: pd.DataFrame, 
                     headers: Union[str, Dict[str, str]] = "keys",
                     transpose: bool = False,
                     title: str = None,
                     **kwargs) -> str:
        """Helper method to standardize table formatting
        
        Args:
            df: DataFrame to format
            headers: Column headers (string or dict mapping)
            transpose: Whether to transpose the table
            title: Optional title to display above table
            **kwargs: Additional arguments for tabulate
        """
        default_opts = {
            'tablefmt': "pretty",
            'showindex': False,
            'floatfmt': ".2f",
            'numalign': "right",
            'stralign': "left"
        }
        
        # Override defaults with provided kwargs
        opts = {**default_opts, **kwargs}
        
        # Handle transposition
        data = df.T if transpose else df
        
        # Print title if provided
        if title:
            print(f"\n{self.style['neutral']}{title}{self.style['reset']}")
            
        return tabulate(data, headers=headers, **opts)

    def print_table(self, data: Dict[str, Any], headers: str = "keys"):
        """Print formatted table with selected columns"""
        if isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            df = pd.DataFrame([data])
            
        # Convert numeric columns for color formatting
        if 'Change' in df.columns:
            numeric_cols = ['Value', 'Change', '%Change']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Store numeric values for comparison
            changes = df['Change'].copy()
            
            # Add colors and format numbers
            self._format_numeric_columns(df, changes)
        
        # Format large numbers for market summary
        for col in df.columns:
            if col in ['Total Turnover', 'Total Traded Shares', 'Total Transactions', 
                      'Total Scripts Traded', 'Market Capitalization']:
                df[col] = df[col].apply(lambda x: f"{float(x):,.2f}")

        print(self._format_table(df, headers=headers))

    def _format_numeric_columns(self, df: pd.DataFrame, changes: pd.Series = None):
        """Helper method to format numeric columns with colors"""
        if changes is None:
            changes = pd.Series([0] * len(df))  # Default to no change if not provided
        
        if 'Value' in df.columns:
            df['Value'] = df.apply(
                lambda x, c=changes: f"{self.style['up']}{x['Value']:.2f}{self.style['reset']}" if c[x.name] > 0
                else f"{self.style['down']}{x['Value']:.2f}{self.style['reset']}" if c[x.name] < 0
                else f"{x['Value']:.2f}",
                axis=1
            )
        if 'Change' in df.columns:
            df['Change'] = df.apply(
                lambda x, c=changes: f"{self.style['up']}+{x['Change']:.2f}{self.style['reset']}" if c[x.name] > 0
                else f"{self.style['down']}{x['Change']:.2f}{self.style['reset']}"
                if c[x.name] < 0 else f"{x['Change']:.2f}",
                axis=1
            )
        if '%Change' in df.columns:
            df['%Change'] = df.apply(
                lambda x, c=changes: f"{self.style['up']}+{x['%Change']:.2f}{self.style['reset']}" if c[x.name] > 0
                else f"{self.style['down']}{x['%Change']:.2f}{self.style['reset']}"
                if c[x.name] < 0 else f"{x['%Change']:.2f}",
                axis=1
            )
        
        # Format remaining numeric columns if they exist
        for col in ['High', 'Low', 'Prev Close']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: f"{x:.2f}")

    def print_stock_prices(self, data: List[Dict[str, Any]]):
        """Format and display stock prices"""
        if not data:
            print("No price data available")
            return
        
        df = pd.DataFrame(data)
        
        # Convert numeric columns first
        numeric_cols = ['LTP', 'change', '%change', 'Volume', 'Turnover', 'High', 'Low', 'Open', 'Prev Close']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Store numeric values for comparison
        changes = df['change'].copy() if 'change' in df.columns else pd.Series([0] * len(df))
        
        # Format numbers
        if 'Volume' in df.columns:
            df['Volume'] = df['Volume'].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else '')
        if 'Turnover' in df.columns:
            df['Turnover'] = df['Turnover'].apply(lambda x: f"{x:,.2f}" if pd.notnull(x) else '')
        for col in ['LTP', 'High', 'Low', 'Open', 'Prev Close']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else '')
        
        # Color code changes using stored numeric values
        if 'change' in df.columns:
            df['change'] = df.apply(
                lambda x, c=changes: f"{self.style['up']}+{x['change']:.2f}{self.style['reset']}" if c[x.name] > 0
                else f"{self.style['down']}{x['change']:.2f}{self.style['reset']}"
                if c[x.name] < 0 else f"{x['change']:.2f}",
                axis=1
            )
        if '%change' in df.columns:
            df['%change'] = df.apply(
                lambda x, c=changes: f"{self.style['up']}+{x['%change']:.2f}%{self.style['reset']}" if c[x.name] > 0
                else f"{self.style['down']}{x['%change']:.2f}%{self.style['reset']}"
                if c[x.name] < 0 else f"{x['%change']:.2f}%",
                axis=1
            )
        
        print(self._format_table(
            df,
            headers={
                'Symbol': 'Symbol',
                'LTP': 'LTP',
                'change': 'Change',
                '%change': '%Change',
                'Open': 'Open',
                'High': 'High',
                'Low': 'Low',
                'Volume': 'Volume',
                'Turnover': 'Turnover',
                'Prev Close': 'Prev Close'
            }
        ))

    def print_market_depth(self, data: Dict[str, Any]):
        """Format and display market depth data"""
        buy_df = pd.DataFrame(data.get('buyMarketDepthList', []))
        sell_df = pd.DataFrame(data.get('sellMarketDepthList', []))
        
        if not buy_df.empty:
            buy_df.columns = [f"{self.style['up']}{col}{self.style['reset']}" 
                            for col in buy_df.columns]
            print(self._format_table(buy_df, title="Buy Orders"))
            print(f"\nTotal Buy Quantity: {data.get('totalBuyQty', 0):,}")
        
        if not sell_df.empty:
            sell_df.columns = [f"{self.style['down']}{col}{self.style['reset']}" 
                             for col in sell_df.columns]
            print(self._format_table(sell_df, title="Sell Orders"))
            print(f"\nTotal Sell Quantity: {data.get('totalSellQty', 0):,}")

    def print_top_list(self, data: List[Dict[str, Any]], list_type: str):
        """Format and display top lists (gainers, losers, etc)"""
        if not data:
            print(f"No {list_type} data available")
            return
        
        df = pd.DataFrame(data)
        
        # Convert numeric columns first
        numeric_cols = ['LTP', 'Change', '%Change', 'Open', 'High', 'Low', 'Volume', 'Turnover']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Store numeric values for comparison
        changes = df['Change'].copy() if 'Change' in df.columns else pd.Series([0] * len(df))
        
        # Format numbers
        if 'Volume' in df.columns:
            df['Volume'] = df['Volume'].apply(lambda x: f"{x:,.0f}" if pd.notnull(x) else '')
        if 'Turnover' in df.columns:
            df['Turnover'] = df['Turnover'].apply(lambda x: f"{x:,.2f}" if pd.notnull(x) else '')
        for col in ['LTP', 'High', 'Low', 'Open']:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else '')
        
        # Color code changes
        color = self.style['up'] if list_type == "Gainers" else self.style['down']
        df['Symbol'] = df['Symbol'].apply(lambda x: f"{color}{x}{self.style['reset']}")
        
        if 'Change' in df.columns:
            df['Change'] = df.apply(
                lambda x, c=changes: f"{color}{'+' if c[x.name] > 0 else ''}{x['Change']:.2f}{self.style['reset']}", 
                axis=1
            )
        if '%Change' in df.columns:
            df['%Change'] = df.apply(
                lambda x, c=changes: f"{color}{'+' if c[x.name] > 0 else ''}{x['%Change']:.2f}%{self.style['reset']}", 
                axis=1
            )
        
        print(self._format_table(
            df,
            headers={
                'Symbol': 'Symbol',
                'LTP': 'LTP',
                'Change': 'Change',
                '%Change': '%Change',
                'Open': 'Open',
                'High': 'High',
                'Low': 'Low',
                'Volume': 'Volume',
                'Turnover': 'Turnover'
            },
            title=list_type
        ))

    def save_floorsheet(self, data: List[Dict[str, Any]], path):
        """Save floorsheet data to CSV"""
        if not data:
            print("No floorsheet data available")
            return
            
        df = pd.DataFrame(data)
        date = datetime.now()
        weekday = calendar.day_name[date.weekday()]
        filename = f"floorsheet_{date.date()}_{weekday}.csv"
        
        df.to_csv(path / filename, index=False)
        print(f"Floorsheet saved to {path / filename}")

    def print_company_details(self, data: Union[Dict[str, Any], List[Dict[str, Any]]]):
        """Format and display detailed company information"""
        if not data:
            print("No company details available")
            return
        
        # Convert single company to list
        companies = data if isinstance(data, list) else [data]
        
        # Extract info for each company
        company_info = []
        for company in companies:
            security = company.get('security', {})
            company_data = security.get('companyId', {})
            sector = company_data.get('sectorMaster', {})
            
            # Get trading info
            trade = company.get('securityDailyTradeDto', {})
            ltp = trade.get('lastTradedPrice', 0)
            prev_close = trade.get('previousClose', 0)
            change = ltp - prev_close if ltp and prev_close else 0
            pct_change = (change / prev_close * 100) if prev_close else 0
            
            # Color formatting
            color = self.style['up'] if change > 0 else self.style['down'] if change < 0 else ''
            reset = self.style['reset'] if color else ''
            
            company_info.append({
                'Symbol': security.get('symbol', ''),
                'Name': company_data.get('companyName', ''),
                'Sector': sector.get('sectorDescription', ''),
                'LTP': f"{color}{ltp:,.2f}{reset}",
                'Change': f"{color}{change:+.2f}{reset}",
                '%Change': f"{color}{pct_change:+.2f}%{reset}",
                'Market Cap': f"{company.get('marketCapitalization', 0):,.0f}",
                'Listed Shares': f"{company.get('stockListedShares', 0):,.0f}",
                'Public %': f"{company.get('publicPercentage', 0):,.2f}%",
                'Promoter %': f"{company.get('promoterPercentage', 0):,.2f}%"
            })
        
        print(self._format_table(
            pd.DataFrame(company_info),
            headers={
                'Symbol': 'Symbol',
                'Name': 'Name',
                'Sector': 'Sector',
                'LTP': 'LTP',
                'Change': 'Change',
                '%Change': '%Change',
                'Market Cap': 'Market Cap',
                'Listed Shares': 'Listed Shares',
                'Public %': 'Public %',
                'Promoter %': 'Promoter %'
            },
            title="Company Information"
        ))

    def print_sector_summary(self, data: List[Dict[str, Any]]):
        """Format and display sector-wise market summary"""
        if not data:
            print("No sector data available")
            return
        
        df = pd.DataFrame(data)
        
        # Convert numeric columns first
        numeric_cols = ['Value', 'Change', '%Change']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Store numeric values for comparison before formatting
        changes = df['Change'].copy() if 'Change' in df.columns else pd.Series([0] * len(df))
        
        # Format numbers
        if 'Value' in df.columns:
            df['Value'] = df['Value'].apply(lambda x: f"{x:,.2f}" if pd.notnull(x) else '')
        
        # Color code changes using stored numeric values
        if 'Change' in df.columns:
            df['Change'] = df.apply(
                lambda x, c=changes: f"{self.style['up']}+{x['Change']:.2f}{self.style['reset']}" if c[x.name] > 0
                else f"{self.style['down']}{x['Change']:.2f}{self.style['reset']}"
                if c[x.name] < 0 else f"{x['Change']:.2f}",
                axis=1
            )
        if '%Change' in df.columns:
            df['%Change'] = df.apply(
                lambda x, c=changes: f"{self.style['up']}+{x['%Change']:.2f}%{self.style['reset']}" if c[x.name] > 0
                else f"{self.style['down']}{x['%Change']:.2f}%{self.style['reset']}"
                if c[x.name] < 0 else f"{x['%Change']:.2f}%",
                axis=1
            )
        
        print(self._format_table(
            df,
            headers={
                'Sector': 'Sector',
                'Value': 'Value', 
                'Change': 'Change',
                '%Change': '%Change'
            },
            title="Sector Summary"
        )) 