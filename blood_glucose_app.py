# Part 1
# Extract from the csv file: 
# patient name & date range in a dictionary ^
# glucose values & timestamp in a list of tuples ^

# Part 2
# Use OpenAI to analyze the data
import csv
from open_ai_chat import chat
from token_count import num_tokens_from_string
from make_sample_data import make_sample_data_set

file_path = "/Users/tabithamccracken/Documents/codingnomads/blood_glucose_app/cgm_data_one_day.csv"

def convert_patient_info_data_to_dictionary(patient_info_line):
    """Extracts desired patient info and puts it into a dictionary

    Args:
        patient_info_line (list): patient info from the csv file

    Returns:
        patient_info (dict): name, start_date, end_date of data
    """

    name_part = patient_info_line[0]
    if ":" in name_part:
        patient_name = name_part.split(":")[1].strip()
    else:
        print(f"Unexpected format for name part: {name_part}")
        patient_name = "Unknown"

    date_range_part = patient_info_line[1].split(":")[1].strip()
    start_date, end_date = date_range_part.split(" ")
    end_date = end_date[1:]
        
    patient_info = {
            'Name': patient_name,
            'Start Date': start_date,
            'End Date': end_date
        }

    return patient_info

def compact_format(entry):
    date, level = entry
    date_parts = date.split()
    compact_date = date_parts[1]  # Only take the time
    compact_level = str(int(float(level)))  # Remove decimal part
    return compact_date + '|' + compact_level

def get_glucose_data (file_path):
    """Get blood glucose data from a csv file.

    Args:
        file (CSV): blood glucose data

    Returns:
        patient_info_line (list): name and date range of data
        glucose_data (list of tuples):  cgm time stamp and glucose
    """

    glucose_data = []

    with open(file_path, "r", encoding='utf-8') as file:
        csvreader = csv.reader(file)
        patient_info_line = next(csvreader)

        headers = next(csvreader)

        for row in csvreader:
            time_stamp, glucose, _ = row # We don't need the device info
            glucose_data.append((time_stamp, glucose)) # Adding parenthesis makes it a tuple
    
    parsed_patient_info = convert_patient_info_data_to_dictionary(patient_info_line)

    # Make the data more compact by changing format
    compact_cgm_data= [compact_format(entry) for entry in glucose_data]

    return parsed_patient_info, compact_cgm_data # a dictionary and a list of tuples

if __name__ == "__main__":
    # Gets patient info and cgm data from csv file or make a sample data set

    # Get data from file
    patient_info_line, cgm_data = get_glucose_data(file_path)
    print(patient_info_line)
    print(cgm_data)

    # Make sample data set
    # cgm_data = make_sample_data_set()
    
    # Check the token size of the compact data
    token_size = num_tokens_from_string(cgm_data)
    print(f"Token size: {token_size}")

    # Starts AI chat
    # ai_response = chat(cgm_data)
    # print(ai_response)
    # user_prompt = input("What would you like to ask ") ???



