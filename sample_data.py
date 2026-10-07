from database import connect_db, hash_password


def add_sample_data():

    conn = connect_db()
    cursor = conn.cursor()

    # -----------------------------
    # SALES USER
    # -----------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE username = ?",
        ("sales",)
    )

    if cursor.fetchone()[0] == 0:

        cursor.execute(
            """
            INSERT INTO users
            (username, password, role)
            VALUES (?, ?, ?)
            """,
            (
                "sales",
                hash_password("sales123"),
                "Sales User"
            )
        )

    # -----------------------------
    # LEADS
    # -----------------------------

    leads = [
        (
            "Rahul Sharma",
            "rahul@example.com",
            "9876543210",
            "TechNova Solutions",
            "New",
            "Website"
        ),
        (
            "Priya Reddy",
            "priya@example.com",
            "9876543211",
            "DataWorks Pvt Ltd",
            "Contacted",
            "LinkedIn"
        ),
        (
            "Arjun Kumar",
            "arjun@example.com",
            "9876543212",
            "CloudTech India",
            "Qualified",
            "Referral"
        ),
        (
            "Sneha Rao",
            "sneha@example.com",
            "9876543213",
            "Innovate Labs",
            "Contacted",
            "Email"
        ),
        (
            "Vikram Singh",
            "vikram@example.com",
            "9876543214",
            "Future Systems",
            "Lost",
            "Website"
        )
    ]

    for lead in leads:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM leads
            WHERE email = ?
            """,
            (lead[1],)
        )

        if cursor.fetchone()[0] == 0:

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
                lead
            )

    # -----------------------------
    # CUSTOMERS
    # -----------------------------

    customers = [
        (
            "Ananya Mehta",
            "ananya@example.com",
            "9876500001",
            "Alpha Technologies"
        ),
        (
            "Rohit Verma",
            "rohit@example.com",
            "9876500002",
            "NextGen Systems"
        ),
        (
            "Kavya Nair",
            "kavya@example.com",
            "9876500003",
            "Smart Solutions"
        ),
        (
            "Aditya Patel",
            "aditya@example.com",
            "9876500004",
            "Digital Edge"
        )
    ]

    for customer in customers:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM customers
            WHERE email = ?
            """,
            (customer[1],)
        )

        if cursor.fetchone()[0] == 0:

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
                customer
            )

    # -----------------------------
    # DEALS
    # -----------------------------

    deals = [
        (
            "CRM Implementation",
            "Alpha Technologies",
            150000,
            "Proposal"
        ),
        (
            "AI Analytics Platform",
            "NextGen Systems",
            250000,
            "Negotiation"
        ),
        (
            "Cloud Migration",
            "Smart Solutions",
            180000,
            "Won"
        ),
        (
            "Data Dashboard",
            "Digital Edge",
            120000,
            "Contacted"
        ),
        (
            "Automation Project",
            "Alpha Technologies",
            200000,
            "New"
        ),
        (
            "Security Upgrade",
            "NextGen Systems",
            100000,
            "Lost"
        )
    ]

    for deal in deals:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM deals
            WHERE title = ?
            """,
            (deal[0],)
        )

        if cursor.fetchone()[0] == 0:

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
                deal
            )

    # -----------------------------
    # ACTIVITIES
    # -----------------------------

    activities = [
        (
            "Alpha Technologies",
            "Email",
            "Sent project proposal and pricing details."
        ),
        (
            "NextGen Systems",
            "Phone Call",
            "Discussed requirements and project timeline."
        ),
        (
            "Smart Solutions",
            "Meeting",
            "Completed product demonstration."
        ),
        (
            "Digital Edge",
            "Follow-up",
            "Followed up regarding dashboard requirements."
        ),
        (
            "Alpha Technologies",
            "Email",
            "Shared implementation schedule."
        ),
        (
            "NextGen Systems",
            "Meeting",
            "Discussed contract and final pricing."
        )
    ]

    for activity in activities:

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM activities
            WHERE customer = ?
            AND activity_type = ?
            AND description = ?
            """,
            activity
        )

        if cursor.fetchone()[0] == 0:

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
                activity
            )

    conn.commit()
    conn.close()

    print("Sample data inserted successfully!")


if __name__ == "__main__":

    add_sample_data()