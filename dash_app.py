import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import yfinance as yf

# --- Data Fetching and Preparation (Copied from plot_indices.py) ---
def fetch_data(tickers, start_date, end_date):
    """Fetches historical data for a list of tickers."""
    data = yf.download(tickers, start=start_date, end=end_date, progress=False, timeout=30)
    return data['Close']

def get_data():
    """Fetches and prepares all necessary financial data."""
    start_date = "2000-01-01"
    end_date = pd.to_datetime("today").strftime('%Y-%m-%d')
    
    index_tickers = {
        "DAX": "^GDAXI",
        "SP500_TR": "^SP500TR",
        "SMIC": "^SSMI",
        "CAC40": "^FCHI",
        "GOLD": "GC=F"
    }
    currency_tickers = {
        "EURCHF": "EURCHF=X",
        "USDCHF": "USDCHF=X"
    }
    
    indices_data = fetch_data(list(index_tickers.values()), start_date, end_date)
    currency_data = fetch_data(list(currency_tickers.values()), start_date, end_date)

    indices_data.rename(columns={v: k for k, v in index_tickers.items()}, inplace=True)
    currency_data.rename(columns={v: k for k, v in currency_tickers.items()}, inplace=True)

    currency_data.ffill(inplace=True)
    df = pd.concat([indices_data, currency_data], axis=1).ffill()

    df['DAX_CHF'] = df['DAX'] * df['EURCHF']
    df['SP500_TR_CHF'] = df['SP500_TR'] * df['USDCHF']
    df['CAC40_CHF'] = df['CAC40'] * df['EURCHF']
    df['SMIC_CHF'] = df['SMIC']
    df['GOLD_CHF'] = df['GOLD'] * df['USDCHF']

    return df[['DAX_CHF', 'SP500_TR_CHF', 'SMIC_CHF', 'CAC40_CHF', 'GOLD_CHF']].dropna()

def calculate_cagr(series):
    """Calculates CAGR for a given series."""
    if len(series) < 2:
        return 0
    start_value = series.iloc[0]
    end_value = series.iloc[-1]
    num_years = (series.index[-1] - series.index[0]).days / 365.25
    if num_years <= 0: # Handle cases where num_years is zero or negative
        return 0
    cagr = (end_value / start_value) ** (1 / num_years) - 1
    return cagr

# --- Initialize Dash app ---
app = dash.Dash(__name__)

# --- Load data once ---
df_chf = get_data()

# --- Define app layout ---
app.layout = html.Div([
    html.H1("Financial Index Performance (CHF)", style={'textAlign': 'center'}),

    dcc.Graph(id='performance-graph'),

    html.Div(id='cagr-output', style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'gap': '20px', 'marginTop': 20}),
    html.Div(id='final-value-output', style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'gap': '20px', 'marginTop': 20})
])

# --- Callback to update graph and CAGR ---
@app.callback(
    Output('performance-graph', 'figure'),
    Output('cagr-output', 'children'),
    Output('final-value-output', 'children'),
    Input('performance-graph', 'relayoutData') # This input captures zoom/pan events including range slider
)
def update_graph_and_cagr(relayoutData):
    # Determine the date range from the relayoutData
    if relayoutData and 'xaxis.range[0]' in relayoutData:
        start_date_str = relayoutData['xaxis.range[0]']
        end_date_str = relayoutData['xaxis.range[1]']
        
        # Convert to datetime objects
        start_date = pd.to_datetime(start_date_str)
        end_date = pd.to_datetime(end_date_str)
        
        # Filter DataFrame based on selected range
        filtered_df = df_chf[(df_chf.index >= start_date) & (df_chf.index <= end_date)]
    else:
        # Default to full range if no relayoutData or range not present
        filtered_df = df_chf.copy()
        start_date = df_chf.index[0]
        end_date = df_chf.index[-1]

    # --- Normalization ---
    normalized_df = filtered_df.copy()
    if not normalized_df.empty:
        for col in normalized_df.columns:
            first_valid_value = normalized_df[col].iloc[0] # Use iloc[0] for the first value in the filtered range
            normalized_df[col] = 100 * (normalized_df[col] / first_valid_value)
    else:
        # Handle empty filtered_df case
        normalized_df = pd.DataFrame(columns=df_chf.columns)

    # --- CAGR Calculation ---
    cagr_values = {}
    if not filtered_df.empty:
        for col in filtered_df.columns:
            cagr_values[col] = calculate_cagr(filtered_df[col])
    
    # --- Create Plot ---
    fig = go.Figure()
    for col in normalized_df.columns:
        fig.add_trace(go.Scatter(
            x=normalized_df.index, 
            y=normalized_df[col],
            name=f"{col.replace('_', ' ')}"
        ))
        
    fig.update_layout(
        title=f"Normalized Performance ({start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')})",
        xaxis_title="Date",
        yaxis_title="Normalized Value (CHF)",
        xaxis_rangeslider_visible=True,
        template="plotly_dark"
    )

    # --- Prepare CAGR Output ---
    cagr_output_lines = [html.H3("CAGR (Compound Annual Growth Rate):")]
    if cagr_values:
        for name, cagr in cagr_values.items():
            cagr_output_lines.append(
                html.Div([
                    html.Span(f"{name.replace('_', ' ')}: ", style={'fontWeight': 'bold'}),
                    html.Span(f"{cagr:.2%}", style={'color': 'green'})
                ], style={'margin': '5px 10px'})
            )
    else:
        cagr_output_lines.append(html.P("No data for CAGR calculation in the selected range."))

    # --- Calculate and Prepare Final Value Output ---
    final_value_output_lines = [html.H3("Final Value of 100 CHF Investment:")]
    if not filtered_df.empty:
        for col in filtered_df.columns:
            start_value = filtered_df[col].iloc[0]
            end_value = filtered_df[col].iloc[-1]
            if start_value != 0:
                final_value = 100 * (end_value / start_value)
                final_value_output_lines.append(
                    html.Div([
                        html.Span(f"{col.replace('_', ' ')}: ", style={'fontWeight': 'bold'}),
                        html.Span(f"{final_value:.2f} CHF", style={'color': 'green'})
                    ], style={'margin': '5px 10px'})
                )
            else:
                final_value_output_lines.append(
                    html.Div([
                        html.Span(f"{col.replace('_', ' ')}: ", style={'fontWeight': 'bold'}),
                        html.Span("N/A (Start value is zero)", style={'color': 'red'})
                    ], style={'margin': '5px 10px'})
                )
    else:
        final_value_output_lines.append(html.P("No data for final value calculation in the selected range."))

    return fig, cagr_output_lines, final_value_output_lines

# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=True)
