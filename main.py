import pandas as pd
import numpy as np
import yfinance as yf

# Function to fetch historical stock data
def get_stock_data(symbol, start_date, end_date):
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        return stock_data['Adj Close']
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.Series(name=symbol)

# Function to calculate returns
def calculate_returns(stock_prices):
    return stock_prices.pct_change().dropna()

# Function to calculate correlation matrix
def calculate_correlation_matrix(returns):
    return returns.corr()

# Function to select uncorrelated stocks
def select_uncorrelated_stocks(correlation_matrix, num_stocks):
    selected_stocks = []

    for _ in range(num_stocks):
        # Find the pair of stocks with the minimum correlation
        min_correlation_pair = np.unravel_index(np.argmin(correlation_matrix.to_numpy(), axis=None), correlation_matrix.shape)

        # Select the stock from the pair
        selected_stock = min_correlation_pair[1]

        # Update the correlation matrix by setting the correlation of the selected stock to 1
        correlation_matrix.iloc[min_correlation_pair[0], :] = 1
        correlation_matrix.iloc[:, min_correlation_pair[1]] = 1

        selected_stocks.append(selected_stock)

    return selected_stocks

# Main function
def main():
    # Define the NIFTY stocks
    nifty_stocks = ['TCS.NS', 'HDFCBANK.NS', 'RELIANCE.NS', 'INFY.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'KOTAKBANK.NS',
                    'ITC.NS', 'LT.NS', 'AXISBANK.NS', 'SBIN.NS', 'BAJFINANCE.NS', 'MARUTI.NS', 'BHARTIARTL.NS',
                    'NTPC.NS', 'ONGC.NS', 'WIPRO.NS', 'INDUSINDBK.NS', 'SUNPHARMA.NS']

    # Set the date range for historical data
    start_date = '2022-01-01'
    end_date = '2023-01-01'

    # Fetch stock data
    stock_data = pd.DataFrame({stock: get_stock_data(stock, start_date, end_date) for stock in nifty_stocks})

    # Remove stocks with missing data
    stock_data = stock_data.dropna(axis=1, how='all')

    if stock_data.empty:
        print("No valid data available for the specified stocks.")
        return

    # Calculate returns
    returns = calculate_returns(stock_data)

    # Calculate correlation matrix
    correlation_matrix = calculate_correlation_matrix(returns)

    # Select 5 most uncorrelated stocks
    selected_stocks = select_uncorrelated_stocks(correlation_matrix, 5)

    # Display the selected stocks
    print("Selected Stocks:")
    for stock_index in selected_stocks:
        print(nifty_stocks[stock_index])

if __name__ == "__main__":
    main()
