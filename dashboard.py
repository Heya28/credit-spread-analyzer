import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def build_dashboard(name: str, results: pd.DataFrame, bt_results: pd.DataFrame,
                     output_file: str = None, save_html: bool = True):
    """
    Builds a 3-row dashboard for ONE series ( HY, IG, HY-IG gap).
    name        -> label used in titles and the output filename -HY" etc 
    results     -> output of ZScoreSignal.compute() -> has columns: spread, mean, Z_score, signal
    bt_results  -> output of Backtester.run()       -> has column: cum_pnl
    save_html   -> set False when calling from Streamlit (st.plotly_chart already
                   displays it — writing a file too is unnecessary and gets
                   overwritten on every rerun)
    """

    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            f'{name} Spread + Rolling Mean',
            f'{name} Z-Score with Signal Thresholds',
            f'{name} Cumulative Strategy P&L (bps)'
        ),
        vertical_spacing=0.08,
        shared_xaxes=True
    )

    # Row 1: Spread + mean 
    fig.add_trace(go.Scatter(
        x=results.index, y=results['spread'],
        name=f'{name} Spread', line=dict(color='#1f77b4', width=1.2)
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=results.index, y=results['mean'],
        name='60D Mean', line=dict(color='orange', dash='dash')
    ), row=1, col=1)

    # Row 2: Z-score 
    fig.add_trace(go.Scatter(
        x=results.index, y=results['Z_score'],
        name='Z-Score', line=dict(color='purple', width=1)
    ), row=2, col=1)

    # Threshold lines (entry/exit levels, same ones used by ZScoreSignal / Backtester)
    for val, color in [(1.5, 'green'), (-1.5, 'red'),
                        (0.5, 'lightgreen'), (-0.5, 'lightsalmon')]:
        fig.add_hline(y=val, line_dash='dot',
                      line_color=color, row=2, col=1)

    # Shade signal regions (continuous CHEAP/RICH stretches, not day-by-day)
    cheap_mask = results['signal'] == 'CHEAP'
    rich_mask = results['signal'] == 'RICH'
    shapes = []
    for mask, color in [(cheap_mask, 'rgba(0,200,0,0.1)'),
                         (rich_mask, 'rgba(200,0,0,0.1)')]:
        in_region = False
        start = None
        for date, val in mask.items():
            if val and not in_region:
                start = date
                in_region = True
            elif not val and in_region:
                shapes.append(dict(
                    type='rect',
                    xref='x2', yref='y2 domain',
                    x0=start, x1=date,
                    y0=0, y1=1,
                    fillcolor=color, line_width=0,
                ))
                in_region = False
    fig.update_layout(shapes=shapes)

    # Row 3: PnL 
    fig.add_trace(go.Scatter(
        x=bt_results.index, y=bt_results['cum_pnl'],
        name='Cumulative PnL', fill='tozeroy',
        line=dict(color='darkgreen', width=1.5)
    ), row=3, col=1)

    fig.update_layout(
        title=f'Credit Spread Analyzer — {name} Dashboard',
        height=900,
        template='plotly_white',
        showlegend=True
    )

    if save_html:
        if output_file is None:
            output_file = f'dashboard_{name.lower().replace(" ", "_").replace("-", "_")}.html'
        fig.write_html(output_file)
        print(f"Dashboard saved to {output_file} — open in browser")

    return fig