import pandas as pd
import numpy as np

class Backtester:
    """ Simulates trading on a signal series.
    Position: +1 = long credit, -1 = short credit, 0 = flat
    """
    def __init__(self, results, entry_z=1.5, exit_z=0.5):
        self.results=results.dropna().copy()
        self.entry_z=entry_z
        self.exit_z=exit_z
    
    def run(self):
        # returns a pd dataframe
        df=self.results.copy();
        position=[]
        curr_pos=0
        for z in df['Z_score']:
            if curr_pos==0:
                if z>self.entry_z:
                    curr_pos=1 # go long ( buy cheap credit )
                elif z<-self.entry_z:
                    curr_pos=-1 # go short ( sell rich credit )
            elif curr_pos==1:
                if z<self.exit_z:
                    curr_pos=0 # exit long
            elif curr_pos==-1:
                if z>-self.exit_z:
                    curr_pos=0 # exit short 
            position.append(curr_pos)
        
        df['position']=position

        # PnL - how much profit and loss ( spread points ) we made or lost
        # spread changes appx inverse of return 
        df['spread_change']=df['spread'].diff()
        df['daily_pnl']=-df['position'].shift(1)*df['spread_change']
        df['cum_pnl']=df['daily_pnl'].cumsum()
        return df

    def stats(self, df:pd.DataFrame):
        pnl=df['daily_pnl'].dropna()
        sharpe=pnl.mean()/ pnl.std() *np.sqrt(252) # >1 - good, >2 - excellent, <0.5 - losing money over time
        total=df['cum_pnl'].iloc[-1] # final total profit or loss
        dd= (df['cum_pnl']-df['cum_pnl'].cummax()).min()
        wins=(pnl>0).sum() / (pnl!=0).sum()*100
        trades = (df['position'].diff() != 0).sum()

        print("\nBacktest Results")
        print(f"Total PnL (bps): {total:.1f}")
        print(f"Sharpe Ratio: {sharpe:.2f}")
        print(f"Max Drawdown (bps): {dd:.1f}")
        print(f"Win Rate: {wins:.1f}")
        print(f"Total Trades: {trades}")