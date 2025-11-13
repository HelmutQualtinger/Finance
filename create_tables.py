import yfinance as yf
import pandas as pd
from datetime import datetime

# Download DAX data from inception to today
dax = yf.download('^GDAXI', period='max', interval='1mo')['Close']

# Round to 2 decimals
dax = dax.round(2)

# Convert index to ISO strings
dax.index = dax.index.strftime('%Y-%m-%d')

# Convert to dict
dax_dict = dax.to_dict()

# The dictionary
dax_dict