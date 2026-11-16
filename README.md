# Job Application Tracker

## Project Overview

The Job Application Tracker is a web application developed using Python, Flask, and MySQL. It helps users organize companies, job opportunities, applications, and professional contacts.

The application also includes a Job Match feature that compares users' technical skills against job requirements.

## Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- MySQL Connector/Python

## Features

### Dashboard
Displays application information and statistics.

### Companies
Allows users to add, view, edit, and delete company records.

### Jobs
Allows users to manage job opportunities, including salaries, employment types, posting URLs, and required skills.

### Applications
Allows users to track job applications, update their statuses, and search or filter application records.

### Contacts
Allows users to manage professional contacts associated with companies.

### Job Match
Compares user-entered skills against job requirements stored in MySQL.

The system calculates match percentages, identifies matching and missing skills, and ranks jobs from highest to lowest match.

## Installation

1. Install Python and MySQL.
2. Download or clone the project repository.
3. Install the required Python packages:

   `pip install -r requirements.txt`

4. Create the MySQL database using the provided `schema.sql` file.
5. Configure the database connection in `database.py`. Set the `MYSQL_PASSWORD` environment variable to your local MySQL password.
6. Start the Flask application:

   `python3 app.py`

7. Open `http://127.0.0.1:5000` in your browser.

## Database

The application uses a MySQL database named `job_tracker`.

The main tables are:

- companies
- jobs
- applications
- contacts

## Job Matching Algorithm

The Job Match feature uses the following calculation:

Match Percentage = (Number of Matching Skills / Total Required Skills) × 100

Jobs are displayed in descending order of match percentage.

## Project Status

The main application features have been implemented and tested locally. Final documentation and submission preparation are in progress.