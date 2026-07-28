from fredapi import Fred 
import pandas as pd 
from config import FRED_API_KEY

SERIES={
    'hy_spread': 'BAA10Y',
    'ig_spread': 'AAA10Y',
    'treasury_10y': 'DGS10',
    'treasury_2y': 'DGS2',
}

def fetch_all():
    fred=Fred(api_key=FRED_API_KEY)
    frames={}
    for name,series_id in SERIES.items():
        print(f"Fetching {name}...")
        frames[name]=fred.get_series(series_id, start='2000-01-01')
    df=pd.DataFrame(frames)
    df['hy_ig_gap']=df['hy_spread']-df['ig_spread']
    df['2s10s']=df['treasury_10y']-df['treasury_2y'] # if negative --> inverted yield curve implies impending recession 
    df.dropna(inplace=True)
    df.to_csv('market_data.csv')
    return df

if __name__ =='__main__':
    df=fetch_all()
    print(df.tail())
    print(df.describe())

