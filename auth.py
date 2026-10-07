import streamlit as st

from database import connect_db, hash_password


def login(username, password):

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT username, role
        FROM users
        WHERE username = ? AND password = ?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        return user

    return None


def show_login():

    st.title("🔐 Enterprise CRM")

    st.subheader("Login to your account")

    st.write(
        "Manage leads, customers, sales and activities."
    )

    st.divider()

    username = st.text_input(
        "Username",
        placeholder="Enter username"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password"
    )

    if st.button(
        "🔑 Login",
        width="stretch"
    ):

        if username.strip() == "" or password.strip() == "":

            st.error(
                "Please enter username and password."
            )

            return

        user = login(
            username,
            password
        )

        if user:

            st.session_state.logged_in = True

            st.session_state.username = user[0]

            st.session_state.role = user[1]

            st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )