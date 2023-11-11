# Constants for display
MIN_GLUCOSE = 60
SCALE_FACTOR = 0.2  # Set the length of the bars

sample_data = "23-08-01|03:40|135", "23-08-01|03:55|150", "23-08-01|04:10|160"

def display_glucose_levels(data, patient_info):
    print("Patient Info:")
    for item in patient_info:
        print(item)

    print("Date     | Time  | Glucose | Graph")
    print("---------|-------|---------|--------------------")

    for entry in data:
        date, time, level_str = entry.split('|')
        level = int(level_str)

        # Calculates bar length based on glucose level and scale factor
        bar_length = int((level - MIN_GLUCOSE) * SCALE_FACTOR)
        bar = '#' * bar_length

        print(f"{date} | {time} | {level:7} | {bar}")

if __name__ == "__main__":
    display_glucose_levels(sample_data)