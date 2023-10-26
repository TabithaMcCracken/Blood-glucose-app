import random

def generate_glucose_levels():
    # Constants
    MIN_GLUCOSE = 60
    MAX_GLUCOSE = 250
    MIN_CHANGE = -10
    MAX_CHANGE = 10
    TIME_INCREMENT = 15   # Update to 15 minutes

    # Start in the middle range
    current_glucose = (MIN_GLUCOSE + MAX_GLUCOSE) // 2
    previous_glucose = None
    glucose_data = []

    for h in range(24):
        for m in range(0, 60, TIME_INCREMENT):
            # Randomly decide the change in glucose (ensuring it's within limits)
            glucose_change = random.randint(MIN_CHANGE, MAX_CHANGE)
            # Ensure next value is within allowed range
            current_glucose = min(max(MIN_GLUCOSE, current_glucose + glucose_change), MAX_GLUCOSE)

            if current_glucose != previous_glucose:  # Only store if different from previous
                entry = f"{h:02}:{m:02}|{current_glucose}"
                glucose_data.append(entry)
                previous_glucose = current_glucose

    return glucose_data

# def display_glucose_levels(data):
#     print("Time  | Blood Glucose Level")
#     print("------" + "-" * 20)

#     for entry in data:
#         try:
#             time, level = entry.split('|')
#             print(f"{time} | {level}")
#         except ValueError:
#             print(f"Error with entry: {entry}")

def display_glucose_levels(data):
    # Constants for display
    MIN_GLUCOSE = 60
    SCALE_FACTOR = 0.2  # This will determine the length of bars

    print("Time  | Glucose Level | Graph")
    print("------|---------------|--------------------")

    for entry in data:
        time, level_str = entry.split('|')
        level = int(level_str)

        # Calculate bar length based on glucose level and scale factor
        bar_length = int((level - MIN_GLUCOSE) * SCALE_FACTOR)
        bar = '#' * bar_length

        print(f"{time} | {level:13} | {bar}")


if __name__ == "__main__":
    # Testing the function with generated data
    data = generate_glucose_levels()
    display_glucose_levels(data)

