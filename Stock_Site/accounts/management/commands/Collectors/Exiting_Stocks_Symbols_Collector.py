#Getting symbols of stocks whos historical data is locally available
#and saved in Available_Stocks_Info.csv

import os
import csv

# Directory path where the files are stored
directory = 'historical_data/'

# List to store the names of files without full extensions
file_names = []

# Loop through each file in the directory
for filename in os.listdir(directory):
    if '.BO' in filename or '.NS' in filename:
        # Split the filename at '.BO' or '.NS' and take the part before it
        if '.BO' in filename:
            name = filename.split('.BO')[0] + '.BO'
        elif '.NS' in filename:
            name = filename.split('.NS')[0] + '.NS'
        file_names.append([name])  # Storing as a list for CSV

# Save the file names to a CSV file
with open('sources/Available_Stocks_Info.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Stock Symbol'])  # Header row
    writer.writerows(file_names)

print("File names saved to 'Available_Stocks_Info.csv'")
