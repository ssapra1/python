import streamlit as st 
import pandas as pd
import numpy as np 

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def main():
    st.title("Add Production historical data to database")
    with st.form("my_form1"):

     uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
     submitted1 = st.form_submit_button('upload')
     st.write(submitted1)
    if submitted1:
       if uploaded_file is not None:
        with st.spinner('Reading from CSV file..'):
               time.sleep(20)
        data = pd.read_csv(uploaded_file)

        st.write("Here is the uploaded file's data:")
        st.dataframe(data)

        st.line_chart(data)
        st.write("Material-style data table:")


        import sqlite3

        # Assuming `data` is the DataFrame from the uploaded file
        column_headers = ["ID", "Date", "Brand", "Category", "Weight", "Entered Weight Number", "PHR", "DOP", "Batch","bundleQty","pipeQty"]

        # Ensure the uploaded file contains required columns
        if all(col in data.columns for col in column_headers):
            # Create a connection to the SQLite database (or create the database if it doesn't exist)
            conn = sqlite3.connect('production_form.db')
            cursor = conn.cursor()

            # Create table with the specified columns if it does not exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS form_data (
                    ID TEXT,
                    Date TEXT,
                    Brand TEXT,
                    Category TEXT,
                    Weight REAL,
                    Entered_Weight_Number REAL,
                    PHR TEXT,
                    DOP TEXT,
                    Batch TEXT,
                    bundleQty TEXT,
                    pipeQty TEXT
                )
            ''')

            # Insert all data into the database
            with st.spinner('Inserting data into database...'):
                time.sleep(2)  # Optional delay to simulate loading effect
                # Insert all data into the database
                for _, row in data[column_headers].iterrows():
                    cursor.execute('''
                              INSERT INTO form_data (ID, Date, Brand, Category, Weight, Entered_Weight_Number, PHR, DOP, Batch,bundleQty,pipeQty)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                          ''', tuple(row))
            # Commit changes and close the connection
            conn.commit()
            conn.close()

            st.write("Data has been inserted into the database successfully.")


        else:
            st.write("The uploaded file does not contain all required columns.")


if __name__ == "__main__":
    main()