# main.py
import streamlit as st
import authenticator
import hello
import valuesform as valueform


if __name__ == "__main__":
    text_input1 = st.text_input("Enter first string")
    text_input2 = st.text_input("Enter second string")
    st.title("Login")
    login_button = st.button("Login")
    flag=authenticator.authenticate(text_input1, text_input2)
    if login_button:
       if flag:
           st.sidebar.error("login success")
           hello.upload_and_display_csv()
       else:
          st.sidebar.error("Invalid username or password")
          valueform.multiform()
