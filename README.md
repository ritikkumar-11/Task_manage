# Task_manage
Below is a comprehensive guide for creating a **README.md** file to document how to run the project locally, as well as instructions for testing the API endpoints using either **Postman** or **cURL**.

---

# Task Management API

This is a Django-based RESTful API for managing tasks. Users can register, log in, create tasks, filter tasks, and manage their own tasks. Admin users have additional privileges to view all tasks.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Running the Project Locally](#running-the-project-locally)
4. [API Endpoints](#api-endpoints)
5. [Testing the API](#testing-the-api)
   - [Using Postman](#using-postman)
   - [Using cURL](#using-curl)

---

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package manager)
- Virtualenv (optional but recommended)
- PostgreSQL or SQLite (depending on your database setup)
- Node.js (if you plan to use a frontend framework like React)

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-repo/task-management-api.git
   cd task-management-api
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: `env\Scripts\activate`
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**

   Create a `.env` file in the root directory and add the following environment variables:

   ```env
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3  # Or your PostgreSQL URL
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Run Migrations**

   Apply migrations to set up the database schema:

   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser (Optional)**

   Create an admin user to access the Django admin panel:

   ```bash
   python manage.py createsuperuser
   ```

---

## Running the Project Locally

1. **Start the Development Server**

   ```bash
   python manage.py runserver
   ```

   The server will start at `http://localhost:8000`.

2. **Access the API Documentation**

   Visit the API root at `http://localhost:8000/api/` to see available endpoints.

3. **Admin Panel**

   Access the Django admin panel at `http://localhost:8000/admin/` using the superuser credentials.

---

## API Endpoints

| Endpoint                  | Method | Description                                   | Authentication Required |
|---------------------------|--------|-----------------------------------------------|-------------------------|
| `/api/register/`          | POST   | Register a new user                           | No                      |
| `/api/token/`             | POST   | Obtain JWT tokens for authentication          | No                      |
| `/api/tasks/`             | GET    | List tasks for the logged-in user             | Yes                     |
| `/api/tasks/`             | POST   | Create a new task                             | Yes                     |
| `/api/tasks/{id}/`        | GET    | Retrieve a specific task                      | Yes                     |
| `/api/tasks/{id}/`        | PUT    | Update a specific task                        | Yes                     |
| `/api/tasks/{id}/`        | DELETE | Delete a specific task                        | Yes                     |
| `/api/tasks/all_tasks/`   | GET    | List all tasks (admin only)                   | Yes (Admin Only)        |

---

## Testing the API

### Using Postman

1. **Download Postman**
   - Download and install Postman from [here](https://www.postman.com/downloads/).

2. **Import the Postman Collection**
   - Import the provided Postman collection (`task_management_api.postman_collection.json`) into Postman.

3. **Test the Endpoints**
   - Use the imported collection to test all endpoints. Ensure you include the `Authorization` header with the JWT token for protected endpoints.

   Example:
   - **Header**: `Authorization: Bearer <your_access_token_here>`

---

### Using cURL

You can also test the API using `cURL` commands. Below are examples for each endpoint:

#### 1. Register a New User

```bash
curl -X POST http://localhost:8000/api/register/ \
-H "Content-Type: application/json" \
-d '{
    "username": "new_user",
    "email": "new_user@example.com",
    "password": "secure_password",
    "confirm_password": "secure_password"
}'
```
![alt text](<Screenshot from 2025-03-16 19-02-58.png>)
#### 2. Obtain JWT Tokens

```bash
curl -X POST http://localhost:8000/api/token/ \
-H "Content-Type: application/json" \
-d '{
    "username": "new_user",
    "password": "secure_password"
}'
```
![alt text](<Screenshot from 2025-03-16 19-03-06.png>)
Save the `access` and `refresh` tokens from the response.

#### 3. List Tasks for the Logged-In User

```bash
curl -X GET http://localhost:8000/api/tasks/ \
-H "Authorization: Bearer <your_access_token_here>"
```

#### 4. Create a New Task

```bash
curl -X POST http://localhost:8000/api/tasks/ \
-H "Authorization: Bearer <your_access_token_here>" \
-H "Content-Type: application/json" \
-d '{
    "title": "New Task",
    "description": "This is a new task.",
    "completed": false
}'
```
![alt text](<Screenshot from 2025-03-16 19-03-18.png>)
#### 5. Retrieve a Specific Task

```bash
curl -X GET http://localhost:8000/api/tasks/1/ \
-H "Authorization: Bearer <your_access_token_here>"
```
![alt text](<Screenshot from 2025-03-16 19-05-58.png>)
#### 6. Update a Specific Task

```bash
curl -X PUT http://localhost:8000/api/tasks/1/ \
-H "Authorization: Bearer <your_access_token_here>" \
-H "Content-Type: application/json" \
-d '{
    "title": "Updated Task",
    "description": "This task has been updated.",
    "completed": true
}'
```
![alt text](<Screenshot from 2025-03-16 19-06-04.png>)
#### 7. Delete a Specific Task

```bash
curl -X DELETE http://localhost:8000/api/tasks/1/ \
-H "Authorization: Bearer <your_access_token_here>"
```
![alt text](<Screenshot from 2025-03-16 19-06-07.png>)
#### 8. List All Tasks (Admin Only)

```bash
curl -X GET http://localhost:8000/api/tasks/all_tasks/ \
-H "Authorization: Bearer <your_admin_access_token_here>"
```

---
![alt text](<Screenshot from 2025-03-16 19-17-55.png>)
![alt text](<Screenshot from 2025-03-16 19-14-26.png>)
## Additional Notes

- **JWT Tokens**: Use the `access` token for authenticated requests. If the token expires, refresh it using the `/api/token/refresh/` endpoint.
- **Error Handling**: The API returns appropriate HTTP status codes and error messages for invalid requests.
- **Filters**: You can filter tasks by `completed=true/false`, `created_after=YYYY-MM-DD`, and `created_before=YYYY-MM-DD`.

---

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request.

---



