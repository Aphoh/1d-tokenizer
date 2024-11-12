import os
import re
import pandas as pd

# Directory containing the text files
directory = '.'

# Regular expressions to match alpha, beta, and metrics
filename_pattern = re.compile(r'rar_b_alpha([0-9e\.-]+)_beta([0-9e\.-]+)_eval\.txt')
metrics_pattern = re.compile(r'Inception Score: ([\d.]+)|FID: ([\d.]+)|sFID: ([\d.]+)|Precision: ([\d.]+)|Recall: ([\d.]+)')

# List to store all data
data = []

# Loop through files in directory
for filename in os.listdir(directory):
    if filename.endswith('eval.txt'):
        filepath = os.path.join(directory, filename)

        # Extract alpha and beta from filename
        match = filename_pattern.search(filename)
        if match:
            alpha, beta = match.groups()

        else:
            print(f'Filename {filename} does not match pattern, treating as baseline')
            alpha, beta = 0, 0

        # Read file and extract metrics
        with open(filepath, 'r') as file:
            file_content = file.read()
            metrics = [None] * 5  # Initialize list for Inception Score, FID, sFID, Precision, Recall

            # Use regex to find metric values
            for m in metrics_pattern.finditer(file_content):
                for i, val in enumerate(m.groups()):
                    if val is not None:
                        metrics[i] = float(val)

            if all(m is not None for m in metrics):
                print(f'File {filename} contains all metrics')
                # Append row to data list
                data.append([alpha, beta] + metrics)
            else:
                print(f'File {filename} is missing metrics, skipping')

# Convert data to DataFrame and save to CSV
df = pd.DataFrame(data, columns=['alpha', 'beta', 'Inception Score', 'FID', 'sFID', 'Precision', 'Recall'])
df.to_csv('output.csv', index=False)