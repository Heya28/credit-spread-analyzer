from fredapi import Fred
import pandas as pd
import os

# Load FRED_API_KEY from whichever source is available
FRED_API_KEY = os.environ.get('FRED_API_KEY')

if not FRED_API_KEY:
    try:
        from config import FRED_API_KEY  # works locally, config.py is gitignored
    except ImportError:
        pass

if not FRED_API_KEY:
    try:
        import streamlit as st
        FRED_API_KEY = st.secrets['FRED_API_KEY']  # works on Streamlit Cloud
    except Exception:
        pass

if not FRED_API_KEY:
    raise RuntimeError(
        "FRED_API_KEY not found — set it in config.py locally, "
        "or in Streamlit Cloud's Secrets settings."
    )

SERIES = {
    'hy_spread': 'BAA10Y',
    'ig_spread': 'AAA10Y',
    'treasury_10y': 'DGS10',
    'treasury_2y': 'DGS2',
}

def fetch_all():
    fred = Fred(api_key=FRED_API_KEY)
    frames = {}
    for name, series_id in SERIES.items():
        print(f"Fetching {name}...")
        frames[name] = fred.get_series(series_id, start='2000-01-01')
    df = pd.DataFrame(frames)
    df['hy_ig_gap'] = df['hy_spread'] - df['ig_spread']
    df['2s10s'] = df['treasury_10y'] - df['treasury_2y']  # if negative --> inverted yield curve implies impending recession
    df.dropna(inplace=True)
    df.to_csv('market_data.csv')
    return df

if __name__ == '__main__':
    df = fetch_all()
    print(df.tail())
    print(df.describe())