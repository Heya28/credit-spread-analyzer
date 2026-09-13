import streamlit as st
import os

from data_fetcher import fetch_all
from spread_analyzer import SpreadData, ZScoreSignal, SignalReport
from backtester import Backtester
from dashboard import build_dashboard


def explain_signal(name: str, spread: float, z: float, signal: str) -> str:
    """ Explanation of numbers ( no external API as of now, rules are based on Z-score. ) 
    """
    if signal == 'CHEAP':
        return (
            f"{name} spread is at {spread:.2f}%, which is {z:.2f} standard "
            f"deviations ABOVE its own 60-day average. That means the market "
            f"is demanding more compensation than usual to hold this credit which is  "
            f"a sign of rising fear or stress relative to recent history. "
            f"Historically this is when credit looks 'cheap' (bond prices "
            f"have fallen as yields/spreads rose)."
        )
    elif signal == 'RICH':
        return (
            f"{name} spread is at {spread:.2f}%, which is {z:.2f} standard "
            f"deviations BELOW its own 60-day average. Investors are accepting "
            f"less compensation than usual which is a sign of complacency or confidence. "
            f"This is when credit looks 'rich' (bond prices have risen as "
            f"yields/spreads fell)."
        )
    else:
        return (
            f"{name} spread is at {spread:.2f}%, which is within {z:.2f} "
            f"standard deviations of its own 60-day average which is nothing unusual "
            f"relative to its recent history. No strong signal either way."
        )


st.set_page_config(page_title="Credit Spread Analyzer", layout="wide")
st.title("Credit Spread Analyzer")
st.caption("HY / IG / HY-IG Gap — Tracks US corporate bond spreads and flags when they look unusually cheap or expensive vs their own recent history.")

#  Fetch data (cached so it doesn't re-hit the FRED API on every click) 
@st.cache_data(ttl=86400)  # cache for 24 hours
def load_data():
    if not os.path.exists('market_data.csv'):
        fetch_all()
    data = SpreadData()
    return data.get_series('hy_spread'), data.get_series('ig_spread'), data.get_series('hy_ig_gap')

hy, ig, hy_ig = load_data()

signal_engine = ZScoreSignal()
result_hy = signal_engine.compute(hy)
result_ig = signal_engine.compute(ig)
result_hy_ig = signal_engine.compute(hy_ig)

bt_hy = Backtester(result_hy)
bt_ig = Backtester(result_ig)
bt_hy_ig = Backtester(result_hy_ig)

bt_results_hy = bt_hy.run()
bt_results_ig = bt_ig.run()
bt_results_hy_ig = bt_hy_ig.run()

# Layout: one tab per series
tab1, tab2, tab3 = st.tabs(["High Yield", "Investment Grade", "HY-IG Gap"])

for tab, name, results, bt_results, bt in [
    (tab1, "HY", result_hy, bt_results_hy, bt_hy),
    (tab2, "IG", result_ig, bt_results_ig, bt_ig),
    (tab3, "HY-IG Gap", result_hy_ig, bt_results_hy_ig, bt_hy_ig),
]:
    with tab:
        latest = results.dropna().iloc[-1]
        col1, col2, col3 = st.columns(3)
        col1.metric("Latest Spread", f"{latest['spread']:.2f}")
        col2.metric("Z-Score", f"{latest['Z_score']:.2f}")
        col3.metric("Signal", latest['signal'])

        st.info(explain_signal(name, latest['spread'], latest['Z_score'], latest['signal']))

        fig = build_dashboard(name, results, bt_results, save_html=False)
        st.plotly_chart(fig, use_container_width=True)

        pnl = bt_results['daily_pnl'].dropna()
        sharpe = pnl.mean() / pnl.std() * (252 ** 0.5)
        total = bt_results['cum_pnl'].iloc[-1]
        trades = (bt_results['position'].diff() != 0).sum()

        st.write(
            f"**Total PnL:** {total:.1f} bps &nbsp;|&nbsp; "
            f"**Sharpe:** {sharpe:.2f} &nbsp;|&nbsp; "
            f"**Trades:** {trades}"
        )