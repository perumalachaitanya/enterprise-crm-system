import streamlit as st
import pandas as pd
import plotly.express as px

from database import init_db, connect_db
from auth import show_login
from leads import show_leads
from customers import show_customers
from deals import show_deals
from activities import show_activities
from users import show_users


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="Enterprise CRM",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------------------
# DATABASE
# -----------------------------------

init_db()


# -----------------------------------
# SESSION STATE
# -----------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""


# -----------------------------------
# LOGIN
# -----------------------------------

if not st.session_state.logged_in:

    show_login()

    st.stop()


# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("📊 Enterprise CRM")

st.sidebar.caption(
    "Customer Relationship Management"
)

st.sidebar.divider()

st.sidebar.write(
    f"👤 **{st.session_state.username}**"
)

st.sidebar.write(
    f"🔐 **{st.session_state.role}**"
)

st.sidebar.divider()


menu = [
    "📊 Dashboard",
    "👥 Leads",
    "🏢 Customers",
    "💼 Sales Pipeline",
    "📧 Activities & Emails"
]

if st.session_state.role == "Admin":

    menu.append("👤 User Management")


page = st.sidebar.radio(
    "Navigation",
    menu
)


st.sidebar.divider()

if st.sidebar.button(
    "🚪 Logout",
    width="stretch"
):

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

    st.rerun()


# ===================================
# DASHBOARD
# ===================================

if page == "📊 Dashboard":

    st.title("📊 Enterprise CRM Dashboard")

    st.write(
        "Monitor your customers, leads, sales pipeline and business activities."
    )

    st.divider()

    conn = connect_db()

    leads_df = pd.read_sql_query(
        "SELECT * FROM leads",
        conn
    )

    customers_df = pd.read_sql_query(
        "SELECT * FROM customers",
        conn
    )

    deals_df = pd.read_sql_query(
        "SELECT * FROM deals",
        conn
    )

    activities_df = pd.read_sql_query(
        """
        SELECT *
        FROM activities
        ORDER BY id DESC
        """,
        conn
    )

    conn.close()


    # -----------------------------------
    # KPI CARDS
    # -----------------------------------

    lead_count = len(leads_df)

    customer_count = len(customers_df)

    deal_count = len(deals_df)

    revenue = (
        deals_df["value"].sum()
        if not deals_df.empty
        else 0
    )

    activity_count = len(activities_df)


    col1, col2, col3, col4, col5 = st.columns(5)


    col1.metric(
        "👥 Total Leads",
        lead_count
    )

    col2.metric(
        "🏢 Customers",
        customer_count
    )

    col3.metric(
        "💼 Deals",
        deal_count
    )

    col4.metric(
        "💰 Pipeline Value",
        f"₹{revenue:,.0f}"
    )

    col5.metric(
        "📧 Activities",
        activity_count
    )


    st.divider()


    # ===================================
    # CHART ROW 1
    # ===================================

    col1, col2 = st.columns(2)


    # LEAD STATUS

    with col1:

        st.subheader("👥 Lead Status")

        if not leads_df.empty:

            lead_status = (
                leads_df["status"]
                .value_counts()
                .reset_index()
            )

            lead_status.columns = [
                "Status",
                "Count"
            ]

            fig = px.pie(
                lead_status,
                names="Status",
                values="Count",
                hole=0.45
            )

            fig.update_layout(
                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:

            st.info(
                "No lead data available."
            )


    # DEAL PIPELINE

    with col2:

        st.subheader("💼 Deal Value by Stage")

        if not deals_df.empty:

            pipeline = (
                deals_df
                .groupby("stage")["value"]
                .sum()
                .reset_index()
            )

            pipeline.columns = [
                "Stage",
                "Value"
            ]

            fig = px.bar(
                pipeline,
                x="Stage",
                y="Value",
                text_auto=True
            )

            fig.update_yaxes(
                tickprefix="₹"
            )

            fig.update_layout(
                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:

            st.info(
                "No deal data available."
            )


    st.divider()


    # ===================================
    # CHART ROW 2
    # ===================================

    col1, col2 = st.columns(2)


    # DEAL COUNT

    with col1:

        st.subheader("📈 Deals by Stage")

        if not deals_df.empty:

            stage_count = (
                deals_df["stage"]
                .value_counts()
                .reset_index()
            )

            stage_count.columns = [
                "Stage",
                "Deals"
            ]

            fig = px.bar(
                stage_count,
                x="Stage",
                y="Deals",
                text_auto=True
            )

            fig.update_layout(
                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20
                )
            )

            st.plotly_chart(
                fig,
                width="stretch"
            )

        else:

            st.info(
                "No pipeline data available."
            )


    # RECENT ACTIVITIES

    with col2:

        st.subheader("📧 Recent Activities")

        if not activities_df.empty:

            recent = activities_df.head(5)

            for _, row in recent.iterrows():

                st.write(
                    f"**{row['activity_type']}** "
                    f"— {row['customer']}"
                )

                st.caption(
                    row["description"]
                )

                st.divider()

        else:

            st.info(
                "No activities recorded yet."
            )


# ===================================
# LEADS
# ===================================

elif page == "👥 Leads":

    show_leads()


# ===================================
# CUSTOMERS
# ===================================

elif page == "🏢 Customers":

    show_customers()


# ===================================
# SALES
# ===================================

elif page == "💼 Sales Pipeline":

    show_deals()


# ===================================
# ACTIVITIES
# ===================================

elif page == "📧 Activities & Emails":

    show_activities()


# ===================================
# USERS
# ===================================

elif page == "👤 User Management":

    if st.session_state.role == "Admin":

        show_users()

    else:

        st.error(
            "Access denied. Admin privileges required."
        )