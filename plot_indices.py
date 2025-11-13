import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# --- Data Fetching and Preparation ---
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
        "SMI": "^SSMI",
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
    df['SMI_CHF'] = df['SMI']
    df['GOLD_CHF'] = df['GOLD'] * df['USDCHF']

    return df[['DAX_CHF', 'SP500_TR_CHF', 'SMI_CHF', 'CAC40_CHF', 'GOLD_CHF']].dropna()

def calculate_cagr(series):
    """Calculates CAGR for a given series."""
    start_value = series.iloc[0]
    end_value = series.iloc[-1]
    num_years = (series.index[-1] - series.index[0]).days / 365.25
    if num_years == 0:
        return 0
    cagr = (end_value / start_value) ** (1 / num_years) - 1
    return cagr

def plot_performance():
    """Fetches data, creates a plot, and displays it."""
    df_chf = get_data()
    
    start_date = df_chf.index[0]
    end_date = df_chf.index[-1]
    
    # --- Normalization ---
    normalized_df = df_chf.copy()
    for col in normalized_df.columns:
        first_valid_value = normalized_df[col].loc[normalized_df[col].first_valid_index()]
        normalized_df[col] = 100 * (normalized_df[col] / first_valid_value)
        
    # --- CAGR Calculation ---
    cagr_values = {}
    for col in df_chf.columns:
        cagr_values[col] = calculate_cagr(df_chf[col])
        
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
        xaxis_rangeslider_visible=True
    )
    
    # --- Print CAGR Output ---
    print("CAGR (Compound Annual Growth Rate):")
    for name, cagr in cagr_values.items():
        print(f"{name.replace('_', ' ')}: {cagr:.2%}")

    fig.show()

if __name__ == '__main__':
    plot_performance()
