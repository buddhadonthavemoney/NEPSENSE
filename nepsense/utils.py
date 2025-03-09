"""
Utility functions for NEPSE market data handling

This module provides common utility functions used across the package
for data processing, formatting, and display.

Functions:
    with_progress: Progress bar decorator for long operations
"""

import sys
from functools import wraps
from tqdm import tqdm

def with_progress(desc="Fetching data"):
    """Decorator to show progress bar during function execution"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not sys.stdout.isatty():
                return func(*args, **kwargs)

            # Get the symbols argument
            symbols = args[1] if len(args) > 1 else []
            
            # Handle single symbol case
            if isinstance(symbols, str):
                return func(*args, **kwargs)
                
            # For list of symbols, handle iteration here
            results = []
            with tqdm(total=len(symbols), desc=desc, leave=False) as pbar:
                for symbol in symbols:
                    # Call the function with one symbol at a time
                    result = func(args[0], symbol)
                    if result:
                        results.append(result)
                    pbar.update(1)
                return results

        return wrapper
    return decorator 