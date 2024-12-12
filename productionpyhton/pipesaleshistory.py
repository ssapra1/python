
def main():
    import streamlit as st
    import pandas as pd
    import sqlite3

    # Define required columns
    required_columns = [
        "Date of Sale", "Party Name", "Item Sold", "Bundle", "Qty( s)", "total weight",
        "Rate", "Gross Amount", "GST rate", "GST Amount", "Total Sale", "Name Used",
        "Amount Received- Date", "Amount Received", "Balance Amount Received- Date",
        "Balance Amount Received", "Balance", "Commnets"
    ]

    # Streamlit app
    st.title("Sales Data File Uploader")

    st.markdown("""
    Upload multiple files containing sales data.
    The app validates whether uploaded files contain the required columns.
    """)

    # File uploader for multiple files
    uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Display file name
            st.subheader(f"File: {uploaded_file.name}")

            try:
                # Read file into DataFrame
                df = pd.read_csv(uploaded_file)

                # Check if all required columns are in the uploaded file
                missing_columns = [col for col in required_columns if col not in df.columns]
                if not missing_columns:
                    st.success("All required columns are present!")
                    st.dataframe(df)  # Display the loaded DataFrame

                    # Establish database connection (or create database if it doesn't exist)
                    conn = sqlite3.connect("production_form.db")
                    cursor = conn.cursor()

                    # Create a table if it doesn't already exist
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS SalesData (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        [Date of Sale] TEXT,
                        [Party Name] TEXT,
                        [Item Sold] TEXT,
                        [Bundle] TEXT,
                        [Qty( s)] INTEGER,
                        [total weight] REAL,
                        [Rate] REAL,
                        [Gross Amount] REAL,
                        [GST rate] REAL,
                        [GST Amount] REAL,
                        [Total Sale] REAL,
                        [Name Used] TEXT,
                        [Amount Received- Date] TEXT,
                        [Amount Received] REAL,
                        [Balance Amount Received- Date] TEXT,
                        [Balance Amount Received] REAL,
                        [Balance] REAL,
                        [Commnets] TEXT
                    )
                    """)
                    conn.commit()

                    # Store the data into the database
                    df.to_sql('SalesData', conn, if_exists='append', index=False)

                    st.success("Data successfully added to the database!")
                else:
                    st.error(f"The following required columns are missing: {', '.join(missing_columns)}")
            except Exception as e:
                st.error(f"Error reading file {uploaded_file.name}: {e}")
            finally:
                if 'conn' in locals():
                    conn.close()

    # Add a section to display all data from the database
    st.title("View All Sales Data")

    try:
        # Establish database connection
        conn = sqlite3.connect("production_form.db")
        cursor = conn.cursor()

        # Query all data from the SalesData table
        cursor.execute("SELECT * FROM SalesData")
        all_data = cursor.fetchall()

        # Fetch column names from the table for headers
        cursor.execute("PRAGMA table_info(SalesData)")
        column_names = [info[1] for info in cursor.fetchall()]

        # Display data in a table format if available
        if all_data:
            st.subheader("All Sales Data")
            st.write("Below is the data stored in the database:")
            df_all_data = pd.DataFrame(all_data, columns=column_names)
            st.dataframe(df_all_data)  # Streamlit table
        else:
            st.info("No data found in the database.")
    except Exception as view_all_error:
        st.error(f"Error while retrieving data: {view_all_error}")
    finally:
        conn.close()


# Call the main function
if __name__ == "__main__":
    main()

# Streamlit app
