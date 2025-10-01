## FastAPI Task Management Application

## OVERVIEW
A web-based task management system built with FastAPI, SQLAlchemy ORM, and Jinja2 templating. It supports user authentication, task creation, status updates, task assignment, and CSV export.

## KEY FEATURES:

1.Secure user signup and login with hashed passwords and JWT authentication.

2.Task CRUD operations with assigned users and status management.

3.Server-rendered HTML frontend using Jinja2 templates.

4.CSV export of tasks.

5.Uses SQLite by default but can be configured for other databases.

6.Ready to deploy on cloud platforms such as Render.

## Technology Stack

1.FastAPI: Python web framework for building APIs.

2.SQLAlchemy: ORM for database operations.

3.Jinja2: Server-side template rendering.

4.Passlib: Password hashing and verification.

4.Python-JOSE: JWT token creation and verification.

5.SQLite: Default relational database.

6.Uvicorn: ASGI server.

7.Additional libraries: python-multipart, email-validator, csvkit, etc.

## REQUIREMENTS

Install dependencies:

pip install -r requirements.txt

## SETUP:

Clone the repository
git clone https://github.com/Sivanth-Raj/Task_collab_app.git

cd Task Collab app

Run the application locally:

uvicorn main:app --reload

Access the app via  http://127.0.0.1:8000/signup

## CONFIGURATION

1.Database connection is configured in database.py using SQLite by default.

2.For production, update SQLALCHEMY_DATABASE_URL to point to a production-grade DB.

3.JWT secret keys and other secrets should be configured as environment variables (recommended).

4.Render or other hosts require environment variables setup and dynamic port using $PORT.

## DEPLOYMENT ON RENDER

1.Add all environment variables in Render dashboard.

2.Use the start command: uvicorn main:app --host 0.0.0.0 --port $PORT

3.Ensure requirements.txt is included.

4.Use persistent storage or managed DB for SQLite data persistence.

## Usage

1.Sign up new users.

2.Log in with credentials.

3.Create, update, assign, and delete tasks.

4.Export task data as CSV for reporting.

5.Dashboard shows task stats and lists.

## Functionality Spotlight

<img width="1919" height="1019" alt="image" src="https://github.com/user-attachments/assets/30a21ef0-543c-4667-819d-d668c30b2758" /> 


<img width="1916" height="1019" alt="image" src="https://github.com/user-attachments/assets/56cb0427-c7f9-47aa-be6d-eaa40dc188db" />  

<img width="1919" height="1020" alt="image" src="https://github.com/user-attachments/assets/553a5ac0-3f5b-450f-a53b-e31cd277c94a" /> 

<img width="1919" height="1020" alt="image" src="https://github.com/user-attachments/assets/f025563d-69d2-4b9e-9bd9-e6beb8a3c029" />


<img width="1919" height="1019" alt="image" src="https://github.com/user-attachments/assets/cc59f0a3-6c88-47eb-928a-c8dccea5b7ab" />                  





