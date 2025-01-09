from bsedata.bse import BSE
from bsedata.exceptions import InvalidStockException
import csv

# Instantiate BSE and update scrip codes
b = BSE(update_codes=True)

# Get all scrip codes (BSE codes) and company names
scrip_codes = b.getScripCodes()

# Create a list to hold the stock data
stock_data = []

# Iterate over the scrip codes to populate the stock_data list
for bse_code, company_name in scrip_codes.items():
    try:
        # Fetch the quote to get the security ID
        quote = b.getQuote(bse_code)
        if 'securityID' in quote:
            # Append a tuple of (scripCode, companyName, securityID) to the list
            stock_data.append((bse_code, company_name, quote['securityID']))
    except InvalidStockException:
        # Skip inactive stocks
        print(f'Skipped inactive stock: {company_name} (BSE Code: {bse_code})')
    except Exception as e:
        # Handle other potential exceptions
        print(f'Error fetching data for {company_name} (BSE Code: {bse_code}): {e}')

# Define the CSV file path
csv_file_path = 'sources/stock_data.csv'

# Write the stock data to a CSV file
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(['scripCode', 'companyName', 'securityID'])
    # Write the stock data
    writer.writerows(stock_data)

print(f'Stock data saved to {csv_file_path}')
