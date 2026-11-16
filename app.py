
import os
import json
import mysql.connector

from decimal import Decimal, InvalidOperation

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from database import (
    # Applications
    add_application,
    get_applications,
    get_application,
    update_application,
    delete_application,
    get_statistics,

    # Companies
    get_companies,
    add_company,
    get_company,
    update_company,
    delete_company as delete_company_record,

    # Jobs
    get_jobs,
    get_job,
    add_job,
    update_job,
    delete_job as delete_job_record,

    # Contacts
    get_contacts,
    get_contact,
    add_contact,
    update_contact,
    delete_contact as delete_contact_record
)


# ==========================================
# FLASK CONFIGURATION
# ==========================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "FLASK_SECRET_KEY",
    "development-only-change-this-key"
)

VALID_STATUSES = [
    "Applied",
    "Interview",
    "Accepted",
    "Rejected"
]

JOB_TYPES = [
    "Full-time",
    "Part-time",
    "Contract",
    "Internship"
]


# ==========================================
# APPLICATION FORM VALIDATION
# ==========================================

def read_application_form():

    company_name = request.form.get(
        "company_name", ""
    ).strip()

    job_title = request.form.get(
        "job_title", ""
    ).strip()

    application_date = request.form.get(
        "application_date", ""
    ).strip()

    status = request.form.get(
        "status", ""
    ).strip()

    if not company_name or not job_title or not application_date:
        raise ValueError(
            "Please complete all required fields."
        )

    if status not in VALID_STATUSES:
        raise ValueError(
            "Please select a valid application status."
        )

    if len(company_name) > 100 or len(job_title) > 100:
        raise ValueError(
            "Company name and job title must be 100 characters or fewer."
        )

    return (
        company_name,
        job_title,
        application_date,
        status
    )


# ==========================================
# DASHBOARD
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        try:
            application_data = read_application_form()

            add_application(*application_data)

            flash(
                "Application added successfully!",
                "success"
            )

        except ValueError as error:
            flash(str(error), "error")

        return redirect(url_for("home"))

    search = request.args.get(
        "search", ""
    ).strip()

    status_filter = request.args.get(
        "status", ""
    ).strip()

    if status_filter and status_filter not in VALID_STATUSES:
        status_filter = ""

    applications_data = get_applications(
        search,
        status_filter
    )

    statistics = get_statistics()

    return render_template(
        "index.html",
        applications=applications_data,
        statistics=statistics,
        search=search,
        status_filter=status_filter,
        statuses=VALID_STATUSES
    )


# ==========================================
# APPLICATIONS PAGE
# ==========================================

@app.route(
    "/applications",
    methods=["GET", "POST"]
)
def applications():

    if request.method == "POST":

        try:
            application_data = read_application_form()

            add_application(*application_data)

            flash(
                "Application added successfully!",
                "success"
            )

        except ValueError as error:
            flash(str(error), "error")

        return redirect(url_for("applications"))

    search = request.args.get(
        "search", ""
    ).strip()

    status_filter = request.args.get(
        "status", ""
    ).strip()

    if status_filter and status_filter not in VALID_STATUSES:
        status_filter = ""

    return render_template(
        "applications.html",
        applications=get_applications(
            search,
            status_filter
        ),
        search=search,
        status_filter=status_filter,
        statuses=VALID_STATUSES
    )


# ==========================================
# EDIT APPLICATION
# ==========================================

@app.route(
    "/edit/<int:application_id>",
    methods=["GET", "POST"]
)
def edit(application_id):

    application = get_application(application_id)

    if application is None:
        flash(
            "Application not found.",
            "error"
        )
        return redirect(url_for("applications"))

    if request.method == "POST":

        try:
            application_data = read_application_form()

            update_application(
                application_id,
                *application_data
            )

            flash(
                "Application updated successfully!",
                "success"
            )

            return redirect(url_for("applications"))

        except ValueError as error:
            flash(str(error), "error")

            return redirect(
                url_for(
                    "edit",
                    application_id=application_id
                )
            )

    return render_template(
        "edit.html",
        application=application,
        statuses=VALID_STATUSES
    )


# ==========================================
# DELETE APPLICATION
# ==========================================

@app.route(
    "/delete/<int:application_id>",
    methods=["POST"]
)
def delete(application_id):

    application = get_application(application_id)

    if application is None:
        flash(
            "Application not found.",
            "error"
        )
        return redirect(url_for("applications"))

    delete_application(application_id)

    flash(
        "Application deleted successfully!",
        "success"
    )

    return redirect(url_for("applications"))


# ==========================================
# COMPANIES PAGE
# ==========================================

