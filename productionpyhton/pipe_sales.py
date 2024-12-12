import streamlit as st


def main():
    st.title("Sales Entry Form")

    # Streamlit form
    with st.form("sales_form"):
        st.subheader("Enter Sales Details")

        # Input fields
        date_of_sale = st.date_input("Date of Sale")
        party_name = st.text_input("Party Name")
        dropdown_values = ["LMS (20-40)", "MMS (40-52)", "HMS (52-70)", "Others"]
        item_sold = st.selectbox("Choose a Category ", dropdown_values)
        if item_sold == "Others":
            other_category = st.text_input("Please specify the category")
        bundle = st.text_input("Bundle")
        qty = st.number_input("Qty (s)", min_value=0, step=1)
        total_weight = st.number_input("Total Weight (kg)", min_value=0.0, step=0.1)
        rate = st.number_input("Rate", min_value=0.0, step=0.01)
        gross_amount = st.number_input("Gross Amount", min_value=0.0, step=0.01)
        gst_rate = st.number_input("GST Rate (%)", min_value=0.0, step=0.01)
        gst_amount = st.number_input("GST Amount", min_value=0.0, step=0.01)
        total_sale = st.number_input("Total Sale", min_value=0.0, step=0.01)
        name_used = st.text_input("Name Used")
        amount_received_date = st.date_input("Amount Received - Date")
        amount_received = st.number_input("Amount Received", min_value=0.0, step=0.01)
        balance_received_date = st.date_input("Balance Amount Received - Date")
        balance_received = st.number_input("Balance Amount Received", min_value=0.0, step=0.01)
        balance = st.number_input("Balance", min_value=0.0, step=0.01)
        comments = st.text_area("Comments")

        # Form submission
        submitted = st.form_submit_button("Submit")

        if submitted:
            st.success("Form submitted successfully!")
            st.write("Here are the details you submitted:")
            st.json({
                "Date of Sale": str(date_of_sale),
                "Party Name": party_name,
                "Item Sold": item_sold,
                "Bundle": bundle,
                "Qty (s)": qty,
                "Total Weight": total_weight,
                "Rate": rate,
                "Gross Amount": gross_amount,
                "GST Rate": gst_rate,
                "GST Amount": gst_amount,
                "Total Sale": total_sale,
                "Name Used": name_used,
                "Amount Received - Date": str(amount_received_date),
                "Amount Received": amount_received,
                "Balance Amount Received - Date": str(balance_received_date),
                "Balance Amount Received": balance_received,
                "Balance": balance,
                "Comments": comments
            })


if __name__ == "__main__":
    main()
