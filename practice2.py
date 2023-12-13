# This application allows the user to store cgm data to SQL database, get and 
# plot the last 24 hours of data from the database, or ask ChatGPT to analyze 
# the last 24 hours of data


import csv
from datetime import datetime, timedelta
import sqlalchemy
from secret import password
import pymysql
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, MetaData
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import func
import pandas as pd
import matplotlib.pyplot as plt
import plotille
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import openai
from secret import key
from token_count import num_tokens_from_string
import gzip
import json
from open_ai_chat import chat
import zlib


file_path = "/Users/tabithamccracken/Documents/codingnomads/blood_glucose_app/cgm_data_one_week.csv"

# Define the SQLAlchemy model
Base = declarative_base()

# Create the MySQL engine
mysql_engine = create_engine(f"mysql+mysqlconnector://root:{password}@localhost/glucose_data")

# OpenAI API key
openai.api_key = key

class GlucoseData(Base):
    __tablename__ = 'glucose_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    time_stamp = Column(DateTime, unique=True)
    glucose_value = Column(Float)
    
# Function to read CSV file and create GlucoseData objects
def read_csv(file_path):
    glucose_data_list = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        
        # Read metadata (skip the first line)
        metadata_line = next(reader)
        patient_name = None
        for item in metadata_line:
            if item.startswith('Name:'):
                patient_name = item.split('Name:')[1].strip()

        # Read actual column headers
        headers = next(reader)
        
        for row in reader:
            time_stamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M')
            glucose_amount = float(row[1])
            glucose_data = GlucoseData(
                name=patient_name,
                time_stamp=time_stamp,
                glucose_value=glucose_amount
            )
            glucose_data_list.append(glucose_data)
    return glucose_data_list

def insert_into_database(data_list, engine):
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for data in data_list:
            # Check for duplicates before adding to the session
            try:
                existing_entry = (
                    session.query(GlucoseData)
                    .filter_by(name=data.name, time_stamp=data.time_stamp)
                    .one()
                )
                # If entry already exists, skip adding the duplicate
                print(f"Duplicate entry found for {data.name} at {data.time_stamp}. Skipping.")
            except NoResultFound:
                # If no duplicate found, add the data to the session
                session.add(data)
                

        session.commit()
    print("Data added to the database.")

def get_data_from_database(engine):
    with Session(engine) as session:
        # Query all data from the database
        query_result = session.query(GlucoseData).all()

        # Convert the query result to a Pandas DataFrame
        data_frame = pd.DataFrame([(data.id, data.name, data.time_stamp, data.glucose_value) for data in query_result],
                            columns=['id', 'name', 'time_stamp', 'glucose_value'])
    return data_frame

def get_last_24_hours_data (data_frame):

    # Ensure that 'time_stamp' column is in datetime format
    data_frame['time_stamp'] = pd.to_datetime(data_frame['time_stamp'])

    # Sort DataFrame by time_stamp for proper plotting
    data_frame = data_frame.sort_values(by='time_stamp')

    # Find the maximum timestamp in the data
    max_timestamp = data_frame['time_stamp'].max()

    # Filter DataFrame to include only the last 24 hours' data
    last_24_hours_data = data_frame[data_frame['time_stamp'] >= (max_timestamp - pd.DateOffset(days=1))]    

    for item in last_24_hours_data:
        print(item)
    
    return last_24_hours_data

def convert_dataframe_to_string(data_frame):
    string_data = ""
    for index, row in data_frame.iterrows():
        string_data += f"{row['time_stamp'], {row['glucose_value']}}\n"

    return string_data.strip()

def convert_dataframe_to_compressed_string(data_frame):
    """
    Convert a Pandas DataFrame to a compressed string.

    Parameters:
    - data_frame (pd.DataFrame): The DataFrame to be converted.

    Returns:
    - str: Compressed string representation of the DataFrame.
    """
    # Use a shorter time format
    data_frame['time_stamp'] = data_frame['time_stamp'].str.split('T').str[0]

    # Convert DataFrame to a string with a comma as a delimiter
    string_data = data_frame.to_csv(index=False)

    # Compress the string
    compressed_data = zlib.compress(string_data.encode('utf-8'))

    # Convert compressed bytes to a string
    compressed_string = compressed_data.decode('utf-8')

    return compressed_string

