import sqlite3

import pandas as pd
import streamlit as st
from datetime import datetime
import historicaldata
import sales
def main():

    st.title('Production Form for Saxena Industries ')


    st.markdown(
        """
        <style>
        .css-1lcbmhc {
            max-width: 100%;
            padding-left: 1em;
            padding-right: 1em;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Include custom CSS for background image
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("E:/python/productionpyhton/images.jpg");
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.form("my_form"):

        # Add a flag to track validation status

        # Show the error message if validation fails

        # Calendar date selector
        selected_date = st.date_input("Select a date", datetime.now())

        # Dropdown menu
        dropdown_values = ["SAFAL", "SARAS", "ENDO" , "GE", "SVE"]
        selected_brand_option = st.selectbox("Choose a Brand ", dropdown_values)

        dropdown_values = ["LMS (20-40)", "MMS (40-52)", "HMS (52-70)", "Others"]
        selected_category_option = st.selectbox("Choose a Category ", dropdown_values)
        if selected_category_option =="Others":
             other_category = st.text_input("Please specify the category")

        dropdown_values = ["30", "32", "38", "44","48","52","56","60","Others"]
        selected_weight_option = st.selectbox("Choose a Weight ", dropdown_values)
        if selected_weight_option == "Others":
            other_weight = st.text_input("Please specify the Weight")

        # Text input that accepts only numbers with up to three decimal places
        numeric_input = st.text_input("Enter a weight number  (up to three decimals)", value="0.000")
        # Validate the input to ensure it matches the required format
        try:
            float_value = float(numeric_input)
            rounded_value = round(float_value, 3)
            st.write(f"Validated weight: {rounded_value}")
        except ValueError:
            st.write("Please enter a valid weight.")

        dropdown_values = ["70","80","90", "100" ]
        selected_phr_option = st.selectbox("Choose a PHR ", dropdown_values)

        # Dropdown menu with Yes and No options
        yes_no_option = st.selectbox("Select DOP", ["Yes", "No"])

        dropdown_values = ["6", "7","8","9","10","Others"]
        selected_batch_option = st.selectbox("Choose a batch ", dropdown_values)
        if selected_batch_option == "Others":
            other_batch = st.text_input("Please specify the batch")

        is_valid = True
        error_message = ""

        # Highlight fields with validation errors

        # Validations for each field
        if not selected_date:
            is_valid = False
            error_message += "Please select a valid date.\n"

        if not selected_brand_option:
            is_valid = False
            error_message += "Please select a brand option.\n"

        if not selected_category_option:
            is_valid = False
            error_message += "Please select a category option.\n"

        if selected_category_option == "Others" and not other_category:
            is_valid = False
            error_message += "Please specify the category for 'Others'.\n"

        if not selected_weight_option:
            is_valid = False
            error_message += "Please select a weight option.\n"

        if selected_weight_option == "Others" and not other_weight:
            is_valid = False
            error_message += "Please specify the weight for 'Others'.\n"

        if not numeric_input:
            is_valid = False
            error_message += "Please enter a valid numeric weight value.\n"
        else:
            try:
                float_value = float(numeric_input)
                rounded_value = round(float_value, 3)
            except ValueError:
                is_valid = False
                error_message += "The weight value must be a valid number up to three decimals.\n"

        if not selected_phr_option:
            is_valid = False
            error_message += "Please select a PHR option.\n"

        if not yes_no_option:
            is_valid = False
            error_message += "Please select a DOP option.\n"

        if not selected_batch_option:
            is_valid = False
            error_message += "Please select a batch option.\n"

        if selected_batch_option == "Others" and not other_batch:
            is_valid = False
            error_message += "Please specify the batch for 'Others'.\n"

        if not is_valid:
            st.error("The form contains the following errors:\n" + error_message)
        st.write("Please fill out the form below:")

        if not is_valid:
            st.error("The form contains the following errors:\n" + error_message)

            # Highlight errors by displaying the fields with issues again
            if not selected_date:
                st.warning("⚠️ Please select a valid date.")

            if not selected_brand_option:
                st.warning("⚠️ Please select a brand option.")

            if not selected_category_option:
                st.warning("⚠️ Please select a category option.")
            elif selected_category_option == "Others" and not other_category:
                st.warning("⚠️ Please specify the category for 'Others'.")

            if not selected_weight_option:
                st.warning("⚠️ Please select a weight option.")
            elif selected_weight_option == "Others" and not other_weight:
                st.warning("⚠️ Please specify the weight for 'Others'.")

            if not numeric_input:
                st.warning("⚠️ Please enter a valid numeric weight value.")
            else:
                try:
                    float_value = float(numeric_input)
                    rounded_value = round(float_value, 3)
                except ValueError:
                    st.warning("⚠️ The weight value must be a valid number up to three decimals.")

            if not selected_phr_option:
                st.warning("⚠️ Please select a PHR option.")

            if not yes_no_option:
                st.warning("⚠️ Please select a DOP option.")

            if not selected_batch_option:
                st.warning("⚠️ Please select a batch option.")
            elif selected_batch_option == "Others" and not other_batch:
                st.warning("⚠️ Please specify the batch for 'Others'.")
        # Submit button

        submitted = st.form_submit_button("Submit")

    import sqlite3
    def insert_into_database(data):
        # Connect to the SQLite database (or creates it if it doesn't exist)
        conn = sqlite3.connect('production_form.db')
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute('''
                 CREATE TABLE IF NOT EXISTS form_data (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     date TEXT,
                     brand TEXT,
                     category TEXT,
                     weight TEXT,
                     entered_weight_number TEXT,
                     phr TEXT,
                     dop TEXT,
                     batch TEXT
                 )
             ''')

        # Insert the data into the table
        cursor.execute('''
                 INSERT INTO form_data (date, brand, category, weight, entered_weight_number, phr, dop, batch)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)
             ''', (
            data["Date"][0],
            data["Brand"][0],
            data["Category"][0],
            data["Weight"][0],
            data["Entered Weight Number"][0],
            data["PHR"][0],
            data["DOP"][0],
            data["Batch"][0]
        ))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

    # In the submit section, call this function
    if submitted and is_valid:
        st.success("Data submitted successfully!")

        import pandas as pd

        # Prepare the data for the table
        data = {
            "Date": [selected_date],
            "Brand": [selected_brand_option],
            "Category": [
                f"{selected_category_option} - {other_category}" if selected_category_option == "Others" else selected_category_option
            ],
            "Weight": [
                f"{selected_weight_option} - {other_weight}" if selected_weight_option == "Others" else selected_weight_option
            ],
            "Entered Weight Number": [rounded_value if numeric_input else "N/A"],
            "PHR": [selected_phr_option],
            "DOP": [yes_no_option],
            "Batch": [
                f"{selected_batch_option} - {other_batch}" if selected_batch_option == "Others" else selected_batch_option
            ],
        }

        # Insert the data into the database
        insert_into_database(data)

        # Create a DataFrame and display it
        df = pd.DataFrame(data)
        st.write(df.style.set_table_styles(
            [{'selector': 'table', 'props': [('width', '100%')]}]
        ))
        all_data = get_all_data_from_database()
        if all_data:
            # Define column headers based on the table schema
            column_headers = ["ID", "Date", "Brand", "Category", "Weight", "Entered Weight Number", "PHR", "DOP",
                              "Batch"]

            # Use pandas to create a DataFrame and display it
            df_all_data = pd.DataFrame(all_data, columns=column_headers)
            st.write("All Submitted Data:")
            st.write(df_all_data.style.set_table_styles(
                [{'selector': 'table', 'props': [('width', '100%')]}]
            ))
        else:
            st.write("No data found in the database.")

        # Reset the form fields after submission using session state

        # Function to retrieve all records from database


def get_all_data_from_database():
    # Connect to the SQLite database
    conn = sqlite3.connect('production_form.db')
    cursor = conn.cursor()

    # Retrieve all records from the form_data table
    cursor.execute('SELECT * FROM form_data')
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    return rows


# Fetch all data and display it in a table


if __name__ == "__main__":
    main()
