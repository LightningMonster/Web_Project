# accounts/management/commands/Collectors/stos.py
import pandas as pd
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Reformat Indian stock data and save to a CSV file'

    def handle(self, *args, **kwargs):
        # Load the CSV file (replace 'your_file.csv' with your actual file path)
        df = pd.read_csv('accounts/management/commands/Collectors/sources/indian_stocks_list.csv')

        # Create a new DataFrame to store the reformatted data
        output_data = []

        # Loop through each row in the original data
        for index, row in df.iterrows():
            symbol = row['Ticker']
            
            # Create entries for both BO and NS markets (but include only ticker)
            output_data.append([f"{symbol}.BO"])
            output_data.append([f"{symbol}.NS"])

        # Convert the list to a DataFrame with only 'Ticker' column
        output_df = pd.DataFrame(output_data, columns=["Ticker"])

        # Save the reformatted data to a CSV file
        output_df.to_csv('accounts/management/commands/Collectors/sources/reformatted_stock_data.csv', index=False)

        # Print message after saving
        self.stdout.write(self.style.SUCCESS('Data saved to reformatted_stock_data.csv'))
