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
                    position=1 # go long ( buy cheap credit )
                elif z<-self.entry_z:
                    position=-1 # go short ( sell rich credit )
            elif curr_pos==1:
                if z<self.exit_z:
                    position=0 # exit long
            elif curr_pos==-1:
                if z>-self.exit_z:
                    curr_pos=0 # exit short 
            position.append(curr_pos)
        
        df['position']=position

        # PnL - how much profit and loss ( spread points ) we made or lost
        # spread changes appx inverse of return 
        df['spread_change']=df['spread'].diff()
        df['daily_pnl']=-df['position'].shift(1)*df[spread_change]
