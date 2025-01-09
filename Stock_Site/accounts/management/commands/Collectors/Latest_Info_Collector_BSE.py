from bsedata.bse import BSE
from bsedata.exceptions import InvalidStockException
import csv

# Instantiate BSE
b = BSE(update_codes=True)

# Define the path of the input CSV file containing scrip codes and the output CSV file
csv_input_file = 'Stock Craweler/Collectors/sources/stock_data.csv'  # Change this to your actual input CSV file path
csv_output_file = 'latest_data/latest_stock_data.csv'

# List to store fieldnames for CSV
fieldnames = None

# Read scrip codes from the CSV file and fetch data
with open(csv_input_file, mode='r', encoding='utf-8') as infile, open(csv_output_file, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    writer = None

    for row in reader:
        scrip_code = row['scripCode']  # Assuming the column header is 'scripCode'

        try:
            # Fetch the quote for the given scrip code
            quote = b.getQuote(scrip_code)

            # Initialize the CSV writer and fieldnames if not already done
            if writer is None:
                fieldnames = list(quote.keys())
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()

            # Write the stock information as a row in the CSV
            writer.writerow(quote)
            print(f'Saved data for {scrip_code} in {csv_output_file}')

        except InvalidStockException:
            # Skip inactive stocks
            print(f'Skipped inactive stock: {scrip_code}')
        except Exception as e:
            # Handle other potential exceptions
            print(f'Error fetching data for {scrip_code}: {e}')

print('All stock data has been saved to CSV.')
