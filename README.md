# plot_indices.py

This script fetches, processes, and visualizes financial market data to compare the performance of several major stock indices and gold, all converted to Swiss Francs (CHF).

## Functionality

The script performs the following main functions:

1.  **Data Fetching**: It retrieves historical daily closing prices for the following indices and commodities from Yahoo Finance (`yfinance`):
    *   DAX (Germany)
    *   S&P 500 Total Return (USA)
    *   SMI (Switzerland)
    *   CAC 40 (France)
    *   Gold

2.  **Currency Conversion**: It also fetches historical exchange rates for:
    *   EUR to CHF
    *   USD to CHF

    It then converts the prices of the foreign indices (DAX, S&P 500 TR, CAC 40) and Gold (priced in USD) into CHF.

3.  **Performance Normalization**: To provide a clear comparison of performance over time, the script normalizes the starting value of each index/commodity to 100. This allows for an easy visual comparison of their growth from the same starting point.

4.  **CAGR Calculation**: It calculates the Compound Annual Growth Rate (CAGR) for each of the CHF-denominated assets. The CAGR represents the mean annual growth rate of an investment over a specified period of time longer than one year.

5.  **Visualization**: The script generates an interactive plot using `plotly` that shows the normalized performance of all the assets over time. The plot includes a time-slider for easy navigation.

6.  **Output**:
    *   The interactive plot is displayed in a web browser.
    *   The calculated CAGR for each asset is printed to the console.

## How to Run

To run the script, simply execute it from your terminal:

```bash
python plot_indices.py
```

## Requirements

The script requires the following Python libraries:

*   `yfinance`: To fetch data from Yahoo Finance.
*   `pandas`: For data manipulation and analysis.
*   `plotly`: For creating the interactive plot.

You can install these dependencies using pip:

```bash
pip install yfinance pandas plotly
```
