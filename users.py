import streamlit as st
import pandas as pd

from database import connect_db, hash_password


def show_users():

    st.title("👤 User Management")

    st.write(
        "Admin can create and manage CRM users."
    )

    st.divider()

    # -----------------------------------
    # ADD USER
    # -----------------------------------

    st.subheader("➕ Create New User")

    with st.form("user_form"):

        col1, col2 = st.columns(2)

        with col1:

            username = st.text_input(
                "Username"
            )

            password = st.text_input(
                "Password",
                type="password"
            )

        with col2:

            role = st.selectbox(
                "Role",
                [
                    "Sales User",
                    "Admin"
                ]
            )

        submitted = st.form_submit_button(
            "➕ Create User",
            width="stretch"
        )

        if submitted:

            if username.strip() == "":

                st.error(
                    "Username is required."
                )

            elif password.strip() == "":

                st.error(
                    "Password is required."
                )

            else:

                conn = connect_db()

                cursor = conn.cursor()

                try:

                    cursor.execute(
                        """
                        INSERT INTO users
                        (
                            username,
                            password,
                            role
                        )
                        VALUES (?, ?, ?)
                        """,
                        (
                            username,
                            hash_password(password),
                            role
                        )
                    )

                    conn.commit()

                    st.success(
                        "User created successfully!"
                    )

                except Exception:

                    st.error(
                        "Username already exists."
                    )

                conn.close()

    st.divider()

    # -----------------------------------
    # DISPLAY USERS
    # -----------------------------------

    st.subheader("📋 CRM Users")

    conn = connect_db()

    df = pd.read_sql_query(
        """
        SELECT
            id,
            username,
            role
        FROM users
        ORDER BY id
        """,
        conn
    )

    conn.close()

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # -----------------------------------
    # DELETE USER
    # -----------------------------------

    st.subheader("🗑️ Delete User")

    user_ids = df["id"].tolist()

    if user_ids:

        selected_id = st.selectbox(
            "Select User ID",
            user_ids
        )

        if st.button(
            "🗑️ Delete Selected User",
            width="stretch"
        ):

            if selected_id == 1:

                st.error(
                    "The default admin account cannot be deleted."
                )

            else:

                conn = connect_db()

                cursor = conn.cursor()

                cursor.execute(
                    "DELETE FROM users WHERE id = ?",
                    (selected_id,)
                )

                conn.commit()

                conn.close()

                st.success(
                    "User deleted successfully!"
                )

                st.rerun()