import yfinance as yf
import json
from typing import Dict, List
from pathlib import Path

def market_cap_download(ticker: str) -> None:
    stock = yf.Ticker(ticker)

    # Get historical data (max available)
    hist = stock.history(period="max")

    # Calculate market capitalization (closing price * shares outstanding)
    hist = hist.assign(Market_Cap=hist['Close'] * stock.info['sharesOutstanding'])

    # Prepare data for Chart.js
    chart_data = hist['Market_Cap'].reset_index()
    json_data: List[Dict[str, float]] = [
        {
            'x': str(row['Date']),
            'y': round(row['Market_Cap'], 2)
        }
        for _, row in chart_data.iterrows()
    ]

    # Save data as JSON
    output_file = Path(f"{ticker.lower()}_market_cap.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(json_data))

    print(f"Data saved to {output_file}")

import yfinance as yf
from pathlib import Path
import json
from typing import List, Dict

def market_cap_download_2(ticker: str) -> None:
    if ticker.upper() in ['GOOGL', 'GOOG']:
        # Handle Google/Alphabet specially
        googl = yf.Ticker('GOOGL')
        goog = yf.Ticker('GOOG')
        
        # Get historical data (max available)
        hist_googl = googl.history(period="max")
        hist_goog = goog.history(period="max")
        
        # Ensure both dataframes have the same index
        common_index = hist_googl.index.intersection(hist_goog.index)
        hist_googl = hist_googl.loc[common_index]
        hist_goog = hist_goog.loc[common_index]
        
        # Calculate total market capitalization
        total_shares = googl.info['sharesOutstanding'] + goog.info['sharesOutstanding']
        hist = hist_googl.copy()
        hist['Close'] = (hist_googl['Close'] * googl.info['sharesOutstanding'] + 
                         hist_goog['Close'] * goog.info['sharesOutstanding']) / total_shares
        hist = hist.assign(Market_Cap=hist['Close'] * total_shares)
    else:
        stock = yf.Ticker(ticker)
        # Get historical data (max available)
        hist = stock.history(period="max")
        # Calculate market capitalization (closing price * shares outstanding)
        hist = hist.assign(Market_Cap=hist['Close'] * stock.info['sharesOutstanding'])

    # Prepare data for Chart.js
    chart_data = hist['Market_Cap'].reset_index()
    json_data: List[Dict[str, float]] = [
        {
            'x': str(row['Date']),
            'y': round(row['Market_Cap'], 2)
        }
        for _, row in chart_data.iterrows()
    ]

    # Save data as JSON
    output_file = Path(f"{ticker.lower()}_market_cap.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(json_data))

    print(f"Data saved to {output_file}")

# Usage
market_cap_download('GOOGL')  # This will handle both GOOGL and GOOG