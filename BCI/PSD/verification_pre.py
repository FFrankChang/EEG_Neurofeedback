import re
import numpy as np
import csv

# Function to parse all frequency bands and calculate their averages
def parse_all_bands(line):
    # Extracting each band array using regular expressions and computing their means
    band_means = {}
    for band in ['alpha', 'beta', 'theta', 'delta']:
        match = re.search(fr"'{band}': array\((\[.*?\])\)", line)
        if match:
            array_str = match.group(1)
            array = np.fromstring(array_str.strip('[]'), sep=', ')
            band_means[band] = array.mean()
    return band_means

# Input file path
input_file_path = 'power_bands_final_2.csv'  # Update this path with your actual file path
# Output file path
output_file_path = '11111.csv'  # Update this path with your desired output path

# Open the input file to read, and the output file to write
with open(input_file_path, 'r') as infile, open(output_file_path, 'w', newline='') as outfile:
    csv_writer = csv.writer(outfile)
    # Write the header
    csv_writer.writerow(['alpha_mean', 'beta_mean', 'theta_mean', 'delta_mean'])
    # Process each line in the input file
    for line in infile:
        band_means = parse_all_bands(line.strip())
        if band_means:
            # Write the computed means to the CSV
            csv_writer.writerow([band_means.get('alpha'), band_means.get('beta'), 
                                 band_means.get('theta'), band_means.get('delta')])
