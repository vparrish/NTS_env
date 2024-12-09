import csv
from collections import defaultdict
from datetime import datetime
from dateutil import parser
import pandas as pd

def reformat_csv(input_file, output_file, uniform_time_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file, header=None)

    # Display the DataFrame
    print(df)
    
    # Convert the DataFrame to a CSV file
    df.to_csv(output_file, index=False, header=False)

    # Function to clean and convert time to a uniform format
    def convert_time(time_str):
        try:
            # Remove any incorrect "AM" or "PM" suffixes if the time is in 24-hour format
            if 'AM' in time_str or 'PM' in time_str:
                time_str = time_str.replace(' AM', '').replace(' PM', '')
            return parser.parse(time_str).strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Error parsing time: {time_str}, error: {e}")
            return time_str

    # Read the CSV file into a DataFrame
    df = pd.read_csv(output_file, header=None)

    # Apply the conversion function to the 'Time' column
    df[2] = df[2].apply(convert_time)  # Assuming 'Time' is the third column (index 2)

    # Save the updated DataFrame back to a CSV file
    df.to_csv(uniform_time_file, index=False, header=False)


def process_csv(input_file, output_file):
    data = {}

    # Read the input CSV file
    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            quad_color = row['Quad Color']
            wire_pair = row['Wire Pair']
            date = datetime.strptime(row['Time'], '%Y-%m-%d %H:%M:%S').date()
            temp = float(row['Temp [C]']) if row['Temp [C]'] else None
            humidity = row['Humidity ']
            air_temp = temp  # Assuming air temperature is the same as the measured temperature

            if temp is not None:
                key = (quad_color, wire_pair, date)
                if key not in data:
                    data[key] = (temp, humidity, air_temp)

    # Prepare the output data
    output_data = []
    cable_length_km = 2
    for (quad_color, wire_pair, date), (temp, humidity, air_temp) in data.items():
        wire_temp = temp + (cable_length_km / 2)
        output_data.append([quad_color, wire_pair, date, wire_temp, air_temp, humidity])

    # Write the output CSV file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Quad Color', 'Wire Pair', 'Date', 'Wire Temp [C]', 'Air Temp [C]', 'Humidity'])
        writer.writerows(output_data)


# USAGE
reformat_csv('/home/victoria/work/icecube/service/nts/NTS_VNA/csv/8.12.24_12.05.24_no_outlier.csv', '/home/victoria/work/icecube/service/nts/NTS_VNA/csv/output.csv', '/home/victoria/work/icecube/service/nts/NTS_VNA/csv/output_uniform_time.csv')
process_csv('/home/victoria/work/icecube/service/nts/NTS_VNA/csv/output_uniform_time.csv', '/home/victoria/work/icecube/service/nts/NTS_VNA/csv/new_processed_output.csv')