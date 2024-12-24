import pandas as pd

# Specify the path to the CSV file
file_path = 'data/raw/31a3ab4a-279d-4767-97ad-93db6a708d68.csv'

# Read the CSV file into a pandas DataFrame
data = pd.read_csv(file_path)

# Display the first 5 rows of the data to check if it's loaded correctly
print(data.head(10))