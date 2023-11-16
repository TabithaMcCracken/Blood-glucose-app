# Create an instance of the class
# Load the data from the csv file 
# Get the patient info and cgm data (into the instance of the class)

# Back the data up into the SQL database

# Condense the data to send to the OpenAI API

# Anazlyze the data ? (Pandas)

# Start an AI chat


import csv
from datetime import datetime
import sqlalchemy
from secret import password
import pymysql
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, MetaData
from sqlalchemy.orm import declarative_base, Session

# Define the SQLAlchemy model
Base = declarative_base()


file_path = "/Users/tabithamccracken/Documents/codingnomads/blood_glucose_app/cgm_data_one_day.csv"
# Replace 'your_mysql_username', 'your_mysql_password', 'your_mysql_host', and 'your_mysql_database' with your MySQL credentials
mysql_engine = create_engine(f"mysql+mysqlconnector://root:{password}@localhost/glucose_data")

# sql_engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{password}@localhost/glucose_data')
# connection = sql_engine.connect()
# metadata = sqlalchemy.MetaData()


class GlucoseData(Base):
    __tablename__ = 'glucose_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    time_stamp = Column(DateTime)
    glucose_value = Column(Float)

# # Define a class to store the data
# class GlucoseData:
#     def __init__(self, id, name, timestamp, glucose_value):
#         self.id = id
#         self.name = name
#         self.timestamp = timestamp
#         self.glucose_value = glucose_value

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
            glucose_value = float(row[1])
            glucose_data = GlucoseData(
                name=patient_name,
                time_stamp=time_stamp,
                glucose_value=int(glucose_value)
            )
            glucose_data_list.append(glucose_data)
    return glucose_data_list


# def insert_into_database(metadata, engine, connection, glucose_data):
#     # Connect to local database
#     if glucose_data:
#         data_list = sqlalchemy.Table('glucose_data', metadata, autoload=True, autoload_with=engine)
#         query = sqlalchemy.insert(data_list)
#         result_proxy = connection.execute(query, glucose_data)

#     else:
#         print("There was no data, so no data was added to the database.")


def insert_into_database(data_list, engine):
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for data in data_list:
            session.add(data)
        session.commit()
    
if __name__ == "__main__":
    # Create instance of class with the current file path
    glucose_data_list = read_csv(file_path)

    # for item in glucose_data_list:
    #     print(f"Name: {item.name}")
    #     print(f"Timestamp: {item.time_stamp}")
    #     print(f"Glucose Value: {item.glucose_value}")

    if glucose_data_list:
        insert_into_database(glucose_data_list, mysql_engine)
