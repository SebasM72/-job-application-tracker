
import os
import mysql.connector


# ==========================================
# DATABASE CONNECTION
# ==========================================

def create_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=os.environ.get("MYSQL_PASSWORD", ""),
        database="job_tracker"
    )


# ==========================================
# APPLICATION DATABASE FUNCTIONS
# ==========================================

def add_application(company_name, job_title, application_date, status):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO applications
                (company_name, job_title, application_date, status)
            VALUES (%s, %s, %s, %s)
        """, (
            company_name,
            job_title,
            application_date,
            status
        ))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def get_applications(search="", status=""):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT
                a.application_id,
                a.job_id,
                COALESCE(c.company_name, a.company_name) AS company_name,
                COALESCE(j.job_title, a.job_title) AS job_title,
                a.application_date,
                a.status
            FROM applications a
            LEFT JOIN jobs j
                ON a.job_id = j.job_id
            LEFT JOIN companies c
                ON j.company_id = c.company_id
            WHERE 1 = 1
        """

        parameters = []

        if search:
            query += """
                AND (
                    COALESCE(c.company_name, a.company_name) LIKE %s
                    OR COALESCE(j.job_title, a.job_title) LIKE %s
                )
            """
            parameters.extend([
                f"%{search}%",
                f"%{search}%"
            ])

        if status:
            query += " AND a.status = %s"
            parameters.append(status)

        query += """
            ORDER BY a.application_date DESC,
                     a.application_id DESC
        """

        cursor.execute(query, tuple(parameters))
        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_application(application_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                a.application_id,
                a.job_id,
                COALESCE(c.company_name, a.company_name) AS company_name,
                COALESCE(j.job_title, a.job_title) AS job_title,
                a.application_date,
                a.status
            FROM applications a
            LEFT JOIN jobs j
                ON a.job_id = j.job_id
            LEFT JOIN companies c
                ON j.company_id = c.company_id
            WHERE a.application_id = %s
        """, (application_id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


def update_application(
    application_id,
    company_name,
    job_title,
    application_date,
    status
):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE applications
            SET company_name = %s,
                job_title = %s,
                application_date = %s,
                status = %s
            WHERE application_id = %s
        """, (
            company_name,
            job_title,
            application_date,
            status,
            application_id
        ))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def delete_application(application_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM applications
            WHERE application_id = %s
        """, (application_id,))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


# ==========================================
# DASHBOARD STATISTICS
# ==========================================

def get_statistics():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                COUNT(*) AS total,

                SUM(
                    CASE
                        WHEN status = 'Applied'
                        THEN 1 ELSE 0
                    END
                ) AS applied,

                SUM(
                    CASE
                        WHEN status IN (
                            'Interview',
                            'Interview Completed'
                        )
                        THEN 1 ELSE 0
                    END
                ) AS interviews,

                SUM(
                    CASE
                        WHEN status IN (
                            'Accepted',
                            'Offer',
                            'Offer Accepted'
                        )
                        THEN 1 ELSE 0
                    END
                ) AS accepted,

                SUM(
                    CASE
                        WHEN status = 'Rejected'
                        THEN 1 ELSE 0
                    END
                ) AS rejected

            FROM applications
        """)

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


# ==========================================
# COMPANIES DATABASE FUNCTIONS
# ==========================================

