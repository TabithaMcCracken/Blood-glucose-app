
# Load the data from the csv file 
# Get the patient info and cgm data (into the instance of the class)

# Back the data up into the SQL database

# Anazlyze the data with Pandas
# Analyze the data with Plotille

# Condense the data to send to the OpenAI API
# Start an AI chat


import csv
from datetime import datetime
import sqlalchemy
from secret import password
import pymysql
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, MetaData
from sqlalchemy.orm import declarative_base, Session
import pandas as pd
import matplotlib.pyplot as plt
import plotille
from sqlalchemy.orm import sessionmaker
import matplotlib.ticker as ticker
import matplotlib.dates as mdates


file_path = "/Users/tabithamccracken/Documents/codingnomads/blood_glucose_app/cgm_data_one_day.csv"

# Define the SQLAlchemy model
Base = declarative_base()

# Create the MySQL engine
mysql_engine = create_engine(f"mysql+mysqlconnector://root:{password}@localhost/glucose_data")


class GlucoseData(Base):
    __tablename__ = 'glucose_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    time_stamp = Column(DateTime)
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
            session.add(data)
        session.commit()
    

def plot_data_from_database_with_matplotlib(engine):
    with Session(engine) as session:
        # Query all data from the database
        query_result = session.query(GlucoseData).all()

        # Convert the query result to a Pandas DataFrame
        df = pd.DataFrame([(data.id, data.name, data.time_stamp, data.glucose_value) for data in query_result],
                            columns=['id', 'name', 'time_stamp', 'glucose_value'])

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

    # Query the data from the database
    query_result = session.query(GlucoseData).all()

    # Extract timestamps and glucose values from the query result
    timestamps = [data.time_stamp for data in query_result]
    glucose_values = [data.glucose_value for data in query_result]

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
    
    session.close()


if __name__ == "__main__":
    # Get data from CSV file
    glucose_data_list = read_csv(file_path)

    # Put data into database
    # if glucose_data_list:
    #     insert_into_database(glucose_data_list, mysql_engine)

    # Plot the data from the database with Matplotlib
    plot_data_from_database_with_matplotlib(mysql_engine)

    # Plot the data from the database with Plotille
    # plot_data_from_database_with_plotille(mysql_engine)



