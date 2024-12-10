# Extend sidebar navigation with logic for application switching

import Productionhistoricaldata
import sales
import streamlit as st
import productionform
import SalesHistoricalData

def main():

    st.write('')

if "app_page" not in st.session_state:
    st.session_state["app_page"] = "Home"
    st.sidebar.image("images.jpg", use_container_width=True)

def navigate_to(app_name):

    st.session_state["app_page"] = app_name


if st.sidebar.button("Go to Production"):
    navigate_to("Production")

if st.sidebar.button("Go to Sales"):
    navigate_to("Sales")

if st.sidebar.button("HistoricalData for Production"):
    navigate_to("HistoricalData")

if st.sidebar.button("HistoricalData for Sales"):
    navigate_to("SalesHistoricalData")

if st.sidebar.button("Home"):
    navigate_to("Home")


# Logic to render different applications based on selection
if st.session_state["app_page"] == "Home":
    st.write("Welcome to the Home Page.")
elif st.session_state["app_page"] == "Production":
    st.write("You are in Production")
    productionform.main()
elif st.session_state["app_page"] == "Sales":
    st.write("You are in Sales.")
    sales.main()
elif st.session_state["app_page"] == "HistoricalData":
    st.write("You are in HistoricalData.")
    Productionhistoricaldata.main()
elif st.session_state["app_page"] == "SalesHistoricalData":
    st.write("You are in SalesHistoricalData.")
    SalesHistoricalData.main()

if __name__ == "__main__":
    main()
