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
        column_headers = ["ID", "Date", "Brand", "Weight (kg)", "Category", "PHR", "Bundle Count",
               "Pipe Count"]
        # Ensure the uploaded file contains required columns
        if all(col in data.columns for col in column_headers):
            # Create a connection to the SQLite database (or create the database if it doesn't exist)
            conn = sqlite3.connect('production_form.db')
            cursor = conn.cursor()

            # Create table with the specified columns if it does not exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS SalesFormData (
                     ID Text,
                                date TEXT,
                                brand TEXT,
                                weight REAL,
                                category TEXT,
                                phr TEXT,
                                bundle_count INTEGER,
                                pipe_count INTEGER
                )
            ''')

            # Insert all data into the database
            with st.spinner('Inserting data into database...'):
                time.sleep(2)  # Optional delay to simulate loading effect
                # Insert all data into the database
                for _, row in data[column_headers].iterrows():
                    cursor.execute('''
                             INSERT INTO SalesFormData (ID,date, brand, weight, category, phr, bundle_count, pipe_count)
                            VALUES ( ? ,?, ?, ?, ?, ?, ?, ?)
                          ''', tuple(row))
            # Commit changes and close the connection
            conn.commit()
            conn.close()

            # Adding additional Streamlit elements for interaction
            st.header("Sales Data Analysis Dashboard")

            # Adding metric widgets to display key information
            st.subheader("Key Metrics")
            if "Weight (kg)" in data.columns and "Bundle Count" in data.columns:
                total_weight = data["Weight (kg)"].sum()
                total_bundles = data["Bundle Count"].sum()
                st.metric(label="Total Weight (kg)", value=f"{total_weight:.2f}")
                st.metric(label="Total Bundles", value=int(total_bundles))

            # Adding checkbox for file preview
            if st.checkbox("Preview First 5 Rows of Data"):
                st.write(data.head())

            # Adding a multiselect to filter data by Category
            if "Category" in data.columns:
                selected_categories = st.multiselect(
                    "Select Categories to Display:",
                    options=data["Category"].unique(),
                    default=data["Category"].unique()
                )
                filtered_data = data[data["Category"].isin(selected_categories)]
                st.write("Filtered Data:")
                st.dataframe(filtered_data)

            # Adding an expander for advanced filtering options
            with st.expander("Advanced Filters"):
                if "Brand" in data.columns:
                    selected_brands = st.multiselect(
                        "Select Brands:",
                        options=data["Brand"].unique(),
                        default=data["Brand"].unique()
                    )
                    filtered_data = filtered_data[filtered_data["Brand"].isin(selected_brands)]

                if "Weight (kg)" in data.columns:
                    min_weight, max_weight = st.slider(
                        "Select Weight Range (kg):",
                        min_value=float(data["Weight (kg)"].min()),
                        max_value=float(data["Weight (kg)"].max()),
                        value=(float(data["Weight (kg)"].min()), float(data["Weight (kg)"].max()))
                    )
                    filtered_data = filtered_data[
                        (filtered_data["Weight (kg)"] >= min_weight) &
                        (filtered_data["Weight (kg)"] <= max_weight)
                        ]

                st.write("Data after applying all filters:")
                st.dataframe(filtered_data)

            st.write("Data has been inserted into the database successfully.")
        else:
            st.write("The uploaded file does not contain all required columns.")
if __name__ == "__main__":
    main()