def plot_data_from_database_with_matplotlib(last_24_hours_data):

    if last_24_hours_data.empty:
        print("No data available in the database.")

    else:

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(last_24_hours_data['time_stamp'], last_24_hours_data['glucose_value'], marker='o', linestyle='-', color='b')
        plt.title('Blood Glucose Levels Over Time')
        plt.xlabel('Time Stamp')
        plt.ylabel('Glucose Value')
        plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: int(x)))# Set y-axis ticks to be integers
        plt.xticks(rotation=45, fontsize = 8)# Set x-axis ticks to 45 degrees and size 8
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))# Reformat the timestamp on x-axis labels
        plt.grid(True)
        plt.tight_layout()

        # Show the plot
        plt.show()

def plot_data_from_database_with_plotille(last_24_hours_data):

    if last_24_hours_data.empty:
        print("No data available in the database.")

    else:

        time_stamps = last_24_hours_data['time_stamp']
        glucose_values = last_24_hours_data['glucose_value']

        # Reformats to integers
        def _num_formatter(val, chars, delta, left=False):
            align = '<' if left else ''
            return '{:{}{}d}'.format(int(val), align, chars)

        # Plot using plotille
        plot = plotille.Figure()
        plot.width = 80
        plot.height = 30
        plot.register_label_formatter(float, _num_formatter) # Reformat to integer
        plot.register_label_formatter(int, _num_formatter) # Reformat to integer
        plot.set_x_limits(min(time_stamps), max(time_stamps))
        plot.set_y_limits(min(glucose_values), max(glucose_values) + 10)
        plot.plot(time_stamps, glucose_values, lc='red')
        print(plot.show(legend=True))

    
if __name__ == "__main__":
    while True:
        user_input = int(input(
            "What would you like to do?\n"
            "1) Upload data from a csv file to the database\n"
            "2) Plot the last 24 hours of uploaded data on the command line\n"
            "3) Plot the last 24 hours of data with Matplotlib\n"
            "4) Ask ChatGPT to analyze the most recent days data\n"
            "5) Exit the program\n"
        ))

        if user_input == 1:
            # Get data from CSV file
            glucose_data_list = read_csv(file_path)

            # Put data into database
            if glucose_data_list:
                insert_into_database(glucose_data_list, mysql_engine)

        elif user_input == 2:
            # Get the data from the database and put into a dataframe
            client_data = get_data_from_database(mysql_engine)

            # Get just the last 24 hours of data
            last_24_hours_data = get_last_24_hours_data(client_data)

            # Plot the data from the database with Plotille
            plot_data_from_database_with_plotille(last_24_hours_data)
            

        elif user_input == 3:
            # Get the data from the database and put into a dataframe
            client_data = get_data_from_database(mysql_engine)

            # Get just the last 24 hours of data
            last_24_hours_data = get_last_24_hours_data(client_data)

            # Plot the data from the database with Matplotlib
            plot_data_from_database_with_matplotlib(client_data)


        elif user_input ==4:
            # Get the data from the database and put into a dataframe
            client_data = get_data_from_database(mysql_engine)

            # Get just the last 24 hours of data
            last_24_hours_data = get_last_24_hours_data(client_data)

            # Condense the data
            condensed_string_data = convert_dataframe_to_compressed_string (last_24_hours_data)

            # Check the token count of the condensed data
            token_count = num_tokens_from_string(str(condensed_string_data))
            print(f"Token count of the condensed data: {token_count}")

            # if token_count < 3000:
            #     ai_response = chat(condensed_string_data)

        elif user_input == 5:
            break

        else:
            print("Invalid input, please try again.")
    





