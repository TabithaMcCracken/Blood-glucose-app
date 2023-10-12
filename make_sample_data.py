from datetime import datetime, timedelta
import random

def make_sample_data_set():
    """Create a tuple we can use as a sample data set

    Returns:
        Tuple: timestamp and blood glucose level
    """

    # Start from the current time
    start_time = datetime.now()

    # Generate the user_data list
    sample_data = tuple((start_time + timedelta(minutes=5 * i), 80 + i % 10) for i in range(24))

    # Example printout
    for timestamp, level in sample_data:
       print(timestamp.strftime('%Y-%m-%d %H:%M'), level)
    return sample_data



def generate_glucose_levels():
    # Define constants
    MIN_GLUCOSE = 60
    MAX_GLUCOSE = 200
    MIN_CHANGE = -10
    MAX_CHANGE = 10
    TIME_INCREMENT = 5
    HOURS_IN_DAY = 24

    # Start in the middle range
    current_glucose = (MIN_GLUCOSE + MAX_GLUCOSE) // 2

    glucose_levels = []

    for minute in range(0, HOURS_IN_DAY * 60, TIME_INCREMENT):
        hour = minute // 60
        minute_within_hour = minute % 60
        
        # Randomly decide the change in glucose (ensuring it's within limits)
        glucose_change = random.randint(MIN_CHANGE, MAX_CHANGE)
        
        # Ensure next value is within allowed range
        current_glucose = min(max(MIN_GLUCOSE, current_glucose + glucose_change), MAX_GLUCOSE)
        
        glucose_levels.append((f"{hour:02}:{minute_within_hour:02}", current_glucose))

    return tuple(glucose_levels)


def display_glucose_levels(data):
    print("Time  | Blood Glucose Level (Graphed as '#')")
    print("------" + "-" * 40)

    for time, level in data:
        bar_length = (level - 60) // 3  # Adjust this division for scaling the length of bars
        bar = '#' * bar_length
        print(f"{time} | {level:3} | {bar}")


if __name__ == "__main__":
    data = generate_glucose_levels()
    print (type(data))
    display_glucose_levels(data)

