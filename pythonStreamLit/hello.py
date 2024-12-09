import streamlit as st 
import pandas as pd
import numpy as np 

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def upload_and_display_csv():
    st.title("CSV File Upload and Display")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    submitted1 = st.form_submit_button('Submit 1')
    st.write(submitted1)
    if submitted1:
       if uploaded_file is not None:
        time.sleep(20)
        data = pd.read_csv(uploaded_file)

        st.write("Here is the uploaded file's data:")
        st.dataframe(data)

        st.line_chart(data)
        st.write("Material-style data table:")
