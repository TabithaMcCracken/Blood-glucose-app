# Blood Glucose Data Handler
## Overview
This Python script is designed to handle blood glucose data for individuals with Type 1 Diabetes. It provides functionalities to upload blood glucose data from a CSV file to a MySQL database, plot the last 24 hours of uploaded data, analyze the data using ChatGPT, and more.

## Installation
Clone this repository to your local machine.
Install the required dependencies using pip:
```bash
pip install sqlalchemy pandas matplotlib plotille openai
```

Make sure you have MySQL installed and running locally. Set up a MySQL database named glucose_data.
Set up environment variables for the MySQL password (MYSQL_PASSWORD) and your OpenAI API key (OPENAI_KEY).
Usage
To run the script, execute the main.py file using Python:
```bash
python main.py
```

Follow the prompts to interact with the script and perform various actions such as uploading data, plotting graphs, and analyzing data with ChatGPT.
## Functionality
Upload CGM Data from CSV: Allows users to upload blood glucose data from a CSV file to the MySQL database.
Plot Data on Command Line: Displays a command-line plot of the last 24 hours of uploaded blood glucose data.
Plot Data with Matplotlib: Generates a graphical plot of the last 24 hours of blood glucose data using Matplotlib.
Analyze Data with ChatGPT: Engages in a conversation with ChatGPT to analyze the most recent day's blood glucose data.

## Requirements
Python 3.x
MySQL database
OpenAI API key

## Dependencies
SQLAlchemy
Pandas
Matplotlib
Plotille
OpenAI

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

