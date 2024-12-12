
def main():
    import streamlit as st
    import pandas as pd
    import sqlite3

    # Define required columns
    # Define required columns
    required_columns = [
        "id", "date_of_sale", "party_name", "category", "bundle", "qty", "total_weight", "rate",
        "gross_amount", "gst_rate", "gst_amount", "total_sale", "name_used", "amount_received_date",
        "amount_received", "balance_received_date", "balance_received", "balance", "comments"
    ]

    # File upload functionality for multiple CSV files
    uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
    if uploaded_files:
        all_data = []  # List to hold validated DataFrames
        for file in uploaded_files:
            try:
                # Read the uploaded file into a DataFrame
                df = pd.read_csv(file)
                # Check if required columns are present
                if all(column in df.columns for column in required_columns):
                    all_data.append(df)  # Append valid DataFrame to list
                else:
                    st.error(f"The file '{file.name}' is missing one or more required columns.")

            except Exception as e:
                st.error(f"Error reading file '{file.name}': {e}")
        # When we have valid data, concatenate and display it
        if all_data:
            combined_data = pd.concat(all_data, ignore_index=True)
            st.write("Uploaded Data Display:")
            st.dataframe(combined_data)

            # Drop the 'id' column if it exists
            if 'id' in combined_data.columns:
                combined_data = combined_data.drop('id', axis=1)
            # Database connection and insertion
            conn = sqlite3.connect('production_form.db')  # Create/connect to SQLite database
            cursor = conn.cursor()
            # Create table if it does not exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS SalesData (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date_of_sale TEXT,
                    party_name TEXT,
                    category TEXT,
                    bundle TEXT,
                    qty INTEGER,
                    total_weight REAL,
                    rate REAL,
                    gross_amount REAL,
                    gst_rate REAL,
                    gst_amount REAL,
                    total_sale REAL,
                    name_used TEXT,
                    amount_received_date TEXT,
                    amount_received REAL,
                    balance_received_date TEXT,
                    balance_received REAL,
                    balance REAL,
                    comments TEXT
                )
            ''')
            conn.commit()
            # Insert the data into the database
            combined_data.to_sql('SalesData', conn, if_exists='append', index=False)
            st.success("Data successfully added to the database!")
            # Close the database connection
            conn.close()

            # Display all the data from the database in a table format
            conn = sqlite3.connect('production_form.db')  # Reconnect to SQLite database
            cursor = conn.cursor()

            # Fetch all data from the table
            cursor.execute("SELECT * FROM SalesData")
            data = cursor.fetchall()

            # Get the column names for the table
            columns = [description[0] for description in cursor.description]

            # Display the data in a table format
            st.write("All Data from Database:")
            st.table(pd.DataFrame(data, columns=columns))

            # Close the database connection after fetching and displaying
            conn.close()
