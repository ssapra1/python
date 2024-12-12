import streamlit as st
import pandas as pd
import numpy as np

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def main():
    st.title("Add Sales historical data to database")
    with st.form("sales_form1"):

        uploaded_files = st.file_uploader("Choose CSV files", type=["csv"], accept_multiple_files=True)
        submitted1 = st.form_submit_button('upload')
        st.write(submitted1)
        if submitted1:
            if uploaded_files:
                dataframes = []
                for uploaded_file in uploaded_files:
                    with st.spinner(f'Reading from {uploaded_file.name}...'):
                        time.sleep(2)
                        df = pd.read_csv(uploaded_file)
                        dataframes.append(df)
                        st.write(f"Data from {uploaded_file.name}:")
                        st.dataframe(df)

                # Combine all data into a single DataFrame
                combined_data = pd.concat(dataframes, ignore_index=True)
                st.write("Combined Data:")
                st.dataframe(combined_data)

                # Specify the columns to retain and exclude "ID" from the database
                required_columns = ["ID", "Date", "Brand", "Weight (kg)", "Category", "PHR", "Bundle Count",
                                    "Pipe Count"]

                # Check if all required columns exist in the combined data
                if all(column in combined_data.columns for column in required_columns):
                    # Filter the DataFrame with the required columns, excluding "ID"
                    filtered_data = combined_data[required_columns].drop(columns=["ID"])

                    # Assuming connection to a SQLite database; you can replace it as per requirements
                    import sqlite3

                    # Establish a connection to the database (SQLite example)
                    conn = sqlite3.connect("production_form.db")  # Replace with your database filename
                    cursor = conn.cursor()

                    # Create a table if it doesn't exist
                    table_creation_query = """
                    CREATE TABLE IF NOT EXISTS SalesFormData (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        Date TEXT,
                        Brand TEXT,
                        Weight_kg REAL,
                        Category TEXT,
                        PHR INTEGER,
                        bundle_count INTEGER,
                        pipe_count INTEGER
                    )
                    """
                    cursor.execute(table_creation_query)

                    # Write the filtered data into the database
                    filtered_data.rename(columns={
                        "Weight (kg)": "weight",
                        "bundle_count": "bundle_count",
                        "Pipe Count": "pipe_count"
                    }, inplace=True)
                    filtered_data.to_sql("SalesFormData", conn, if_exists="append", index=False)

                    # Commit and close the connection
                    conn.commit()
                    conn.close()
                    show_data_base()
                    st.success("Data successfully written to the database!")

                # Display all data from the database in a table format

                else:
                    st.error("Combined data does not contain all required columns.")
                # Further processing can now be applied to `combined_data`
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])


st.write("Here is the uploaded file's data:")


def show_data_base():
    st.write("All Data from Database:")

    import sqlite3

    # Establish a connection to the database
    conn = sqlite3.connect("production_form.db")  # Replace with your database filename
    cursor = conn.cursor()

    # Fetch all data from the SalesFormData table
    fetch_query = "SELECT * FROM SalesFormData"
    data = cursor.execute(fetch_query).fetchall()

    # Fetch column names to use as table headers
    columns_query = "PRAGMA table_info(SalesFormData)"
    columns = [column[1] for column in cursor.execute(columns_query).fetchall()]

    # Create a Pandas DataFrame from the fetched data
    all_data_df = pd.DataFrame(data, columns=columns)

    # Display the DataFrame in Streamlit
    st.dataframe(all_data_df)

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()