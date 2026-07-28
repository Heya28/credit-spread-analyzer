from data_fetcher import fetch_all
from spread_analyzer import SpreadData, ZScoreSignal, SignalReport
import os
import time

# fetch data every new day
if not os.path.exists('market_data.csv') or \
   (time.time() - os.path.getmtime('market_data.csv')) > 86400:
    fetch_all()

data = SpreadData()
hy = data.get_series('hy_spread')
ig = data.get_series('ig_spread')
hy_ig=data.get_series('hy_ig_gap')

signal_engine=ZScoreSignal()
result_hy=signal_engine.compute(hy)
result_ig=signal_engine.compute(ig)
result_hy_ig=signal_engine.compute(hy_ig)

report_hy=SignalReport(result_hy)
report_ig=SignalReport(result_ig)
report_hy_ig=SignalReport(result_hy_ig)


print("\nHigh Yield Bonds")
report_hy.latest()
report_hy.summary()

print("\nInvestment Grade Bonds")
report_ig.latest()
report_ig.summary()

print("\nHY-IG Gap (Credit Stress Indicator)") # high gap indicates panic or stress in market leading to relative value opportunities in high yield bonds. 
report_hy_ig.latest()
report_hy_ig.summary()