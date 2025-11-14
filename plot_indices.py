import plotly.graph_objects as go
from finance_analyzer import get_data, calculate_cagr

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
            name="{}".format(col.replace('_', ' '))
        ))
        
    fig.update_layout(
        title="Normalized Performance ({} to {})".format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')),
        xaxis_title="Date",
        yaxis_title="Normalized Value (CHF)",
        xaxis_rangeslider_visible=True
    )
    
    # --- Print CAGR Output ---
    print("CAGR (Compound Annual Growth Rate):")
    for name, cagr in cagr_values.items():
        print("{}: {:.2%}".format(name.replace('_', ' '), cagr))

    fig.show()

if __name__ == '__main__':
    plot_performance()
