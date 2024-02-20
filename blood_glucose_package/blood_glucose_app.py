import os
import csv
from datetime import datetime, timedelta
# import sqlalchemy
# import pymysql
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, MetaData
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import plotille
import openai
from token_count import num_tokens_from_string
# from open_ai_chat import chat
import tkinter as tk
from tkinter import filedialog
from openai import OpenAI
from token_count import num_tokens_from_string

# Define the SQLAlchemy model
Base = declarative_base()

class GlucoseData(Base):
    """
    SQLAlchemy model for blood glucose data.
    """
    __tablename__ = 'glucose_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    time_stamp = Column(DateTime, unique=True)
    glucose_value = Column(Float)
    

def browse_for_csv_file() -> str:
    """
    Function to get the path of a .csv file using tkinter file dialog.
    
    Returns:
        str: Path of the selected .csv file.
        None: If no file is selected or the selected file is not a .csv file.
    """
    root = tk.Tk()
    root.withdraw()
    
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    
    if file_path and file_path.lower().endswith('.csv'):
        return file_path
    else:
        print("Please select a .csv file.")
        return None

def read_csv(file_path) -> list:
    """
    Read blood glucose data from a CSV file.

    Parameters:
    - file_path (Path): Path to the CSV file. ???

    Returns:
    - list: List of GlucoseData objects.
    """
    glucose_data_list = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        
        metadata_line = next(reader)
        patient_name = None
        for item in metadata_line:
            if item.startswith('Name:'):
                patient_name = item.split('Name:')[1].strip()

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

def insert_into_database(data_list: list, engine) -> None:
    """
    Insert blood glucose data into the database.

    Parameters:
    - data_list (list): List of GlucoseData objects.
    - engine: SQLAlchemy database engine.
    """
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        for data in data_list:
            try:
                existing_entry = (
                    session.query(GlucoseData)
                    .filter_by(name=data.name, time_stamp=data.time_stamp)
                    .one()
                )
            except NoResultFound:
                session.add(data)
                
        session.commit()
    print("New data added to the database.")

def get_data_from_database(engine) -> pd.DataFrame:
    """
    Retrieve blood glucose data from the database.

    Parameters:
    - engine: SQLAlchemy database engine.

    Returns:
    - pd.DataFrame: Pandas DataFrame containing blood glucose data.
    """
    with Session(engine) as session:
        query_result = session.query(GlucoseData).all()
        data_frame = pd.DataFrame([(data.id, data.name, data.time_stamp, data.glucose_value) for data in query_result],
                            columns=['id', 'name', 'time_stamp', 'glucose_value'])
    return data_frame

def get_last_24_hours_data (data_frame: pd.DataFrame) -> pd.DataFrame:
    """
    Extract the last 24 hours of blood glucose data.

    Parameters:
    - data_frame (pd.DataFrame): Pandas DataFrame containing blood glucose data.

    Returns:
    - pd.DataFrame: Pandas DataFrame with the last 24 hours of data.
    """

    data_frame['time_stamp'] = pd.to_datetime(data_frame['time_stamp'])
    max_timestamp = data_frame['time_stamp'].max()
    last_24_hours_timestamp = max_timestamp - pd.Timedelta(days=1)
    last_24_hours_data = data_frame[data_frame['time_stamp'] >= last_24_hours_timestamp]   
    return last_24_hours_data

def convert_dataframe_to_compressed_string(data_frame: pd.DataFrame) -> str:
    """
    Convert a Pandas DataFrame to a compressed string.

    Parameters:
    - data_frame (pd.DataFrame): Pandas DataFrame to be converted.

    Returns:
    - str: Compressed string representation of the DataFrame.
    """
    string_data = ""
    for index, row in data_frame.iterrows():
        string_data += f"{row['time_stamp']}:{row['glucose_value']}\n"

    return string_data.strip()