@app.route(
    "/companies",
    methods=["GET", "POST"]
)
def companies():

    if request.method == "POST":

        company_name = request.form.get(
            "company_name", ""
        ).strip()

        industry = request.form.get(
            "industry", ""
        ).strip()

        website = request.form.get(
            "website", ""
        ).strip()

        city = request.form.get(
            "city", ""
        ).strip()

        state = request.form.get(
            "state", ""
        ).strip()

        notes = request.form.get(
            "notes", ""
        ).strip()

        if not company_name:
            flash(
                "Company name is required.",
                "error"
            )
            return redirect(url_for("companies"))

        if (
            len(company_name) > 100
            or len(industry) > 50
            or len(website) > 200
            or len(city) > 50
            or len(state) > 50
        ):
            flash(
                "One or more fields exceed the maximum allowed length.",
                "error"
            )
            return redirect(url_for("companies"))

        add_company(
            company_name,
            industry,
            website,
            city,
            state,
            notes
        )

        flash(
            "Company added successfully!",
            "success"
        )

        return redirect(url_for("companies"))

    return render_template(
        "companies.html",
        companies=get_companies()
    )


# ==========================================
# EDIT COMPANY
# ==========================================

@app.route(
    "/companies/edit/<int:company_id>",
    methods=["GET", "POST"]
)
def edit_company(company_id):

    company = get_company(company_id)

    if company is None:
        flash(
            "Company not found.",
            "error"
        )
        return redirect(url_for("companies"))

    if request.method == "POST":

        company_name = request.form.get(
            "company_name", ""
        ).strip()

        industry = request.form.get(
            "industry", ""
        ).strip()

        website = request.form.get(
            "website", ""
        ).strip()

        city = request.form.get(
            "city", ""
        ).strip()

        state = request.form.get(
            "state", ""
        ).strip()

        notes = request.form.get(
            "notes", ""
        ).strip()

        if not company_name:
            flash(
                "Company name is required.",
                "error"
            )
            return redirect(
                url_for(
                    "edit_company",
                    company_id=company_id
                )
            )

        if (
            len(company_name) > 100
            or len(industry) > 50
            or len(website) > 200
            or len(city) > 50
            or len(state) > 50
        ):
            flash(
                "One or more fields exceed the maximum allowed length.",
                "error"
            )
            return redirect(
                url_for(
                    "edit_company",
                    company_id=company_id
                )
            )

        update_company(
            company_id,
            company_name,
            industry,
            website,
            city,
            state,
            notes
        )

        flash(
            "Company updated successfully!",
            "success"
        )

        return redirect(url_for("companies"))

    return render_template(
        "edit_company.html",
        company=company
    )


# ==========================================
# DELETE COMPANY
# ==========================================

@app.route(
    "/companies/delete/<int:company_id>",
    methods=["POST"]
)
def delete_company(company_id):

    company = get_company(company_id)

    if company is None:
        flash(
            "Company not found.",
            "error"
        )
        return redirect(url_for("companies"))

    try:
        delete_company_record(company_id)

        flash(
            "Company deleted successfully!",
            "success"
        )

    except mysql.connector.IntegrityError:
        flash(
            "Cannot delete this company because it has related records.",
            "error"
        )

    return redirect(url_for("companies"))


# ==========================================
# JOB FORM VALIDATION
# ==========================================

def read_job_form():

    company_id = request.form.get(
        "company_id", ""
    ).strip()

    job_title = request.form.get(
        "job_title", ""
    ).strip()

    job_type = request.form.get(
        "job_type", ""
    ).strip()

    salary_min_text = request.form.get(
        "salary_min", ""
    ).strip()

    salary_max_text = request.form.get(
        "salary_max", ""
    ).strip()

    posting_url = request.form.get(
        "posting_url", ""
    ).strip()

    date_posted = request.form.get(
        "date_posted", ""
    ).strip()

    skills_text = request.form.get(
        "required_skills", ""
    ).strip()

    if not company_id.isdigit() or int(company_id) < 1:
        raise ValueError(
            "Please select a company."
        )

    if not job_title or len(job_title) > 100:
        raise ValueError(
            "Job title must be between 1 and 100 characters."
        )

    if job_type not in JOB_TYPES:
        raise ValueError(
            "Please select a valid job type."
        )

    if len(posting_url) > 500:
        raise ValueError(
            "Job posting URL is too long."
        )

    try:
        salary_min = (
            Decimal(salary_min_text)
            if salary_min_text
            else None
        )

        salary_max = (
            Decimal(salary_max_text)
            if salary_max_text
            else None
        )

    except InvalidOperation:
        raise ValueError(
            "Please enter valid salary amounts."
        )

    for salary in (salary_min, salary_max):
        if salary is not None and (
            not salary.is_finite()
            or salary < 0
            or salary > 99999999.99
        ):
            raise ValueError(
                "Please enter a valid nonnegative salary."
            )

    if (
        salary_min is not None
        and salary_max is not None
        and salary_min > salary_max
    ):
        raise ValueError(
            "Minimum salary cannot exceed maximum salary."
        )

    valid_company_ids = {
        company["company_id"]
        for company in get_companies()
    }

    if int(company_id) not in valid_company_ids:
        raise ValueError(
            "The selected company does not exist."
        )

    skills = list(dict.fromkeys(
        skill.strip()
        for skill in skills_text.split(",")
        if skill.strip()
    ))

    requirements = json.dumps({
        "required_skills": skills
    })

    return (
        int(company_id),
        job_title,
        job_type,
        salary_min,
        salary_max,
        posting_url or None,
        date_posted or None,
        requirements
    )


