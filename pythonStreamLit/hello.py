import streamlit as st 
import pandas as pd
import numpy as np 


## title for webpage 

st.title("Hellow this is my firts web application in python")

## display text

st.write("this is a simple ext ") 

df = pd.DataFrame({
    'first Column':[1,2,3,4],
    'second column':[10,20,30,40]
})

## display the data frame

st.write("Here is teh data frame")

st.write(df)

chart_data=pd.DataFrame(
    np.random.randn(20,3), columns=['a','b','c']
)

st.line_chart(chart_data)
