# Disaster Response Pipeline Project

### Instructions:

1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/

### Project Structure

- app

| - template

| |- base.html  # base template of web app

| |- home.html  # home page of web app

| |- profiling_message.html  # pandas profilimg result of message dataframe

| |- profiling.html  # profiling page of web app

| |- search_table.html  # search table page of web app

| |- table_rows.html  # template page used by htmx to do infinite scrolling

| |- go.html  # classification result page of web app

|- run.py  # Flask file that runs app

|- extensions.py  # Flask extensions

|- utility.py  # utility function for web app

- data

|- disaster_categories.csv  # data to process 

|- disaster_messages.csv  # data to process

|- process_data.py

|- InsertDatabaseName.db   # database to save clean data to

- models

|- train_classifier.py

|- classifier.pkl  # saved model 

- README.md

- Requirements.txt  # python dependencies

### Flask app

Home page: display visuals, prompt to classify message

Raw data page: display raw data, able to do infinite scrolling to display the raw message table

Profiling page: display pandas df profiling
