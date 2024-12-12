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

            # Display submitted data in a table format
            if submitted:
                st.subheader("Entered Sales Details")
                # Show values in a single-row table
                st.table({
                    "Field": [
                        "Date of Sale",
                        "Party Name",
                        "Category",
                        "Bundle",
                        "Qty (s)",
                        "Total Weight (kg)",
                        "Rate",
                        "Gross Amount",
                        "GST Rate (%)",
                        "GST Amount",
                        "Total Sale",
                        "Name Used",
                        "Amount Received - Date",
                        "Amount Received",
                        "Balance Amount Received - Date",
                        "Balance Received",
                        "Balance",
                        "Comments"
                    ],
                    "Value": [
                        date_of_sale,
                        party_name,
                        other_category if item_sold == "Others" else item_sold,
                        bundle,
                        qty,
                        total_weight,
                        rate,
                        gross_amount,
                        gst_rate,
                        gst_amount,
                        total_sale,
                        name_used,
                        amount_received_date,
                        amount_received,
                        balance_received_date,
                        balance_received,
                        balance,
                        comments
                    ]
                })

                import sqlite3

                def save_to_database(data):
                    # Connect to SQLite database (creates file if it doesn't exist)
                    conn = sqlite3.connect("production_form.db")
                    cursor = conn.cursor()

                    # Create table if not exists
                    cursor.execute("""
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
                    """)

                    # Insert data into the table
                    cursor.execute("""
                        INSERT INTO SalesData (
                            date_of_sale, party_name, category, bundle, qty, total_weight, rate, gross_amount,
                            gst_rate, gst_amount, total_sale, name_used, amount_received_date, amount_received,
                            balance_received_date, balance_received, balance, comments
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, data)

                    # Commit changes and close the connection
                    conn.commit()
                    conn.close()

                if submitted:
                    # Prepare data to be saved to the database
                    category_value = other_category if item_sold == "Others" else item_sold
                    sales_data = (
                        date_of_sale,
                        party_name,
                        category_value,
                        bundle,
                        qty,
                        total_weight,
                        rate,
                        gross_amount,
                        gst_rate,
                        gst_amount,
                        total_sale,
                        name_used,
                        amount_received_date,
                        amount_received,
                        balance_received_date,
                        balance_received,
                        balance,
                        comments
                    )

                    # Save the data
                    save_to_database(sales_data)

                    # Function to fetch and display all records from the database
                    def display_all_records():
                        import sqlite3
                        # Connect to SQLite database
                        conn = sqlite3.connect("production_form.db")
                        cursor = conn.cursor()

                        # Fetch all records from SalesData table
                        cursor.execute("SELECT * FROM SalesData")
                        records = cursor.fetchall()

                        # Define columns for display
                        columns = [
                            "ID", "Date of Sale", "Party Name", "Category", "Bundle", "Qty (s)",
                            "Total Weight (kg)", "Rate", "Gross Amount", "GST Rate (%)", "GST Amount",
                            "Total Sale", "Name Used", "Amount Received - Date", "Amount Received",
                            "Balance Amount Received - Date", "Balance Received", "Balance", "Comments"
                        ]

                        # Display records in Streamlit
                        st.subheader("All Sales Records")
                        if records:
                            st.table({col: [row[idx] for row in records] for idx, col in enumerate(columns)})
                        else:
                            st.write("No records found in the database.")

                    # Call the function to display all records after submission
                    if submitted:
                        display_all_records()

if __name__ == "__main__":
    main()
