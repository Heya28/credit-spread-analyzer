import pandas as pd 
import numpy as np

class SpreadData:
    # load and hold market data
    def __init__(self, file_path='market_data.csv'):
        self.df=pd.read_csv(file_path, index_col=0, parse_dates=True)
    
    # get one column and drop na
    def get_series(self, name):
        return self.df[name].dropna() # we do not need to do inplace=True? 
    
    # return entire dataframe
    def get_all(self):
        return self.df.copy() # prevent modification to original dataframe


class ZScoreSignal:
    # computes z score based cheap or rich signals for a series
    def __init__(self, threshold=1.5, window=60):
        self.threshold=threshold
        self.window=window
    
    def compute(self, series):
        rolling_mean=series.rolling(self.window).mean() # Series provides the spread ( corporate yield - us treasury yield )
        rolling_std=series.rolling(self.window).std()
        rolling_zscore=(series-rolling_mean)/rolling_std

        signal=pd.Series(index=series.index, dtype=str)
        signal[rolling_zscore>threshold]='CHEAP' # spread is wide; bond price is cheap
        signal[rolling_zscore<-threshold]='RICH' # spread is tight ; bond price is rich or expensive
        signal[rolling_zscore>=-threshold and rolling_zscore<=threshold]='NEUTRAL'

        return pd.DataFrame({
            'spread':series, 
             'mean':     rolling_mean,
            'std':       rolling_std,
            'z_score':   rolling_zscore,
            'signal':    signal,
        })

