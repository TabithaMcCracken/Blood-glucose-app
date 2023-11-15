# Create an instance of the class
# Load the data from the csv file 
# Get the patient info and cgm data (into the instance of the class)

# Back the data up into the SQL database

# Condense the data to send to the OpenAI API

# Anazlyze the data ? (Pandas)

# Start an AI chat


import csv
from datetime import datetime
import sqlite3

file_path = "/Users/tabithamccracken/Documents/codingnomads/blood_glucose_app/cgm_data_one_day.csv"

# Define a class to store the data
class GlucoseData:
    def __init__(self, id, name, date_range, timestamp, glucose_value):
        self.id = id
        self.name = name
        self.date_range = date_range
        self.timestamp = timestamp
        self.glucose_value = glucose_value

# def load_data(self):
#         with open(self.file_path, "r", encoding='utf-8') as file:
#             csvreader = csv.reader(file)
#             self.patient_info_line = next(csvreader)
#             headers = next(csvreader)

#             for row in csvreader:
#                 time_stamp, glucose, _ = row  # We don't need the device info
#                 self.data.append((time_stamp, glucose)) 

#             for item in self.data:
#                 print(item)

# Function to read CSV file and create GlucoseData objects
def read_csv(file_path):
    glucose_data_list = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        
        # Read metadata (skip the first line)
        metadata_line = next(reader)
        name, date_range = None, None
        for item in metadata_line:
            if item.startswith('Name:'):
                name = item.split('Name:')[1].strip()
            elif item.startswith('Date Range:'):
                date_range = item.split('Date Range:')[1].strip()

        # Read actual column headers
        headers = next(reader)
        
        for row in reader:
            timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M')
            glucose_value = float(row[1])
            glucose_data = GlucoseData(id, name, date_range, timestamp, glucose_value)
            glucose_data_list.append(glucose_data)
    return glucose_data_list


def insert_into_database(data_list):
    connection = sqlite3.connect('/usr/local/mysql/data/glucose_data.db')
    cursor = connection.cursor()

    for data in data_list:
        cursor.execute(
            "INSERT INTO glucose_data (id, name, date_range, timestamp, glucose_value) VALUES (?, ?, ?, ?)",
            (data.name, data.date_range, data.timestamp, data.glucose_value)
        )

    connection.commit()
    connection.close()

if __name__ == "__main__":
    # Create instance of class with the current file path
    glucose_data_list = read_csv(file_path)

    if glucose_data_list:
        insert_into_database(glucose_data_list)
