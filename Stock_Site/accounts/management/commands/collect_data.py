# collect_data.py 
# run command: python manage.py collect_data
"""
This Django management command collects stock data for multiple companies listed in a CSV file 
    and saves the historical stock data along with company details in CSV format.
"""
import pandas as pd
import yfinance as yf
import os
from django.core.management.base import BaseCommand # library for making file as a command 

class Command(BaseCommand): # file name as a command (python manage.py collect_data) we can run file entering command
    help = 'Read tickers from the input file and save all data about stock in the historical_data folder'

    # handle: This is the method that Django calls when executing the management command.
    def handle(self, *args, **kwargs):
        #self: Refers to the instance of the Command class.
        #*args: Collects any additional positional arguments passed to the command. (1 2 etc. [only if file needed command line argument.])
        #**kwargs: Collects any additional keyword arguments passed to the command. (--help, etc.)

        # Path of the input CSV file
        input_file = 'accounts/management/commands/Collectors/sources/test_stocks_list.csv'
        
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        # Path of the output folder
        output_dir = "accounts/management/commands/Collectors/historical_data"

        # Create a directory to save historical data if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Loop through each stock ticker
        for index, row in df.iterrows(): 
            #df.iterrows(): This method returns an iterator that generates each row of the DataFrame as a pair (index, row), 
            #where index is the index of the row and row is a pandas Series representing the row data.

            ticker = row["Ticker"] # Extracts the value of the "Ticker" column for the current row.
            print(f"Fetching data for {ticker}...") # Print ticker

            try:
                # Fetch stock data
                stock = yf.Ticker(ticker) # Creates a Ticker object for the specified stock ticker
                info = stock.info  # Get all available information

                # Extract relevant company details
                # .get() is used to avoid errors in case the key doesn't exist; if the key is not found, it returns None
                company_data = {

                    "Ticker": ticker, 
                    # Assigns the ticker

                    "Company Name": info.get("longName"), 
                    # Extracts the full company name

                    "Industry": info.get("industry"), 
                    # Retrieves the industry the company belongs to.

                    "Sector": info.get("sector"), 
                    # Extracts the sector

                    "CEO": info["companyOfficers"][0]['name'] if info.get("companyOfficers") else "N/A",
                    # Extracts the name of the CEO from the "companyOfficers" list, 
                    # specifically the first item ([0]) in the list, which typically contains the CEO's information. 
                    # If the "companyOfficers" key doesn't exist, it defaults to "N/A" using the ternary if expression.

                    "Headquarters": f"{info.get('city')}, {info.get('country')}",
                    # Combines the city and country information (e.g., "Cupertino, United States") to represent the company's headquarters.
                    
                    "Website": info.get("website"),
                    # Retrieves the company's website URL 

                    "Current Price": info.get("currentPrice"),
                    # Retrieves the current trading price of the stock

                    "Open Price": info.get("open"),
                    # Retrieves the opening price of the stock

                    "High": info.get("dayHigh"),
                    # Fetches the highest price the stock reached during the day

                    "Low": info.get("dayLow"),
                    # Retrieves the lowest price the stock reached during the day

                    "Market Cap": info.get("marketCap"),
                    # Extracts the company's market capitalization (total value of all outstanding shares)

                    "Volume": info.get("volume"),
                    # Retrieves the trading volume (number of shares traded) for the current day

                    "P/E Ratio": info.get("trailingPE"),
                    # Extracts the Price-to-Earnings (P/E) ratio, which compares the company's stock price to its earnings per share

                    "EPS": info.get("trailingEps"),
                    # Retrieves the earnings per share (EPS). EPS indicates the company's profitability.

                    "Dividend Yield": info.get("dividendYield"),
                    # Extracts the dividend yield (if available). This represents the annual dividend paid out as a percentage of the stock price.

                    "52-Week High": info.get("fiftyTwoWeekHigh"),
                    # Retrieves the highest stock price over the past 52 weeks

                    "52-Week Low": info.get("fiftyTwoWeekLow"),
                    # Fetches the lowest stock price over the past 52 weeks

                }

                # Fetch historical data
                historical_data = stock.history(period="max", interval="1d")
                # stock.history(...) - This method retrieves historical stock price data.
                # period = "max" - This specifies the maximum available historical data for the stock.
                # interval = "1d" - This sets the frequency of data points to one day (daily stock prices).

                if not historical_data.empty:
                    # Reset index to get Date as a column
                    historical_data.reset_index(inplace=True)
                    # history() returns a DataFrame where the index is Date by default.
                    # reset_index(inplace=True) moves the Date from the index to a regular column.

                    # Merge company info with historical data
                    for key, value in company_data.items():
                        historical_data[key] = value  # Add company info to each row

                    # Save merged data to a CSV file
                    output_file = os.path.join(output_dir, f'{ticker}_data.csv')
                    historical_data.to_csv(output_file, index=False) # index=False - prevents saving the default Pandas index.
                    print(f"Merged data for {ticker} saved successfully.")
                else:
                    print(f"No historical data available for {ticker}.")

            except Exception as e: # Catches any unexpected errors that occur during data fetching.
                print(f"Error fetching data for {ticker}: {e}")

        print("All stock data fetching completed.")

# Output should be like this
# Date,Open,High,Low,Close,Volume,Dividends,Stock Splits,Ticker,Company Name,Industry,Sector,CEO,Headquarters,Website,Current Price,Open Price,Market Cap,P/E Ratio,EPS,Dividend Yield,52-Week High,52-Week Low
