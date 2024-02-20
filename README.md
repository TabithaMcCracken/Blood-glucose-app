# Blood Glucose Data Handler
## Overview
This Python script is designed to handle blood glucose data obtained from a CGM through Glooko for individuals with Type 1 or Type 2 Diabetes. It provides functionalities to upload blood glucose data from a CSV file downloaded from the users Glooko account to a MySQL database, plot the last 24 hours of uploaded data, and analyze the data using ChatGPT.

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

4. **Set Up Environment Variables:**
- Set up environment variables for the MySQL password (`MYSQL_PASSWORD`) and your OpenAI API key (`OPENAI_KEY`).
- For the ChatGPT functionality, you also need to sign up for an OpenAI API account and obtain an API key.
- Sign up for an account at [OpenAI](https://openai.com/) if you haven't already.
- After signing up, generate an API key from your account dashboard.
- Set the environment variable for the OpenAI API key:
  ```
  export OPENAI_KEY=your_openai_api_key
  ```
- Replace `your_openai_api_key` with your actual OpenAI API key.

- To set the environment variable for the MySQL password using the following command:
  ```
  export MYSQL_PASSWORD=your_mysql_password
  ```
- Replace `your_mysql_password` with your actual MySQL password


## Usage
To run the script, execute the main.py file using Python:
```bash
python main.py
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

