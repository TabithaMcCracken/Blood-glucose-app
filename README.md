# Blood Glucose Data Handler
## Overview
This Python script is designed to handle blood glucose data obtained from a CGM through Glooko for individuals with Type 1 or Type 2 Diabetes. It provides functionalities to store blood glucose data from a CSV file in a MySQL database, plot the last 24 hours of uploaded data, and analyze the data using ChatGPT.

## Installation
1. Clone this repository to your local machine.
2. Install the required dependencies using pip:
```bash
pip install sqlalchemy pandas matplotlib plotille openai
```
3. **Set Up MySQL Database:**
- Make sure you have MySQL installed and running locally. If not, download and install MySQL from [MySQL Downloads](https://dev.mysql.com/downloads/).
- Create a MySQL database named `glucose_data` using your preferred MySQL client or the command line:
  ```
  CREATE DATABASE glucose_data;
  ```
- Ensure that you have a MySQL user with appropriate permissions to access and modify the `glucose_data` database. You can create a user and grant permissions using commands like:
  ```
  CREATE USER 'your_username'@'localhost' IDENTIFIED BY 'your_password';
  GRANT ALL PRIVILEGES ON glucose_data.* TO 'your_username'@'localhost';
  ```
- Replace `'your_username'` and `'your_password'` with your desired username and password.

4. **Obtain an OpenAI Key**
- For the ChatGPT functionality, you also need to sign up for an OpenAI API account and obtain an API key.

- Sign up for an account at [OpenAI](https://openai.com/) if you haven't already.

- After signing up, generate an API key from your account dashboard.

5. **Set Up Environment Variables:**
- Set up environment variables for the MySQL password (`MYSQL_PASSWORD`) and your OpenAI API key (`OPENAI_KEY`).

- Set the environment variable for the OpenAI API key using the following command:
  ```
  export OPENAI_KEY=your_openai_api_key
  ```
- Replace `your_openai_api_key` with your actual OpenAI API key.

- Set the environment variable for the MySQL password using the following command:
  ```
  export MYSQL_PASSWORD=your_mysql_password
  ```
- Replace `your_mysql_password` with your actual MySQL password

5. **Export CGM Data from Glooko
- To use this program with CGM data from Glooko, you'll need to export the CGM data from the Glooko
platform and save it as a CSV file. 

Note: If you don't have CGM data from Glooko or prefer not to download it, you can use the sample data file provided in the package folder.

Follow these steps to export your CGM data from Glooko:

1. Log in to Glooko: Visit the [Glooko](https://glooko.com) website and log in to your account.

2. From the main "Summary" page, click on "Export to CSV".

3. Select the CGM Data time range that you want to download. You may have options to export data for specific time periods, such as the last week, month, or custom date range.

4. Click "Export" to download the files.

5. After the report has been generated, Glooko may provide the data in a zip folder containing multiple files. Download the zip folder to your computer.

6. Extract Files: Once the zip folder is downloaded, extract its contents to a location on your computer. You should now have multiple files containing the CGM data.

7. Select the Appropriate File: Among the extracted files, locate the CSV file containing the CGM data. This file is typically named something like cgm_data.csv.

8. Use with the Program: Now that you have the CSV file containing your CGM data, you can use it with the provided Python program. Follow the instructions in the program to upload the CSV file and analyze your CGM data


## Usage
To run the script, execute the main.py file using Python:
```bash
python blood_glucose_app.py
```
Follow the prompts to interact with the script and perform various actions such as uploading data, plotting graphs, and analyzing data with ChatGPT.

**Note:** If you do not have a CSV file with CGM data downloaded from Glooko, there is a sample data CSV file located in the package folder.

## Functionality
- **Upload CGM Data from CSV**: Allows users to upload blood glucose data from a CSV file to the MySQL database.
- **Plot Data on Command Line**: Displays a command-line plot of the last 24 hours of uploaded blood glucose data.
- **Plot Data with Matplotlib**: Generates a graphical plot of the last 24 hours of blood glucose data using Matplotlib.
- **Analyze Data with ChatGPT**: Engages in a conversation with ChatGPT to analyze the most recent day's blood glucose data.

**Note:** Data must be present in the MySQL database in order to plot data or analyze data with ChatGPT. Make sure to upload blood glucose data using the provided functionality before attempting to plot or analyze it.

## Requirements
- Python 3.x
- MySQL database
- OpenAI API key

## Dependencies
- SQLAlchemy
- Pandas
- Matplotlib
- Plotille
- OpenAI

## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

