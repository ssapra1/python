import streamlit as st
import pandas as pd
import sqlite3


# Function to handle database connection
def create_connection():
    return sqlite3.connect("inputs.db")


# Function to create a table in the database
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Inputs (
            id INTEGER PRIMARY KEY,
            input1 TEXT,
            input2 TEXT,
            input3 TEXT,
            input4 TEXT,
            input5 TEXT,
            input6 TEXT,
            input7 TEXT,
            input8 TEXT,
            input9 TEXT,
            input10 TEXT,
            input11 TEXT,
            input12 TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Function to insert or update row data in the database
def insert_or_update_inputs(row_id, inputs):
    conn = create_connection()
    cursor = conn.cursor()

    # Check if the row exists
    cursor.execute("SELECT COUNT(*) FROM Inputs WHERE id=?", (row_id,))
    exists = cursor.fetchone()[0]

    if exists:
        cursor.execute('''
            UPDATE Inputs
            SET input1=?, input2=?, input3=?, input4=?, input5=?, input6=?,
                input7=?, input8=?, input9=?, input10=?, input11=?, input12=?
            WHERE id=?
        ''', (*inputs, row_id))
    else:
        cursor.execute('''
            INSERT INTO Inputs (id, input1, input2, input3, input4, input5, input6,
                                input7, input8, input9, input10, input11, input12)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row_id, *inputs))

    conn.commit()
    conn.close()


# Streamlit application
def main():
    # Set the layout to 'wide'
    st.set_page_config(layout="wide")

    st.title('CSV Data Editor with Wide Table Format')
    st.markdown(
        "Upload a CSV file and edit the values in a table format with column headers. Save your changes to an SQL database.")

    # Initialize the database
    create_table()

    # Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read CSV file into DataFrame
        df = pd.read_csv(uploaded_file)

        # Ensure the table has 12 columns
        if len(df.columns) < 12:
            st.error("The CSV file must have at least 12 columns.")
            return

        st.subheader("Edit the data below in table format")

        # Display column headers
        column_names = df.columns[:12]
        col_headers = st.columns(12)
        for i, col_name in enumerate(column_names):
            with col_headers[i]:
                st.text(col_name)

        # Iterate over each row and display in a table format
        modified_data = []

        for index, row in df.iterrows():
            # Create columns to mimic a table row
            cols = st.columns(12)
            inputs = []

            for i in range(12):
                with cols[i]:
                    input_value = st.text_input(f"Row {index + 1}, {column_names[i]}", value=str(row[i]))
                    inputs.append(input_value)

            # Store the modified data
            modified_data.append(inputs)

            if st.button(f"Save Row {index + 1}", key=f"save_button_{index}"):
                insert_or_update_inputs(index, inputs)
                st.success(f"Row {index + 1} successfully updated in the database!")


if __name__ == "__main__":
    main()
