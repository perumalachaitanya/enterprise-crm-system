import streamlit as st
import pandas as pd

from database import connect_db


def show_activities():

    st.title("📧 Activities & Email Logs")

    st.write(
        "Record customer communication, calls, meetings and emails."
    )

    st.divider()

    # ADD ACTIVITY
    st.subheader("➕ Add Activity")

    with st.form("activity_form"):

        col1, col2 = st.columns(2)

        with col1:

            customer = st.text_input(
                "Customer / Lead Name"
            )

            activity_type = st.selectbox(
                "Activity Type",
                [
                    "Email",
                    "Phone Call",
                    "Meeting",
                    "Follow-up",
                    "Note"
                ]
            )

        with col2:

            description = st.text_area(
                "Activity Description"
            )

        submitted = st.form_submit_button(
            "➕ Add Activity",
            width="stretch"
        )

        if submitted:

            if customer.strip() == "":

                st.error(
                    "Customer / Lead name is required."
                )

            elif description.strip() == "":

                st.error(
                    "Activity description is required."
                )

            else:

                conn = connect_db()

                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO activities
                    (
                        customer,
                        activity_type,
                        description
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        customer,
                        activity_type,
                        description
                    )
                )

                conn.commit()

                conn.close()

                st.success(
                    "Activity added successfully!"
                )

                st.rerun()

    st.divider()

    # DISPLAY ACTIVITIES
    st.subheader("📋 Activity History")

    conn = connect_db()

    df = pd.read_sql_query(
        """
        SELECT
            id,
            customer,
            activity_type,
            description,
            created_at
        FROM activities
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()

    if df.empty:

        st.info(
            "No activities recorded yet."
        )

        return

    # FILTER
    activity_filter = st.selectbox(
        "Filter by Activity Type",
        [
            "All",
            "Email",
            "Phone Call",
            "Meeting",
            "Follow-up",
            "Note"
        ]
    )

    if activity_filter != "All":

        df = df[
            df["activity_type"] == activity_filter
        ]

    # SEARCH
    search = st.text_input(
        "🔍 Search Activity",
        placeholder="Search customer or description..."
    )

    if search:

        df = df[
            df["customer"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            df["description"].str.contains(
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
    st.subheader("🗑️ Delete Activity")

    if not df.empty:

        activity_ids = df["id"].tolist()

        selected_id = st.selectbox(
            "Select Activity ID",
            activity_ids
        )

        if st.button(
            "🗑️ Delete Selected Activity",
            width="stretch"
        ):

            conn = connect_db()

            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM activities WHERE id = ?",
                (selected_id,)
            )

            conn.commit()

            conn.close()

            st.success(
                "Activity deleted successfully!"
            )

            st.rerun()