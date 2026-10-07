import streamlit as st
import pandas as pd

from database import connect_db


def show_leads():

    st.title("👥 Lead Management")

    st.write("Add, search and manage potential customers.")

    st.divider()

    # ADD LEAD
    st.subheader("➕ Add New Lead")

    with st.form("lead_form"):

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Lead Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")

        with col2:
            company = st.text_input("Company")

            status = st.selectbox(
                "Status",
                ["New", "Contacted", "Qualified", "Lost"]
            )

            source = st.selectbox(
                "Source",
                ["Website", "LinkedIn", "Referral", "Email", "Other"]
            )

        submitted = st.form_submit_button(
            "➕ Add Lead",
            width="stretch"
        )

        if submitted:

            if name.strip() == "":
                st.error("Lead name is required.")

            else:

                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO leads
                    (
                        name,
                        email,
                        phone,
                        company,
                        status,
                        source
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        name,
                        email,
                        phone,
                        company,
                        status,
                        source
                    )
                )

                conn.commit()
                conn.close()

                st.success("Lead added successfully!")
                st.rerun()

    st.divider()

    # DISPLAY LEADS
    st.subheader("📋 All Leads")

    conn = connect_db()

    df = pd.read_sql_query(
        """
        SELECT
            id,
            name,
            email,
            phone,
            company,
            status,
            source,
            created_at
        FROM leads
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    if df.empty:

        st.info(
            "No leads available. Add your first lead above."
        )

        return

    # SEARCH
    search = st.text_input(
        "🔍 Search Leads",
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
    st.subheader("🗑️ Delete Lead")

    if not df.empty:

        lead_ids = df["id"].tolist()

        selected_id = st.selectbox(
            "Select Lead ID",
            lead_ids
        )

        if st.button(
            "🗑️ Delete Selected Lead",
            width="stretch"
        ):

            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM leads WHERE id = ?",
                (selected_id,)
            )

            conn.commit()
            conn.close()

            st.success("Lead deleted successfully!")

            st.rerun()