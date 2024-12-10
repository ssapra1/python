import streamlit as st 
import pandas as pd
import numpy as np 

import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def main():
    st.title("CSV File Upload and Display")
    with st.form("my_form1"):

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


if __name__ == "__main__":
    main()