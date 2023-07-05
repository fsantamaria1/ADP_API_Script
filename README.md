# ADP API Script

The ADP_API_Script is a Python script that retrieves timecards and employee information from ADP using the ADP API. The script can be scheduled to run daily at a specific time to fetch the latest data.

## Table of contents
- [Prerequisites](#Prerequisites)
- [Installation](#Installation)
- [Configuration](#Configuration)
- [Usage](#Usage)
- [Structure](#Project-Structure)
  

## Prerequisites

Before running the script, ensure you have the following:

1. Python installed (version 3.7 or higher)
2. ADP API credentials (client ID and client secret) obtained from ADP
3. Certificates (PEM and KEY files) required for authentication
4. Access to a SQL database to store the retrieved data
5. Environment variables set up in a `.env` file (refer to the `.env.example` file for the required variables)

## Installation

1. Clone or download the ADP_API_Script project from the repository.

   ```shell
   git clone https://github.com/fsantamaria1/ADP_API_Script.git
   ```
   
3. Open a terminal or command prompt and navigate to the project directory.

   ```shell
   cd ADP_API_Script
   ```
   
5. Create a virtual environment (optional but recommended):
   - Run ```shell python -m venv venv``` to create a new virtual environment.
   - Activate the virtual environment:
     - On Windows: ```shell venv\Scripts\activate````
     - On Unix or Linux: ```shell source venv/bin/activate````
6. Install the required dependencies by running the following command:
   ```shell
   pip install -r requirements.txt
   ```

## Configuration

Before running the script, configure the following settings:

1. Update the `.env` file:
   - Set the `client_id` and `client_secret` variables with your ADP API credentials.
   - Set the `main_associate_id` variable with the ID of the main associate.
   - Specify the paths to the PEM and KEY files (`cert_file_path` and `key_file_path` variables).
   - Set the database credentials (`server`, `user`, `password`, `database`, `default_schema`, `adp_schema` variables).
2. Modify the `run.py` file if you want to change the scheduled time for running the script. By default, it is set to run at 10 PM daily.

## Usage

To run the script manually, execute the following command in the project directory:

```
python main.py
```

The script will connect to the ADP API, retrieve employee information, retrieve timecards, and update the database tables accordingly.

To schedule the script to run automatically at the specified time (the default is 10 PM), run the following command:

```
python run.py
```

The script will run in the background and execute at the scheduled time every day until stopped.

## Project Structure

The project structure is organized as follows:

```
ADP_API_Script/
  |- main.py
  |- run.py
  |- requirements.txt
  |- .env.example
  |- resources/
      |- adp_requests.py
      |- config.py
      |- database.py
      |- database_functions.py
      |- date_util.py
      |- models.py
      |- response_filter.py
```

- `main.py`: Contains the main logic for fetching and processing data from the ADP API.
- `run.py`: Entry point script to schedule the main script to run at a specific time.
- `requirements.txt`: List of Python dependencies required by the project.
- `.env.example`: Example file for setting up the environment variables. Rename it to `.env` and update the values accordingly.
- `resources/`: Directory containing various modules used by the main script:
  - `adp_requests.py`: Handles the ADP API requests and authentication.
  - `config.py`: Contains configuration settings for the script.
  - `database.py`: Handles the connection and interaction with the SQL database.
  - `database_functions.py`: Contains functions to execute SQL queries and stored procedures.
  - `date_util.py`: Provides utility functions for date manipulation.
  - `models.py`: Defines the unnormalized data models for timecards and employees.
  - `response_filter.py`: Filters and transforms the API response data.
