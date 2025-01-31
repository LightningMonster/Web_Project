# import_stock_data.py
# run command: python manage.py import_stock_data

"""
This Django management command imports historical stock data from CSV files 
and saves the data into the database.
"""

from django.core.management.base import BaseCommand # library for making file as a command
import os
import csv
from datetime import datetime
from accounts.models import StockData
from decimal import Decimal, InvalidOperation

def safe_decimal(value):
    try:
        if value:
            return Decimal(value)
            # If value is not empty or None, it attempts to convert value into a Decimal.
        else:
            return Decimal('0.00') 
            # If value is empty (None, '', etc.), it returns Decimal('0.00') instead.
    except (InvalidOperation, TypeError): 
        return Decimal('0.00')

class Command(BaseCommand): # file name as a command (python manage.py import_data) we can run file entering command
    help = 'Import historical stock data from CSV files'

    # handle: This is the method that Django calls when executing the management command.
    def handle(self, *args, **kwargs):
        #self: Refers to the instance of the Command class.
        #*args: Collects any additional positional arguments passed to the command. (1 2 etc. [only if file needed command line argument.])
        #**kwargs: Collects any additional keyword arguments passed to the command. (--help, etc.)

        # directory path
        data_dir = os.path.join('accounts', 'management', 'commands', 'Collectors', 'historical_data')

        for filename in os.listdir(data_dir): # os.listdir(data_dir) returns a list of all the files and directories in the data_dir directory.
            
            if filename.endswith('.csv'): # This checks if the filename ends with the .csv extension.
                
                stock_symbol = filename.split('_')[0] 
                # This line splits the filename into parts using the underscore (_) as the separator.
                # It then takes the first part (index [0]), which contains stock ticker

                file_path = os.path.join(data_dir, filename)
                # This joins the data_dir path with the filename, creating the full path to the file.
                # For saving historical data in that perticular CSV file.

                with open(file_path, 'r') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        raw_date = row['Date']
                        parsed_date = datetime.strptime(raw_date.split(' ')[0], '%Y-%m-%d').date()

                        # Check if the record already exists in the database
                        if not StockData.objects.filter(stock_symbol=stock_symbol, date=parsed_date).exists():
                            # Use safe_decimal to handle invalid values and handle new fields
                            StockData.objects.create(
                                stock_symbol=stock_symbol,
                                date=parsed_date,
                                open=safe_decimal(row['Open']),
                                high=safe_decimal(row['High']),
                                low=safe_decimal(row['Low']),
                                close=safe_decimal(row['Close']),
                                volume=safe_decimal(row['Volume']),
                                dividends=safe_decimal(row.get('Dividends', 0)),
                                stock_splits=safe_decimal(row.get('Stock Splits', 0)),
                                company_name=row.get('Company Name', ''),
                                industry=row.get('Industry', ''),
                                sector=row.get('Sector', ''),
                                ceo=row.get('CEO', ''),
                                headquarters=row.get('Headquarters', ''),
                                website=row.get('Website', ''),
                                market_cap=safe_decimal(row.get('Market Cap', 0)),
                                pe_ratio=safe_decimal(row.get('P/E Ratio', 0)),
                                eps=safe_decimal(row.get('EPS', 0)),
                                dividend_yield=safe_decimal(row.get('Dividend Yield', 0)),
                                fifty_two_week_high=safe_decimal(row.get('52 Week High', 0)),
                                fifty_two_week_low=safe_decimal(row.get('52 Week Low', 0)),
                            )
                            self.stdout.write(self.style.SUCCESS(f"Data for {stock_symbol} on {parsed_date} imported successfully!"))
                        else:
                            self.stdout.write(self.style.SUCCESS(f"Data for {stock_symbol} on {parsed_date} already exists. Skipping."))
