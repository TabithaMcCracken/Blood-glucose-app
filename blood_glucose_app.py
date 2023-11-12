
# When should I sort the data in chronological order?
# When we get the data or when we condense the data?
# Right now, we are doing both because sometimes the data from a file
# and sometimes it is created using the make_sample_data file

# Extract from the csv file: 
# patient name & date range in a dictionary ^
# glucose values & timestamp in a list of tuples ^

# Get patient info from data (name, start date, end date)

# Make the data more compact
# Display the glucose levels
# Check the token size
# Use OpenAI to analyze the data and converse with the user (seperate file)


import csv
from open_ai_chat import chat
from token_count import num_tokens_from_string
from display_glucose_data import display_glucose_levels
# from make_sample_data import generate_glucose_levels

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
    time_stamp, level = entry
    date_parts = time_stamp.split()
    compact_time = date_parts[1]  # Only take the time
    compact_date = date_parts[0]
    year = compact_date.split('-')[0]
    shortened_year = year[2:]
    updated_date = f"{shortened_year}-{compact_date[5:]}"
    compact_level = str(int(float(level)))  # Removes decimal part and makes it a string
    return updated_date + '|' + compact_time + '|' + compact_level

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
    
    # Make the patient info into a dictionary
    parsed_patient_info = convert_patient_info_data_to_dictionary(patient_info_line)

    # Make the data more compact by changing format
    compact_cgm_data= [compact_format(entry) for entry in glucose_data]
    print(compact_cgm_data)

    # Sort data by time
    compact_cgm_data.sort(key=lambda entry: entry.split('|')[0] + entry.split('|')[1])

    return parsed_patient_info, compact_cgm_data # a dictionary and a list of tuples

def condense_data(data):
    condensed = []
    previous_glucose = None

    # Sort data by time
    data.sort(key=lambda entry: entry.split('|')[0] + entry.split('|')[1])

    # Include the first data point
    first_entry = data[0]
    date, time, level_str = first_entry.split('|')
    glucose = int(level_str)

    condensed.append(f"{date}|{time}|{glucose}")
    previous_glucose = glucose

    for i in range(3, len(data), 3):  # Skip every 3rd entry
        entry = data[i]
        date, time, level_str = entry.split('|')
        glucose = int(level_str)

        if glucose != previous_glucose:
            condensed.append(f"{date}|{time}|{glucose}")
            previous_glucose = glucose

    # Include the last data point
    last_entry = data[-1]
    date, time, level_str = last_entry.split('|')
    glucose = int(level_str)
    condensed.append(f"{date}|{time}|{glucose}")

    return condensed

def remove_date (data):
    # Remove the date from the data string
    shortened_data = [data_string.split('|', 1)[1] for data_string in data]
    return shortened_data

if __name__ == "__main__":
    # Gets patient info and cgm data from csv file or make a sample data set

    # Get data from file
    patient_info_line, cgm_data = get_glucose_data(file_path)
        
    # display_glucose_levels(cgm_data, patient_info_line)

    # # Make sample data set- only needed if user has no data
    # # cgm_data = generate_glucose_levels()
    
    # Check the token size of the data
    token_size = num_tokens_from_string(cgm_data)
    print(f"Token size before condensing: {token_size}")

    # Condense the data and check the new token size
    condensed_data = condense_data(cgm_data)
    condensed_token_size = num_tokens_from_string(condensed_data)
    print(f"Token size after condensing: {condensed_token_size}")

    # Remove the date from the data string
    short_cgm_data = remove_date(cgm_data)

    # display_glucose_levels(condensed_data)
    final_token_check = num_tokens_from_string(short_cgm_data)
    print(f"Final token size: {final_token_check}")

    # if final_token_check < 4097:
    #     # Starts the AI chat
    #     ai_response = chat(cgm_data)