def get_companies():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                company_id,
                company_name,
                industry,
                website,
                city,
                state,
                notes
            FROM companies
            ORDER BY company_name
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def add_company(
    company_name,
    industry,
    website,
    city,
    state,
    notes
):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO companies (
                company_name,
                industry,
                website,
                city,
                state,
                notes
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            company_name,
            industry,
            website,
            city,
            state,
            notes
        ))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def get_company(company_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                company_id,
                company_name,
                industry,
                website,
                city,
                state,
                notes
            FROM companies
            WHERE company_id = %s
        """, (company_id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


def update_company(
    company_id,
    company_name,
    industry,
    website,
    city,
    state,
    notes
):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE companies
            SET company_name = %s,
                industry = %s,
                website = %s,
                city = %s,
                state = %s,
                notes = %s
            WHERE company_id = %s
        """, (
            company_name,
            industry,
            website,
            city,
            state,
            notes,
            company_id
        ))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def delete_company(company_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM companies
            WHERE company_id = %s
        """, (company_id,))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


# ==========================================
# JOBS DATABASE FUNCTIONS
# ==========================================

def get_jobs():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                j.job_id,
                j.company_id,
                c.company_name,
                j.job_title,
                j.job_type,
                j.salary_min,
                j.salary_max,
                j.posting_url,
                j.date_posted,
                j.requirements
            FROM jobs j
            JOIN companies c
                ON j.company_id = c.company_id
            ORDER BY j.job_id DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_job(job_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                job_id,
                company_id,
                job_title,
                job_type,
                salary_min,
                salary_max,
                posting_url,
                date_posted,
                requirements
            FROM jobs
            WHERE job_id = %s
        """, (job_id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


def add_job(
    company_id,
    job_title,
    job_type,
    salary_min,
    salary_max,
    posting_url,
    date_posted,
    requirements
):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO jobs (
                company_id,
                job_title,
                job_type,
                salary_min,
                salary_max,
                posting_url,
                date_posted,
                requirements
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            company_id,
            job_title,
            job_type,
            salary_min,
            salary_max,
            posting_url,
            date_posted,
            requirements
        ))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def update_job(
    job_id,
    company_id,
    job_title,
    job_type,
    salary_min,
    salary_max,
    posting_url,
    date_posted,
    requirements
):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE jobs
            SET company_id = %s,
                job_title = %s,
                job_type = %s,
                salary_min = %s,
                salary_max = %s,
                posting_url = %s,
                date_posted = %s,
                requirements = %s
            WHERE job_id = %s
        """, (
            company_id,
            job_title,
            job_type,
            salary_min,
            salary_max,
            posting_url,
            date_posted,
            requirements,
            job_id
        ))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def delete_job(job_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM jobs
            WHERE job_id = %s
        """, (job_id,))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


# ==========================================
# CONTACTS DATABASE FUNCTIONS
# ==========================================

def get_contacts():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                ct.contact_id,
                ct.company_id,
                c.company_name,
                ct.first_name,
                ct.last_name,
                ct.job_title,
                ct.email,
                ct.phone,
                ct.linkedin_url,
                ct.notes
            FROM contacts ct
            JOIN companies c
                ON ct.company_id = c.company_id
            ORDER BY ct.contact_id DESC
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()


def get_contact(contact_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT
                contact_id,
                company_id,
                first_name,
                last_name,
                job_title,
                email,
                phone,
                linkedin_url,
                notes
            FROM contacts
            WHERE contact_id = %s
        """, (contact_id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


def add_contact(
    company_id,
    first_name,
    last_name,
    job_title,
    email,
    phone,
    linkedin_url,
    notes
):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO contacts (
                company_id,
                first_name,
                last_name,
                job_title,
                email,
                phone,
                linkedin_url,
                notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            company_id,
            first_name,
            last_name,
            job_title,
            email,
            phone,
            linkedin_url,
            notes
        ))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def update_contact(
    contact_id,
    company_id,
    first_name,
    last_name,
    job_title,
    email,
    phone,
    linkedin_url,
    notes
):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            UPDATE contacts
            SET company_id = %s,
                first_name = %s,
                last_name = %s,
                job_title = %s,
                email = %s,
                phone = %s,
                linkedin_url = %s,
                notes = %s
            WHERE contact_id = %s
        """, (
            company_id,
            first_name,
            last_name,
            job_title,
            email,
            phone,
            linkedin_url,
            notes,
            contact_id
        ))

        connection.commit()

    finally:
        cursor.close()
        connection.close()


def delete_contact(contact_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM contacts
            WHERE contact_id = %s
        """, (contact_id,))

        connection.commit()

    finally:
        cursor.close()
        connection.close()

