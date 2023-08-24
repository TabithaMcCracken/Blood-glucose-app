# Extract from the csv file: 
# patient name & date range in a dictionary
# glucose values & timestamp in a list of tuples


import csv

file_path = "/Users/tabithamccracken/Documents/codingnomads/blood_glucose_app/cgm_data.csv"

def convert_patient_info_data_to_dictionary(patient_info_line):
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


def get_glucose_data (file_path):
    """Get blood glucose data from a csv file.

    Args:
        file (CSV): blood glucose data

    Returns:
        patient_info_line (list): name and date range of data
        glucose_data (list of tuples):  cgm time stamp and glucose
    """

    glucose_data = []

    with open(file_path, "r", encoding='utf-8-sig') as file:
        csvreader = csv.reader(file)
        patient_info_line = next(csvreader)
        print(patient_info_line)
        print(type(patient_info_line))

        # patient_info = convert_patient_info_data_to_dictionary(patient_info_line)

        headers = next(csvreader)

        for row in csvreader:
            time_stamp, glucose, device = row # We don't need the device info
            glucose_data.append((time_stamp, glucose)) # Adding parenthesis makes it a tuple

    return patient_info_line, glucose_data # a dictionary and a list of tuples

patient_info_line, cgm_data = get_glucose_data(file_path)

parsed_patient_info = convert_patient_info_data_to_dictionary(patient_info_line)
print(parsed_patient_info)








# final_line = file.readlines()[-1]
# print(final_line)

# with open(file_path, "r") as file:
#     csvreader = csv.reader(file)
#     csv_patient_info = next(csvreader)
#     csv_headings = next(csvreader)
#     first_line = next(csvreader)
# print (csv_patient_info)
# print(csv_headings)
# print(first_line[0])

# print(f"First Date: {first_line[0][0:10]}")


# Check for value errors in the header
# if headers != ["Timestamp", "CGM Glucose Value (mg/dl)", "Serial Number"]
#     raise ValueError("CSV Values are unexpected!")