import random

# Constants for generating glucose levels
MIN_GLUCOSE = 60
MAX_GLUCOSE = 250
MIN_CHANGE = -10
MAX_CHANGE = 10
TIME_INCREMENT = 5
DATE = "23-08-01"

# Constants for display
MIN_GLUCOSE = 60
SCALE_FACTOR = 0.2  # Set the length of the bars

def generate_glucose_levels():

    # Start in the middle of the range of data
    current_glucose = (MIN_GLUCOSE + MAX_GLUCOSE) // 2
    previous_glucose = None
    glucose_data = []

    for h in range(24):
        for m in range(0, 60, TIME_INCREMENT):
            # Randomly decide the change in glucose (within limits)
            glucose_change = random.randint(MIN_CHANGE, MAX_CHANGE)
            # Ensure next value is within allowed range
            current_glucose = min(max(MIN_GLUCOSE, current_glucose + glucose_change), MAX_GLUCOSE)

            if current_glucose != previous_glucose:  # Only store if different from previous
                time = f"{h:02}:{m:02}"
                entry = f"{DATE}|{time}|{current_glucose}"
                glucose_data.append(entry)
                previous_glucose = current_glucose

    return glucose_data


if __name__ == "__main__":
    # Testing the function with generated data
    data = generate_glucose_levels()

