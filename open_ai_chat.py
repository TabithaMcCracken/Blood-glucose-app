# Things we're looking for from the API
# Blood sugar range
# General observations
# Trend Analysis: 
# Morning 6am -12noon
# Afternoon: 12noon - 6pm
# Evening: 6pm - 12midnight
# Overnight: 12midnight - 6am


from datetime import datetime, timedelta
from secret import key
import openai

def make_sample_data_set():

    # Create a tuple we can use to for sample data
    # Start from the current time
    start_time = datetime.now()

    # Generate the user_data list
    sample_data = tuple((start_time + timedelta(minutes=5 * i), 80 + i % 10) for i in range(24))

    # Example printout
    # for timestamp, level in user_data:
    #    print(timestamp.strftime('%Y-%m-%d %H:%M'), level)
    return sample_data

def analyze_glucose_data_with_openai(user_data):
    openai.api_key = key
    system_msg = "You are a helpful assistant."
    # Convert the data to a string for analysis
    data_str = "\n".join(["{}: {}".format(timestamp, level) for timestamp, level in user_data])

    user_prompt = f"Analyze the following blood glucose data giving us a blood glucose range and general observations in one paragraph:\n{data_str}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_prompt}
        ], 
        max_tokens=200  # Adjust based on your needs
    )

    return response["choices"][0]["message"]["content"]


user_data = make_sample_data_set()
ai_analysis = analyze_glucose_data_with_openai(user_data)
print(ai_analysis)

