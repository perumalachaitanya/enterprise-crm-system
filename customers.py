import streamlit as st
import pandas as pd

from database import connect_db


def show_customers():

    st.title("🏢 Customer Management")

    st.write("Manage your existing customers.")

    st.divider()

    # ADD CUSTOMER
    st.subheader("➕ Add New Customer")

    with st.form("customer_form"):

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Customer Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")

        with col2:
            company = st.text_input("Company")

        submitted = st.form_submit_button(
            "➕ Add Customer",
            width="stretch"
        )

        if submitted:

            if name.strip() == "":
                st.error("Customer name is required.")

            else:

                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO customers
                    (
                        name,
                        email,
                        phone,
                        company
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        name,
                        email,
                        phone,
                        company
                    )
                )

                conn.commit()
                conn.close()

                st.success("Customer added successfully!")

                st.rerun()

    st.divider()

    # DISPLAY CUSTOMERS
    st.subheader("📋 All Customers")

    conn = connect_db()

    df = pd.read_sql_query(
        """
        SELECT
            id,
            name,
            email,
            phone,
            company,
            created_at
        FROM customers
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    if df.empty:

        st.info("No customers available.")

        return

    # SEARCH
    search = st.text_input(
        "🔍 Search Customers",
        placeholder="Search by name, email or company..."
    )

    if search:

        df = df[
            df["name"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            df["email"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            df["company"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # DELETE
    st.subheader("🗑️ Delete Customer")

    if not df.empty:

        customer_ids = df["id"].tolist()

        selected_id = st.selectbox(
            "Select Customer ID",
            customer_ids
        )

        if st.button(
            "🗑️ Delete Selected Customer",
            width="stretch"
        ):

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM customers WHERE id = ?",
                (selected_id,)
            )

            conn.commit()
            conn.close()

            st.success("Customer deleted successfully!")

            st.rerun()