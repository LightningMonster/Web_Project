import pandas as pd
import yfinance as yf
import os

# Load the CSV file
# original input file
# df = pd.read_csv("accounts/management/commands/Collectors/sources/indian_stocks_list.csv")

# test input file
df = pd.read_csv('accounts/management/commands/Collectors/sources/test_stocks_list.csv')
# Create a directory to save historical data if it doesn't exist
if not os.path.exists("accounts/management/commands/Collectors/historical_data"):
    os.makedirs("accounts/management/commands/Collectors/historical_data")

# Loop through each stock ticker
for index, row in df.iterrows():
    ticker = row["Ticker"]
    print(f"Fetching historical data for {ticker}...")

    try:
        # Fetch the stock data (replace the content each time)
        stock_data = yf.Ticker(ticker)
        historical_data = stock_data.history(period="max", interval="1d")  # Only fetch the "max" period

        # Save the historical data to a CSV file (replacing previous content)
        if not historical_data.empty:
            historical_data.to_csv(f'accounts/management/commands/Collectors/historical_data/{ticker}_historical_data.csv')
            print(f"Data for {ticker} saved successfully.")
        else:
            print(f"No data available for {ticker}.")

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")

print("All historical data fetching completed.")
