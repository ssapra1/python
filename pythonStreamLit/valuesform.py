
import streamlit as st
import sqlite3


# Function to create a database connection
def create_connection():
    conn = sqlite3.connect("inputs.db")
    return conn


# Function to create table
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
            input8 TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Function to insert inputs into the database
def insert_inputs(inputs):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Inputs (input1, input2, input3, input4, input5, input6, input7, input8)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', inputs)
    conn.commit()
    conn.close()


# Streamlit application
def multiform():

    st.title('Welcome to the Multi-Input Webpage')

    st.write('''
    This simple webpage allows you to input multiple text entries, which will be saved to our database. 
    Please fill out each field below and click the "Save Inputs" button to store your entries.
    ''')

    st.header('Input Form')

    # Create database and table
    create_table()

    # Layout columns for inputs
    col1, col2 = st.columns(2)

    with col1:
        input1 = st.text_input("Enter text for input 1")
        input2 = st.text_input("Enter text for input 2")
        input3 = st.text_input("Enter text for input 3")
        input4 = st.text_input("Enter text for input 4")

    with col2:
        input5 = st.text_input("Enter text for input 5")
        input6 = st.text_input("Enter text for input 6")
        input7 = st.text_input("Enter text for input 7")
        input8 = st.text_input("Enter text for input 8")

    # Collect inputs
    inputs = (input1, input2, input3, input4, input5, input6, input7, input8)

    if st.button("Save Inputs"):
        insert_inputs(inputs)
        st.success("Inputs successfully saved to database!")


