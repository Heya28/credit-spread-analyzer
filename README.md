# Credit Spread Analyzer

**Status:** Data Pipeline & Signal Engine Completed. Backtesting & Visualization in development.

## Overview
This project is a Python-based quantitative tool designed to monitor corporate bond markets, detect abnormal credit spread movements, and generate automated trade signals. Inspired by macro-economic discussions regarding how global geopolitical events (e.g., COVID-19, Russia-Ukraine conflict) directly impact market risk sentiment, this analyzer quantifies those shocks using historical market data. 

## The Finance Behind the Code
*   **What is a Credit Spread?** Corporate bonds are riskier than US Treasuries. To attract investors, corporations must offer higher yields. The difference between a corporate bond yield and a risk-free treasury yield is the "credit spread."
*   **Why it Matters:** Spreads act as a fear gauge. When spreads widen significantly, the market is panicking (bonds are cheap). When spreads are extremely tight, the market is confident (bonds are rich).
*   **The Strategy:** This tool identifies "rich" or "cheap" credit environments by calculating a rolling 60-day Z-score of High Yield (HY) and Investment Grade (IG) spreads to contextualize today's market against the recent past.
    *   **Z-Score > +1.5:** Spread is unusually wide (Market panic → Credit is CHEAP).
    *   **Z-Score < -1.5:** Spread is unusually tight (Market calm → Credit is RICH).

## Current Features (Completed)
*   **Automated Data Pipeline (`data_fetcher.py`):** Integrates with the FRED API to fetch over 20 years of daily market data (approx. 5,000 records), specifically tracking:
    *   High Yield (HY) Credit Spreads (Junk bonds)
    *   Investment Grade (IG) Credit Spreads (Safe corporate bonds)
    *   10-Year and 2-Year US Treasury Yields (for yield curve slope / 2s10s analysis)
*   **OOP Signal Engine (`spread_analyzer.py`):**
    *   `SpreadData`: Encapsulates data loading and extraction (Single Responsibility Principle).
    *   `ZScoreSignal`: Computes rolling 60-day means, standard deviations, and Z-scores to emit automated 'RICH', 'CHEAP', or 'NEUTRAL' trade signals.
    *   `SignalReport`: Aggregates results and provides terminal-based signal distributions.

## Upcoming Features (In Development)
*   **Historical Backtester (`backtester.py`):** A module to simulate daily PnL based on the Z-score signals (going long on cheap credit, shorting rich credit) to evaluate strategy efficacy (Sharpe ratio, max drawdown, win rate).
*   **Interactive Dashboard (`dashboard.py`):** A Plotly-based HTML visualizer plotting the HY spread alongside Z-score thresholds and cumulative PnL.
*   **Macro Event Overlays:** The dashboard will feature vertical markers for major historical shocks (Lehman Collapse, COVID-19 Panic, Russia-Ukraine War, Iran Escalation) to visually correlate global uncertainty with credit spread spikes.

## Installation & Setup

```bash
# Clone the repository
git clone [https://github.com/Heya28/credit-spread-analyzer.git](https://github.com/Heya28/credit-spread-analyzer.git)
cd credit-spread-analyzer

# Install dependencies
pip install pandas matplotlib plotly fredapi scipy requests

# Setup FRED API Key
# 1. Get a free API key from [https://fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)
# 2. Create a config.py file in the root directory and add:
# FRED_API_KEY = 'your_api_key_here'

# Run the data fetcher and signal engine
python main.py