# ==========================================
# JOBS PAGE
# ==========================================

@app.route(
    "/jobs",
    methods=["GET", "POST"]
)
def jobs():

    if request.method == "POST":

        try:
            job_data = read_job_form()

            add_job(*job_data)

            flash(
                "Job added successfully!",
                "success"
            )

        except ValueError as error:
            flash(str(error), "error")

        except mysql.connector.IntegrityError:
            flash(
                "Could not add the job. Check the selected company.",
                "error"
            )

        return redirect(url_for("jobs"))

    return render_template(
        "jobs.html",
        jobs=get_jobs(),
        companies=get_companies()
    )


# ==========================================
# EDIT JOB
# ==========================================

@app.route(
    "/jobs/edit/<int:job_id>",
    methods=["GET", "POST"]
)
def edit_job(job_id):

    job = get_job(job_id)

    if job is None:
        flash(
            "Job not found.",
            "error"
        )
        return redirect(url_for("jobs"))

    if request.method == "POST":

        try:
            job_data = read_job_form()

            update_job(
                job_id,
                *job_data
            )

            flash(
                "Job updated successfully!",
                "success"
            )

            return redirect(url_for("jobs"))

        except ValueError as error:
            flash(str(error), "error")

        except mysql.connector.IntegrityError:
            flash(
                "Could not update the job.",
                "error"
            )

        return redirect(
            url_for(
                "edit_job",
                job_id=job_id
            )
        )

    requirements = job.get("requirements")

    if isinstance(requirements, str):
        try:
            requirements = json.loads(requirements)
        except json.JSONDecodeError:
            requirements = {}

    if not isinstance(requirements, dict):
        requirements = {}

    skills = requirements.get(
        "required_skills", []
    )

    if not isinstance(skills, list):
        skills = []

    job["required_skills_text"] = ", ".join(
        str(skill)
        for skill in skills
    )

    return render_template(
        "edit_job.html",
        job=job,
        companies=get_companies()
    )


# ==========================================
# DELETE JOB
# ==========================================

@app.route(
    "/jobs/delete/<int:job_id>",
    methods=["POST"]
)
def delete_job(job_id):

    job = get_job(job_id)

    if job is None:
        flash(
            "Job not found.",
            "error"
        )
        return redirect(url_for("jobs"))

    try:
        delete_job_record(job_id)

        flash(
            "Job deleted successfully!",
            "success"
        )

    except mysql.connector.IntegrityError:
        flash(
            "Cannot delete this job because applications reference it.",
            "error"
        )

    return redirect(url_for("jobs"))


# ==========================================
# CONTACT FORM VALIDATION
# ==========================================

def read_contact_form():

    company_id = request.form.get(
        "company_id", ""
    ).strip()

    first_name = request.form.get(
        "first_name", ""
    ).strip()

    last_name = request.form.get(
        "last_name", ""
    ).strip()

    job_title = request.form.get(
        "job_title", ""
    ).strip()

    email = request.form.get(
        "email", ""
    ).strip()

    phone = request.form.get(
        "phone", ""
    ).strip()

    linkedin_url = request.form.get(
        "linkedin_url", ""
    ).strip()

    notes = request.form.get(
        "notes", ""
    ).strip()

    if not company_id.isdigit() or int(company_id) < 1:
        raise ValueError(
            "Please select a company."
        )

    if not first_name or not last_name:
        raise ValueError(
            "First name and last name are required."
        )

    if (
        len(first_name) > 50
        or len(last_name) > 50
        or len(job_title) > 100
        or len(email) > 100
        or len(phone) > 20
        or len(linkedin_url) > 200
    ):
        raise ValueError(
            "One or more fields exceed the maximum allowed length."
        )

    valid_company_ids = {
        company["company_id"]
        for company in get_companies()
    }

    if int(company_id) not in valid_company_ids:
        raise ValueError(
            "The selected company does not exist."
        )

    return (
        int(company_id),
        first_name,
        last_name,
        job_title or None,
        email or None,
        phone or None,
        linkedin_url or None,
        notes or None
    )


# ==========================================
# CONTACTS PAGE
# ==========================================

