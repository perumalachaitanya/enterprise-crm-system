# 📊 Enterprise CRM System

A professional Customer Relationship Management (CRM) web application built with **Python, Streamlit, SQLite and Plotly**.

The system helps businesses manage leads, customers, sales opportunities and customer activities from a centralized dashboard.

---

## 🚀 Project Overview

The Enterprise CRM System provides a simple and user-friendly platform for managing the complete customer relationship process.

It includes:

- Lead management
- Customer management
- Sales pipeline tracking
- Activity and communication logs
- Business analytics dashboard
- Role-based access control
- User management
- SQLite database

---

## ✨ Features

### 📊 Dashboard

The dashboard provides an overview of important CRM metrics:

- Total Leads
- Total Customers
- Total Deals
- Pipeline Value
- Total Activities
- Lead status visualization
- Deal value by stage
- Sales pipeline analysis
- Recent customer activities

---

### 👥 Lead Management

Users can:

- Add new leads
- Store contact information
- Assign lead status
- Track lead source
- Search leads
- Delete leads

Lead statuses include:

- New
- Contacted
- Qualified
- Lost

---

### 🏢 Customer Management

Users can:

- Add customers
- Store customer contact details
- Search customers
- View customer records
- Delete customers

---

### 💼 Sales Pipeline

The sales module allows users to:

- Create deals
- Assign customers
- Set deal values
- Track deal stages
- Monitor total pipeline value
- Monitor won deals
- Monitor active pipeline

Deal stages include:

- New
- Contacted
- Proposal
- Negotiation
- Won
- Lost

---

### 📧 Activities & Email Logs

The system records customer interactions such as:

- Emails
- Phone calls
- Meetings
- Follow-ups
- Notes

Users can also search and filter activity records.

---

### 🔐 Role-Based Access Control

The system supports different user roles.

#### Admin

Admin users have access to:

- Dashboard
- Leads
- Customers
- Sales Pipeline
- Activities
- User Management

#### Sales User

Sales users have access to:

- Dashboard
- Leads
- Customers
- Sales Pipeline
- Activities

User Management is restricted to administrators.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Application logic |
| Streamlit | Web interface |
| SQLite | Database |
| Pandas | Data processing |
| Plotly | Interactive charts |
| Git & GitHub | Version control |

---

## 📁 Project Structure

```text
enterprise-crm-system/
│
├── .streamlit/
│   └── config.toml
│
├── app.py
├── auth.py
├── database.py
├── leads.py
├── customers.py
├── deals.py
├── activities.py
├── users.py
├── sample_data.py
├── crm.db
├── requirements.txt
├── README.md
└── .gitignore