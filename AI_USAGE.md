# AI Usage Documentation

**Course:** COP4751 – Advanced Database Management  
**Project:** Job Application Tracker

## 1. Tools Used

I used **ChatGPT by OpenAI** throughout the development of my Job Application Tracker project.

ChatGPT assisted me with Python programming, Flask routes, MySQL database connections, SQL queries, HTML templates, troubleshooting, and documentation.

I used Visual Studio Code to implement the code and MySQL to manage the database.

## 2. Key Prompts

The following are examples of prompts and requests I used while developing my project:

1. "Can you help me with the 404 error?"
2. "The app.py code says there is an error. Can you debug it for me and explain step by step?"
3. "Can you help me fill out the database functions?"

I also requested assistance with creating HTML templates, connecting Flask routes to MySQL, implementing CRUD operations, and developing the Job Match functionality.

## 3. What Worked Well

ChatGPT was particularly helpful when developing the backend of my application.

It provided Python examples for connecting Flask to MySQL and implementing Create, Read, Update, and Delete (CRUD) operations for the companies, jobs, applications, and contacts tables.

AI assistance was also useful when creating HTML templates and connecting them to Flask routes. This helped me develop the six required application sections: Dashboard, Companies, Jobs, Applications, Contacts, and Job Match.

One of the most useful AI-assisted features was the Job Match algorithm. ChatGPT helped generate Python code to compare user-entered skills with required job skills stored in a MySQL JSON column.

The algorithm calculates match percentages, identifies matching and missing skills, and sorts jobs from highest to lowest compatibility.

I tested the algorithm using example jobs and confirmed that a job requiring four skills displayed a 75% match when three requirements were satisfied.

## 4. What I Changed

Although ChatGPT generated code and provided implementation instructions, adjustments were necessary to make the application work with my existing database and project structure.

**Database Compatibility**

I checked the database functions against my actual MySQL tables and column names. The code needed to use the schema already established in my database, including fields such as `posting_url`, `first_name`, `last_name`, and `requirements`.

**Flask Routing**

During testing, I discovered that clicking the Applications navigation link displayed a "404 Not Found" error.

The issue occurred because the HTML navigation linked to `/applications`, but the Flask application did not initially have a corresponding route.

I used ChatGPT to identify the problem, add the missing route, and connect the Applications page to the existing database functions.

**File Organization**

I organized the project into separate Python files, HTML templates, and a CSS stylesheet. I also created additional project files such as `requirements.txt` and `README.md` to prepare the application for submission.

**Testing and Corrections**

I tested the CRUD operations by adding, editing, and deleting sample records. I also tested application search and filtering, Job Match percentages, and job ranking.

These checks helped verify that the AI-assisted code functioned correctly within my local development environment.

## 5. Lessons Learned

This project taught me several important lessons about using generative AI in software development.

First, AI-generated code should not automatically be assumed to work. Even when code looks correct, it must be tested against the actual database structure and application requirements.

Second, providing detailed information about an existing project helps AI generate more relevant code. Information such as table names, column names, file structure, and error messages makes troubleshooting more effective.

Third, I learned that Flask routes, HTML templates, and MySQL database functions must work together for a web application to operate successfully. A missing route or an incorrect database field can prevent a feature from working.

I also gained a better understanding of how JSON can be used to store job requirements and how Python can compare those requirements with user-provided skills.

Finally, I learned that ChatGPT is useful for generating code, explaining programming concepts, and identifying errors, but human verification remains essential.

## Conclusion

ChatGPT was an important development assistant for my Job Application Tracker project. It helped me develop CRUD functionality, connect Flask to MySQL, create HTML templates, implement the Job Match algorithm, and troubleshoot errors.

I used local testing to verify functionality and identify problems that required correction.

This project demonstrated how generative AI can support software development while reinforcing the importance of testing, customization, and understanding the code being implemented.