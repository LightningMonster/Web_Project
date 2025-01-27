import pandas as pd

# Load the CSV file (replace 'your_file.csv' with your actual file path)
df = pd.read_csv('indian_stock_tickers.csv')

# Create a new DataFrame to store the reformatted data
output_data = []

# Loop through each row in the original data
for index, row in df.iterrows():
    symbol = row['symbol']
    name = row['Name']

    # Create entries for both BO and NS markets
    output_data.append([name, "BO", f"{symbol}.BO"])
    output_data.append([name, "NS", f"{symbol}.NS"])

# Convert the list to a DataFrame
output_df = pd.DataFrame(output_data, columns=["Name", "Market", "Ticker"])

# Save the reformatted data to a CSV file
output_df.to_csv('reformatted_stock_data.csv', index=False)

# Print message after saving
print("Data saved to reformatted_stock_data.csv")