@app.route(
    "/contacts",
    methods=["GET", "POST"]
)
def contacts():

    if request.method == "POST":

        try:
            contact_data = read_contact_form()

            add_contact(*contact_data)

            flash(
                "Contact added successfully!",
                "success"
            )

        except ValueError as error:
            flash(str(error), "error")

        except mysql.connector.IntegrityError:
            flash(
                "Could not add the contact. Check the selected company.",
                "error"
            )

        return redirect(url_for("contacts"))

    return render_template(
        "contacts.html",
        contacts=get_contacts(),
        companies=get_companies()
    )


# ==========================================
# EDIT CONTACT
# ==========================================

@app.route(
    "/contacts/edit/<int:contact_id>",
    methods=["GET", "POST"]
)
def edit_contact(contact_id):

    contact = get_contact(contact_id)

    if contact is None:
        flash(
            "Contact not found.",
            "error"
        )
        return redirect(url_for("contacts"))

    if request.method == "POST":

        try:
            contact_data = read_contact_form()

            update_contact(
                contact_id,
                *contact_data
            )

            flash(
                "Contact updated successfully!",
                "success"
            )

            return redirect(url_for("contacts"))

        except ValueError as error:
            flash(str(error), "error")

        except mysql.connector.IntegrityError:
            flash(
                "Could not update the contact.",
                "error"
            )

        return redirect(
            url_for(
                "edit_contact",
                contact_id=contact_id
            )
        )

    return render_template(
        "edit_contact.html",
        contact=contact,
        companies=get_companies()
    )


# ==========================================
# DELETE CONTACT
# ==========================================

@app.route(
    "/contacts/delete/<int:contact_id>",
    methods=["POST"]
)
def delete_contact(contact_id):

    contact = get_contact(contact_id)

    if contact is None:
        flash(
            "Contact not found.",
            "error"
        )
        return redirect(url_for("contacts"))

    try:
        delete_contact_record(contact_id)

        flash(
            "Contact deleted successfully!",
            "success"
        )

    except mysql.connector.IntegrityError:
        flash(
            "Could not delete this contact.",
            "error"
        )

    return redirect(url_for("contacts"))


# ==========================================
# JOB MATCH - SKILL COMPARISON
# ==========================================

def calculate_job_match(job, user_skills):

    requirements = job.get("requirements")

    # Convert JSON text into a Python dictionary
    if isinstance(requirements, str):
        try:
            requirements = json.loads(requirements)
        except json.JSONDecodeError:
            requirements = {}

    if not isinstance(requirements, dict):
        requirements = {}

    required_skills = requirements.get(
        "required_skills", []
    )

    if not isinstance(required_skills, list):
        required_skills = []

    # Remove empty skills and duplicates
    cleaned_skills = []
    seen = set()

    for skill in required_skills:

        if not isinstance(skill, str):
            continue

        skill = skill.strip()
        normalized = skill.casefold()

        if normalized and normalized not in seen:
            cleaned_skills.append(skill)
            seen.add(normalized)

    # Jobs without required skills cannot be scored
    if not cleaned_skills:
        return None

    # Compare skills without case sensitivity
    user_skill_set = {
        skill.strip().casefold()
        for skill in user_skills
        if skill.strip()
    }

    matching_skills = []
    missing_skills = []

    for skill in cleaned_skills:

        if skill.casefold() in user_skill_set:
            matching_skills.append(skill)
        else:
            missing_skills.append(skill)

    match_percentage = round(
        len(matching_skills) / len(cleaned_skills) * 100,
        1
    )

    return {
        "job_id": job["job_id"],
        "job_title": job["job_title"],
        "company_name": job["company_name"],
        "job_type": job.get("job_type"),
        "posting_url": job.get("posting_url"),
        "match_percentage": match_percentage,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills
    }


# ==========================================
# JOB MATCH PAGE
# ==========================================

@app.route(
    "/job-match",
    methods=["GET", "POST"]
)
def job_match():

    skills_input = ""
    results = None

    if request.method == "POST":

        skills_input = request.form.get(
            "skills", ""
        ).strip()

        if not skills_input:
            flash(
                "Please enter at least one skill.",
                "error"
            )

        else:

            user_skills = [
                skill.strip()
                for skill in skills_input.split(",")
                if skill.strip()
            ]

            if not user_skills:
                flash(
                    "Please enter at least one valid skill.",
                    "error"
                )

            else:

                jobs_data = get_jobs()
                results = []

                for job in jobs_data:

                    match = calculate_job_match(
                        job,
                        user_skills
                    )

                    if match is not None:
                        results.append(match)

                # Highest match percentage first
                results.sort(
                    key=lambda result: (
                        -result["match_percentage"],
                        result["job_title"].casefold()
                    )
                )

    return render_template(
        "job_match.html",
        skills_input=skills_input,
        results=results
    )


# ==========================================
# RUN FLASK APPLICATION
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)


