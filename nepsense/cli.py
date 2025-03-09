#!/usr/bin/env python3
import argparse
from pathlib import Path
from .nepse_client import NepseClient
from .formatters import TableFormatter

"""
Command Line Interface for NEPSE market data

This module provides a CLI tool to access NEPSE market data.
It handles argument parsing and formatting output for terminal display.

Classes:
    NepseCLI: Main CLI handler class
"""

class NepseCLI:
    """Command Line Interface for NEPSE market data
    
    Provides command-line access to NEPSE market data with formatted output.
    Supports various commands for fetching different types of market data.
    
    Attributes:
        client: NepseClient instance for API access
        formatter: TableFormatter instance for output formatting
    """
    
    def __init__(self, trace=False):
        self.client = NepseClient(trace=trace)
        self.formatter = TableFormatter()
        
    def run(self):
        """Parse arguments and execute commands"""
        args = self._parse_arguments()
        self._execute_commands(args)

    @staticmethod
    def _parse_arguments() -> argparse.Namespace:
        """Setup and parse CLI arguments"""
        parser = argparse.ArgumentParser(
            description="NEPSE market data CLI tool",
            prog="priceof"
        )
        
        # Company symbols as positional arguments (default behavior)
        parser.add_argument('symbols', nargs='*', metavar='SYMBOL',
                          help="Company symbols (e.g., NABIL ADBL)")
        
        # Market data options
        parser.add_argument("-n", "--nepse", action="store_true", 
                          help="Get NEPSE index")
        parser.add_argument("-s", "--sub-indices", action="store_true", 
                          help="Get sub-indices")
        parser.add_argument("-ms", "--market_summary", action="store_true", 
                          help="Get market summary")
        
        # Detailed data
        parser.add_argument("-m", "--market_depth", metavar="symbol", 
                          help="Get market depth")
        parser.add_argument("-d", "--get_detail", metavar="symbol", nargs="+",
                          help="Get company details for one or more symbols")
        
        # Top lists
        parser.add_argument("--gainers", action="store_true", 
                          help="Get top gainers")
        parser.add_argument("--losers", action="store_true", 
                          help="Get top losers")
        
        # Data export
        parser.add_argument("-f", "--floorsheet", metavar="path", type=Path, nargs="?",
                          const=Path.cwd(),  # Default to current directory if -f used without path
                          help="Download floorsheet using nepse-cli (optional output path)")
        
        # Debug options
        debug_group = parser.add_argument_group('Debug Options')
        debug_group.add_argument("--trace", action="store_true",
                          help="Show API calls and responses")
        
        # Note unsupported features
        parser.add_argument("--turnover", action="store_true", 
                          help="[Unsupported] Get scripts with maximum turnover")
        parser.add_argument("--volume", action="store_true",
                          help="[Unsupported] Get scripts with maximum volume")
        parser.add_argument("--transactions", action="store_true",
                          help="[Unsupported] Get scripts with maximum transactions")
        parser.add_argument("--supply", action="store_true",
                          help="[Unsupported] Get scripts with maximum supply")
        parser.add_argument("--demand", action="store_true",
                          help="[Unsupported] Get scripts with maximum demand")
        
        # Sector summary
        parser.add_argument("-sec", "--sectors", action="store_true",
                           help="Get sector-wise market summary")
        
        return parser.parse_args()

    def _execute_commands(self, args: argparse.Namespace):
        """Execute commands based on parsed arguments"""
        
        # Handle unsupported features
        unsupported = ['turnover', 'volume', 'transactions', 'supply', 'demand']
        for feature in unsupported:
            if getattr(args, feature, False):
                print(f"Warning: The --{feature} feature is not supported by the current API")
                return
        
        # Company price data (default behavior)
        if args.symbols:
            data = self.client.get_stock_prices(args.symbols)
            self.formatter.print_stock_prices(data)
            return
        
        # Market summary
        if args.market_summary:
            data = self.client.get_market_summary()
            self.formatter.print_table(data)
            return
        
        # Company details
        if args.get_detail:
            data = self.client.get_company_details(args.get_detail)
            self.formatter.print_company_details(data)
            return
        
        # Market indices
        if args.nepse:
            data = self.client.get_nepse_index()
            self.formatter.print_table(data)
            
        if args.sub_indices:
            data = self.client.get_sub_indices()
            self.formatter.print_table(data)
            
        # Market depth
        if args.market_depth:
            data = self.client.get_market_depth(args.market_depth)
            self.formatter.print_market_depth(data)
            
        # Top lists
        if args.gainers:
            data = self.client.get_top_gainers()
            self.formatter.print_top_list(data, "Gainers")
            
        if args.losers:
            data = self.client.get_top_losers()
            self.formatter.print_top_list(data, "Losers")
            
        # Floorsheet export
        if args.floorsheet is not None:
            self.client.get_floorsheet(args.floorsheet)
            return
        
        # Sector summary
        if args.sectors:
            data = self.client.get_sector_summary()
            # Print debug info before table
            self.client._print_debug()
            self.formatter.print_sector_summary(data)
            return

def main():
    args = NepseCLI._parse_arguments()
    cli = NepseCLI(trace=args.trace)
    cli.run()

if __name__ == "__main__":
    main() 