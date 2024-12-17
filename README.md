# RBAC Backend API

This project is an implementation of Role-Based Access Control (RBAC) for managing users, roles, permissions, and access validation.

## Features
- User Management (Create, Retrieve, Assign Roles)
- Role Management (Predefined Roles, Dynamic Permissions)
- Permission Management
- Access Validation
- Audit Logging

## Hosted Backend
**Base URL**: soory Deu to some technical issu not done by me(if want i will show in local-host)

## Setup Instructions
1. Clone the repository:
   git https://github.com/pradeepprasad12/rbac.git

2.Set up the virtual environment:

python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate  # Windows

3.Install dependencies:
pip install -r requirements.txt

4.Configure the .env file:

SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_NAME=your-database-name
DATABASE_USER=your-database-user
DATABASE_PASSWORD=your-database-password
DATABASE_HOST=your-database-host
DATABASE_PORT=3306

5.Apply migrations:

python manage.py makemigrations
python manage.py migrate

6.Run the server locally:

python manage.py runserver

7.Postman Collection
## 1.User Management

i) Create User
URL: /api/users/
Method: POST
Request Body:
json-
{
  "username": "example_user",
  "email": "example_user@example.com",
  "password": "example_password"
}
Response (Success):
{
  "success": true,
  "message": "User created successfully.",
  "data": {
    "id": 1,
    "username": "example_user",
    "email": "example_user@example.com"
  }
}
Response (Error):
{
  "success": false,
  "message": {
    "username": ["This field is required."],
    "email": ["Invalid email address."]
  }
}

ii) Retrieve User List
URL: /api/users/
Method: GET
Response (Success):

{
  "success": true,
  "message": "User list retrieved successfully.",
  "data": [
    {
      "id": 1,
      "username": "example_user",
      "email": "example_user@example.com",
      "role": "Staff"
    },
    {
      "id": 2,
      "username": "admin_user",
      "email": "admin@example.com",
      "role": "Admin"
    }
  ]
}

iii) Assign Role to User
URL: /api/users/<user_id>/assign_role/
Method: PATCH
Request Body:

{
  "role_id": 2
}
Response (Success):

{
  "success": true,
  "message": "Role assigned successfully."
}
Response (Error):

{
  "success": false,
  "message": "Role does not exist."
}

## 2. Role Management
i) Retrieve Role List
URL: /api/roles/
Method: GET
Response:

{
  "success": true,
  "message": "Role list retrieved successfully.",
  "data": [
    {
      "id": 1,
      "name": "Staff",
      "permissions": ["API_ONE", "API_TWO"]
    },
    {
      "id": 2,
      "name": "Admin",
      "permissions": ["API_ONE", "API_TWO", "API_THREE"]
    }
  ]
}
ii) Assign Permission to Role
URL: /api/roles/<role_id>/assign_permission/
Method: POST
Request Body:

{
  "permission_id": 3
}
Response (Success):

{
  "success": true,
  "message": "Permission assigned successfully."
}
Response (Error):

{
  "success": false,
  "message": "Permission does not exist."
}


## 3. Permission Management
i) List All Permissions
URL: /api/permissions/
Method: GET
Response:

{
  "success": true,
  "message": "Permission list retrieved successfully.",
  "data": [
    {
      "id": 1,
      "name": "API_ONE"
    },
    {
      "id": 2,
      "name": "API_TWO"
    }
  ]
}
ii) List Permissions for a Role
URL: /api/roles/<role_id>/permissions/
Method: GET

Copy code
{
  "success": true,
  "message": "Permissions for the role retrieved successfully.",
  "data": [
    "API_ONE",
    "API_TWO"
  ]
}

## 4. Access Validation
i) Validate Access
URL: /api/access/validate/
Method: POST
Request Body:
{
  "resource": "User",
  "action": "update"
}
Response (Access Granted):
{
  "success": true,
  "message": "Access granted."
}
Request (Invalid action):
{
  "resource": "User",
  "action": "delete"
}
Response:
{
  "success": false,
  "message": "Access denied."
}



## 5. Audit Logging
i) Retrieve Logs
URL: /api/audit-logs/

Method: GET

Query Parameters:

start_time: Start timestamp (optional)
end_time: End timestamp (optional)
Response:

{
  "success": true,
  "message": "Logs retrieved successfully.",
  "data": [
    {
      "user": "example_user",
      "resource": "API_ONE",
      "outcome": "Granted",
      "timestamp": "2024-12-16T12:00:00Z"
    },
    {
      "user": "admin_user",
      "resource": "API_THREE",
      "outcome": "Denied",
      "timestamp": "2024-12-16T12:10:00Z"
    }
  ]
}