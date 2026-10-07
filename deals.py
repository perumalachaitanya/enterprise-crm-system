import streamlit as st
import pandas as pd

from database import connect_db


def show_deals():

    st.title("💼 Sales Pipeline")

    st.write(
        "Track deals and monitor the sales pipeline."
    )

    st.divider()

    # ADD DEAL
    st.subheader("➕ Add New Deal")

    with st.form("deal_form"):

        col1, col2 = st.columns(2)

        with col1:

            title = st.text_input("Deal Title")

            customer = st.text_input("Customer")

            value = st.number_input(
                "Deal Value (₹)",
                min_value=0.0,
                step=1000.0
            )

        with col2:

            stage = st.selectbox(
                "Deal Stage",
                [
                    "New",
                    "Contacted",
                    "Proposal",
                    "Negotiation",
                    "Won",
                    "Lost"
                ]
            )

        submitted = st.form_submit_button(
            "➕ Add Deal",
            width="stretch"
        )

        if submitted:

            if title.strip() == "":

                st.error(
                    "Deal title is required."
                )

            else:

                conn = connect_db()

                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO deals
                    (
                        title,
                        customer,
                        value,
                        stage
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        title,
                        customer,
                        value,
                        stage
                    )
                )

                conn.commit()

                conn.close()

                st.success(
                    "Deal added successfully!"
                )

                st.rerun()

    st.divider()

    # DISPLAY DEALS
    st.subheader("📋 Sales Pipeline")

    conn = connect_db()

    df = pd.read_sql_query(
        """
        SELECT
            id,
            title,
            customer,
            value,
            stage,
            created_at
        FROM deals
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    if df.empty:

        st.info(
            "No deals available."
        )

        return

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # PIPELINE SUMMARY
    st.subheader("📊 Pipeline Summary")

    col1, col2, col3 = st.columns(3)

    total_value = df["value"].sum()

    won_value = df[
        df["stage"] == "Won"
    ]["value"].sum()

    active_value = df[
        ~df["stage"].isin(
            ["Won", "Lost"]
        )
    ]["value"].sum()

    col1.metric(
        "Total Pipeline",
        f"₹{total_value:,.0f}"
    )

    col2.metric(
        "Won Deals",
        f"₹{won_value:,.0f}"
    )

    col3.metric(
        "Active Pipeline",
        f"₹{active_value:,.0f}"
    )

    st.divider()

    # DELETE DEAL
    st.subheader("🗑️ Delete Deal")

    deal_ids = df["id"].tolist()

    selected_id = st.selectbox(
        "Select Deal ID",
        deal_ids
    )

    if st.button(
        "🗑️ Delete Selected Deal",
        width="stretch"
    ):

        conn = connect_db()

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM deals WHERE id = ?",
            (selected_id,)
        )

        conn.commit()

        conn.close()

        st.success(
            "Deal deleted successfully!"
        )

        st.rerun()