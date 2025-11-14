import pandas as pd
import yfinance as yf

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
