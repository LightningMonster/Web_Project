from django.core.management.base import BaseCommand
import os
import csv
from datetime import datetime  # Import for parsing the date
from accounts.models import StockData  # Adjust based on your app and model location

class Command(BaseCommand):
    help = 'Import historical stock data from CSV files'

    def handle(self, *args, **kwargs):
        data_dir = os.path.join('accounts', 'management', 'commands', 'Collectors', 'historical_data')

        for filename in os.listdir(data_dir):
            if filename.endswith('.csv'):
                stock_symbol = filename.split('_')[0]  # Extract stock symbol from filename
                file_path = os.path.join(data_dir, filename)

                with open(file_path, 'r') as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        # Parse the date to extract only the date part
                        raw_date = row['Date']  # e.g., "2016-12-19 00:00:00+05:30"
                        parsed_date = datetime.strptime(raw_date.split(' ')[0], '%Y-%m-%d').date()

                        StockData.objects.create(
                            stock_symbol=stock_symbol,
                            date=parsed_date,
                            open=row['Open'],
                            high=row['High'],
                            low=row['Low'],
                            close=row['Close'],
                            volume=row['Volume'],
                            dividends=row.get('Dividends', 0),
                            stock_splits=row.get('Stock Splits', 0),
                        )
                self.stdout.write(self.style.SUCCESS(f"Data for {stock_symbol} imported successfully!"))
