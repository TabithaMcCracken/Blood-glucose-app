
# Load the data from the csv file 
# Get the patient info and cgm data (into the instance of the class)

# Back the data up into the SQL database

# Anazlyze the data with Pandas
# Analyze the data with Plotille

# Condense the data to send to the OpenAI API
# Start an AI chat


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
        df = pd.DataFrame([(data.id, data.name, data.time_stamp, data.glucose_value) for data in query_result],
                            columns=['id', 'name', 'time_stamp', 'glucose_value'])
        
    return df
 
def plot_data_from_database_with_matplotlib(df):

        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(df['time_stamp'], df['glucose_value'], marker='o', linestyle='-', color='b')
        plt.title('Blood Glucose Levels Over Time')
        plt.xlabel('Time Stamp')
        plt.ylabel('Glucose Value')

        # Set y-axis ticks to be integers
        plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: int(x)))
        # Set x-axis ticks to 45 degrees and size 8
        plt.xticks(rotation=45, fontsize = 8)

        # Reformat the timestamp on x-axis labels
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

        plt.grid(True)
        plt.tight_layout()

        # Show the plot
        plt.show()

def plot_data_from_database_with_plotille(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Get the maximum timestamp in the database
    max_timestamp = session.query(func.max(GlucoseData.time_stamp)).scalar()

    if max_timestamp is not None:

        # Calculate the start and end dates for filtering (from midnight to the end of the last day)
        start_date = max_timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = max_timestamp.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Query the data from the database for the last day
        query_result = session.query(GlucoseData).filter(GlucoseData.time_stamp.between(start_date, end_date)).all()


        timestamps = [data.time_stamp for data in query_result]
        glucose_values = [data.glucose_value for data in query_result]

        # print(timestamps)
        print("Min Timestamp:", min(timestamps))
        print("Max Timestamp:", max(timestamps))

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
        plot.set_x_limits(min(timestamps), max(timestamps))
        plot.set_y_limits(min(glucose_values), max(glucose_values) + 10)
        plot.plot(timestamps, glucose_values, lc='red')
        # plot.scatter(timestamps, glucose_values, lc='red')
        print(plot.show(legend=True))
    
    else:
        print("No data available in the database.")

    session.close()
    # print()

# Function to get condensed data from the MySQL database
def get_condensed_data(engine):
    with Session(engine) as session:
        # Query the database to get relevant data
        # query_result = session.query(GlucoseData).all()

        # Get the maximum timestamp in the database
        max_timestamp = session.query(func.max(GlucoseData.time_stamp)).scalar()
        # Calculate the start and end dates for filtering (from midnight to the end of the last day)
        start_date = max_timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = max_timestamp.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Query the data from the database for the last day
        query_result = session.query(GlucoseData).filter(GlucoseData.time_stamp.between(start_date, end_date)).all()


        # Extract relevant information for condensation
        glucose_data_strings = [
            (entry.time_stamp.strftime('%H:%M:%S'), int(entry.glucose_value))
            for entry in query_result
        ]

        return glucose_data_strings
    
# if __name__ == "__main__":
#     while True:
#         user_input = int(input(
#             "What would you like to do?\n"
#             "1) Upload data from a csv file to the database\n"
#             "2) Plot the most recent days data\n"
#             "3) Ask ChatGPT to analyze the most recent days data\n"
#             "4) Exit the program\n"
#         ))

#         if user_input == 1:
#             # Get data from CSV file
#             glucose_data_list = read_csv(file_path)

#             # Put data into database
#             if glucose_data_list:
#                 insert_into_database(glucose_data_list, mysql_engine)

#         elif user_input == 2:
#             # Plot the data from the database with Plotille
#             plot_data_from_database_with_plotille(mysql_engine)

#         elif user_input ==3:
#             condensed_data = get_condensed_data(mysql_engine)

#             # Check the token count of the condensed data
#             token_count = num_tokens_from_string(str(condensed_data))
#             print(f"Token count of the condensed data: {token_count}")

#             if token_count < 3000:
#                 ai_response = chat(condensed_data)

#         elif user_input == 4:
#             break

#         else:
#             print("Invalid input, please try again.")
    


# Plot the data from the database with Matplotlib
client_data = get_data_from_database(mysql_engine)
plot_data_from_database_with_matplotlib(client_data)



