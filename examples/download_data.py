import yfinance as yf
import pandas as pd
from pathlib import Path

def download(symbol: str, interval: str = "1m", period: str = "5d", out: str = "data.csv") -> None:
    df = yf.download(tickers=symbol, interval=interval, period=period, progress=False, auto_adjust=False)
    if df is None or df.empty:
        raise SystemExit(f"No data for {symbol}")
    
    # Handle multi-level columns from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        # Get the Close price column (first level is metric, second level is ticker)
        close_col = ('Close', symbol)
        if close_col in df.columns:
            price_col = close_col
        else:
            # Fallback: try to find any Close column
            close_cols = [col for col in df.columns if col[0] == 'Close']
            if close_cols:
                price_col = close_cols[0]
            else:
                raise SystemExit(f"No Close price column found for {symbol}")
    else:
        price_col = "Close" if "Close" in df.columns else "Adj Close"
    
    df = df.reset_index()
    time_col = "Datetime" if "Datetime" in df.columns else ("Date" if "Date" in df.columns else df.columns[0])
    
    # Create clean output dataframe
    out_df = pd.DataFrame({
        'timestamp': df[time_col],
        'price': df[price_col]
    })
    
    # Clean the data
    out_df = out_df.dropna()
    out_df = out_df[out_df['price'] > 0]  # Only positive prices
    out_df = out_df.sort_values('timestamp').reset_index(drop=True)
    
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(out, index=False)
    print(f"Wrote {out} with {len(out_df)} rows")

if __name__ == "__main__":
    download("GOOG", out="examples/goog_1m.csv")

