from django.core.management.base import BaseCommand
import os
import csv
from datetime import datetime
from accounts.models import StockData
from decimal import Decimal, InvalidOperation

def safe_decimal(value):
    try:
        return Decimal(value) if value else Decimal('0.00')
    except (InvalidOperation, TypeError):
        return Decimal('0.00')

class Command(BaseCommand):
    help = 'Import historical stock data from CSV files'

    def handle(self, *args, **kwargs):
        data_dir = os.path.join('accounts', 'management', 'commands', 'Collectors', 'historical_data')

        for filename in os.listdir(data_dir):
            if filename.endswith('.csv'):
                stock_symbol = filename.split('_')[0]
                file_path = os.path.join(data_dir, filename)

                with open(file_path, 'r') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        raw_date = row['Date']
                        parsed_date = datetime.strptime(raw_date.split(' ')[0], '%Y-%m-%d').date()

                        # Check if the record already exists in the database
                        if not StockData.objects.filter(stock_symbol=stock_symbol, date=parsed_date).exists():
                            # Use safe_decimal to handle invalid values
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
                            )
                            self.stdout.write(self.style.SUCCESS(f"Data for {stock_symbol} on {parsed_date} imported successfully!"))
                        else:
                            self.stdout.write(self.style.SUCCESS(f"Data for {stock_symbol} on {parsed_date} already exists. Skipping."))