def plot_data_from_database_with_matplotlib(last_24_hours_data: pd.DataFrame) -> None:
    """
    Plot blood glucose data using Matplotlib.

    Parameters:
    - last_24_hours_data (pd.DataFrame): Pandas DataFrame with blood glucose data.
    """

    if last_24_hours_data.empty:
        print("No data available in the database.")

    else:
        plt.figure(figsize=(10, 6))
        plt.plot(
            last_24_hours_data['time_stamp'], 
            last_24_hours_data['glucose_value'], 
            marker='o', 
            linestyle='-', 
            color='b')
        plt.title('Blood Glucose Levels Over Time')
        plt.xlabel('Time Stamp')
        plt.ylabel('Glucose Value')
        plt.gca().get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: int(x)))# Set y-axis ticks to be integers
        plt.xticks(rotation=45, fontsize = 8)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))# Reformat the timestamp on x-axis labels
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def plot_data_from_database_with_plotille(last_24_hours_data: pd.DataFrame) -> None:
    """
    Plot blood glucose data using Plotille.

    Parameters:
    - last_24_hours_data (pd.DataFrame): Pandas DataFrame with blood glucose data.
    """

    if last_24_hours_data.empty:
        print("No data available in the database.")
    else:
        time_stamps = last_24_hours_data['time_stamp']
        glucose_values = last_24_hours_data['glucose_value']

        # Reformats to integers
        def _num_formatter(val, chars, delta, left=False):
            align = '<' if left else ''
            return '{:{}{}d}'.format(int(val), align, chars)

        plot = plotille.Figure()
        plot.width = 80
        plot.height = 30
        plot.register_label_formatter(float, _num_formatter) # Reformat to integer
        plot.register_label_formatter(int, _num_formatter) # Reformat to integer
        plot.set_x_limits(min(time_stamps), max(time_stamps))
        plot.set_y_limits(min(glucose_values), max(glucose_values) + 10)
        plot.plot(time_stamps, glucose_values, lc='red')
        print(plot.show(legend=True))

def chat(cgm_data, key):
    """Generates a conversation with openai.

    Args:
        cgm_data (tuple): 24 hours of bgl's in 5 minute increments
        key (str): OpenAI API key

    Returns:
        list: conversation with openai
    """

    print("Welcome! Here is the analysis for this data...(Type 'exit' to quit)")

    client = OpenAI(api_key=key)
    chatbot_conversation = []
    system_msg = "You are a helpful assistant."
    chatbot_conversation.append({"role": "system", "content": system_msg})

    initial_user_prompt = (
        'Analyze the following blood glucose data where the '
        'first number is the time stamp and the second is '
        'the blood glucose level. Give us the blood glucose'
        ' range, at what times are the levels out of the'
        ' 70-130 range and general observations in one paragraph:'
        f'\n{cgm_data}'
    )
    chatbot_conversation.append({"role": "user", "content": initial_user_prompt})

    while True:
            
        token_size = num_tokens_from_string(chatbot_conversation)

        if token_size < 128000:
            response = client.chat.completions.create(
                model = "gpt-4-1106-preview",
                messages = chatbot_conversation
            )

            chatbot_repsonse = response.choices[0].message.content
            print(chatbot_repsonse)
            chatbot_conversation.append({"role": "assistant", "content": chatbot_repsonse})

        else:
            print("The conversation is too large to process.")
            break

        print ("To exit the conversation, type: 'exit'.")
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        else:
            chatbot_conversation.append({"role": "user", "content": user_input})

    return chatbot_conversation
 
def main() -> None:
    """
    Main function to interact with the user and execute chosen actions.

    Raises:
        ValueError: If the user enters a non-integer value.
    """
    while True:
        try:
            user_input = int(input(
                "What would you like to do?\n"
                "1) Upload CGM data from a csv file to the database\n"
                "2) Plot the last 24 hours of uploaded data on the command line\n"
                "3) Plot the last 24 hours of data with Matplotlib\n"
                "4) Ask ChatGPT to analyze the most recent days data\n"
                "5) Exit the program\n"
            ))

            if user_input == 1:
                file_path = browse_for_csv_file()
                glucose_data_list = read_csv(file_path)
                if glucose_data_list:
                    insert_into_database(glucose_data_list, MYSQL_ENGINE)

            elif user_input == 2:
                client_data = get_data_from_database(MYSQL_ENGINE)
                last_24_hours_data = get_last_24_hours_data(client_data)
                plot_data_from_database_with_plotille(last_24_hours_data)
                
            elif user_input == 3:
                client_data = get_data_from_database(MYSQL_ENGINE)
                last_24_hours_data = get_last_24_hours_data(client_data)
                plot_data_from_database_with_matplotlib(last_24_hours_data)

            elif user_input ==4:
                client_data = get_data_from_database(MYSQL_ENGINE)
                last_24_hours_data = get_last_24_hours_data(client_data)
                condensed_string_data = convert_dataframe_to_compressed_string (last_24_hours_data)
                token_count = num_tokens_from_string(str(condensed_string_data))
                if token_count < 128000:
                    ai_response = chat(condensed_string_data, OPENAI_KEY)

            elif user_input == 5:
                break
        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    
if __name__ == "__main__":
    DATABASE_PASSWORD = os.environ.get('MYSQL_PASSWORD')
    MYSQL_ENGINE = create_engine(f"mysql+mysqlconnector://root:{DATABASE_PASSWORD}@localhost/glucose_data")
    OPENAI_KEY = os.environ.get('OPENAI_KEY')
    openai.api_key = OPENAI_KEY

    main()





