import sqlite3

import streamlit as st
import pandas as pd
import numpy as np
from streamlit import cursor


def main():
    st.title('Sales Form for Saxena Industries ')

    # Create a form for user input
    with st.form("sales_form"):
        # Add form fields
        date = st.date_input("Date")
        brand = st.selectbox("Brand", ["SAFAL", "SARAS", "ENDO", "GE", "SVE"])
        weight = st.number_input("Weight (in kg)", min_value=0.0)
        category = st.selectbox("Category", ["LMS (20-40)", "MMS (40-52)", "HMS (52-70)", "Others"])
        phr = st.selectbox("PHR", ["40", "50", "60", "70", "80", "90", "100"])
        bundle_count = st.number_input("Bundle Count", min_value=0, step=1)
        pipe_count = st.number_input("Pipe Count", min_value=0, step=1)

        # Submit button
        submitted = st.form_submit_button("Submit")

        # Validation logic
        if submitted:
            error_message = ""

            if not date:
                error_message += "Date is required.\n"
            if not brand or brand == "Select brand":
                error_message += "Please select a valid brand.\n"
            if weight <= 0:
                error_message += "Weight must be greater than 0.\n"
            if not category or category == "Select category":
                error_message += "Please select a valid category.\n"
            if not phr or phr == "Select PHR":
                error_message += "Please select a valid PHR.\n"
            if bundle_count <= 0:
                error_message += "Bundle Count must be greater than 0.\n"
            if pipe_count <= 0:
                error_message += "Pipe Count must be greater than 0.\n"

            if error_message:
                st.error(error_message)
            else:
                st.success("Form submitted successfully!")

                if submitted and not error_message:
                    # Save to database after successful form submission
                    save_to_db(date, brand, weight, category, phr, bundle_count, pipe_count)

                    # Display submitted data in table format
                    submitted_data = pd.DataFrame(
                        {
                            "Date": [date],
                            "Brand": [brand],
                            "Weight": [weight],
                            "Category": [category],
                            "PHR": [phr],
                            "Bundle Count": [bundle_count],
                            "Pipe Count": [pipe_count],
                        }
                    )
                    st.table(submitted_data)
                  # Call the function to display all data
                    st.write("All Submitted Sales Data")
                    all_data=display_all_data()
                    if all_data:
                        # Define column headers based on the table schema

                        # Fetch column headers dynamically
                        column_headers = ["ID", "Date", "Brand", "Weight", "Category", "PHR", "Bundle Count",
               "Pipe Count"]

                        # Use pandas to create a DataFrame and display it
                        df_all_data = pd.DataFrame(all_data, columns=column_headers)
                        st.write("All Submitted Data:")
                        st.write(df_all_data.style.set_table_styles(
                            [{'selector': 'table', 'props': [('width', '100%')]}]
                        ))
                    else:
                        st.write("No data found in the database.")
                    import sqlite3

                    # Save data to SQLite database
def save_to_db(date, brand, weight, category, phr, bundle_count, pipe_count):
    conn = sqlite3.connect('production_form.db')
    cursor = conn.cursor()
    cursor.execute('''
                            CREATE TABLE IF NOT EXISTS SalesFormData (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                date TEXT,
                                brand TEXT,
                                weight REAL,
                                category TEXT,
                                phr TEXT,
                                bundle_count INTEGER,
                                pipe_count INTEGER
                            )
                        ''')

    cursor.execute('''
                            INSERT INTO SalesFormData (date, brand, weight, category, phr, bundle_count, pipe_count)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (date, brand, weight, category, phr, bundle_count, pipe_count))

    conn.commit()
    conn.close()

st.success("Data saved successfully to the database.")


def display_all_data():
    conn = sqlite3.connect('production_form.db')
    cursor = conn.cursor()

    # Retrieve all data from the database
    cursor.execute('SELECT * FROM SalesFormData')
    data = cursor.fetchall()
    conn.close()
    return data




if __name__ == "__main__":
    main()