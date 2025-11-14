# Finance Data Analysis

This project contains scripts to fetch, analyze, and plot financial data.

## Scripts

- `plot_indices.py`: Fetches financial data from Yahoo Finance, calculates CAGR, and plots the normalized performance of several indices in CHF.
- `dash_app.py`: An interactive Dash web application that visualizes the normalized performance of various financial indices in CHF. It includes features such as:
    - Normalized performance charts with date range selection.
    - Compound Annual Growth Rate (CAGR) calculation for the selected period.
    - Calculation of the final value of an initial 100 CHF investment for the selected period.
    To run the application:
    ```bash
    python dash_app.py
    ```
    Access it in your web browser, usually at `http://127.0.0.1:8050/`.

## Data

The project uses several data files in various formats (`.xls`, `.pdf`, `.csv`, `.json`, `.txt`) as data sources.