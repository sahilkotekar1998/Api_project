# Api_project


---

# FastAPI User Registration Project

This project demonstrates user registration functionality using FastAPI with two different configurations: one with PostgreSQL and MongoDB and another with only PostgreSQL.

## Features

- User Registration
- Email and Phone Uniqueness Check
- Profile Picture Storage
- Secure Password Hashing
- User Details Retrieval

## Requirements

- Python 3.7
- PostgreSQL
- MongoDB

## Installation

1. **Clone the repository:**

   
   git clone https://github.com/sahilkotekar1998/Api_project.git
   cd your-repo
   

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv myenv
   myenv\Scripts\activate    
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the PostgreSQL database:**

   - Make sure PostgreSQL is installed and running.
   - Create a new PostgreSQL database:

     ```sh
     psql -U postgres
     CREATE DATABASE user_db;
     \q
     ```

5. **Configure MongoDB:**

   - Make sure MongoDB is installed and running.
   - Update the `MONGO_URL` and `MONGO_DB_NAME` in the code to match your MongoDB configuration.

## Running the Application

1. **Run the FastAPI application:**

   ```sh
   uvicorn main:app --reload
   ```

2. **Open your browser and navigate to:**

   ```sh
   http://127.0.0.1:8000
   ```

## Project Structure

```
.
├── main.py                  # Main application file
├── models.py                # SQLAlchemy models
├── database.py              # Database configuration
├── templates/
│   ├── register.html        # Registration form template
│   └── login.html           # Login form template
├── requirements.txt         # Python packages required
└── .gitignore               # Git ignore file
```


## Usage

### Program 1: User Registration with PostgreSQL and MongoDB

#### Registration Fields:
- Full Name
- Email
- Password
- Phone
- Profile Picture

#### Storage:
- PostgreSQL: First Name, Password, Email, Phone
- MongoDB: Profile Picture

#### Endpoint:
- **POST /register/**: Registers a new user. Checks if the email already exists.
- **GET /register/**: Displays the registration form.
- **POST /login**: Logs in a user. Checks if the email and password are correct and retrieves the profile picture from MongoDB.
- **GET /login**: Displays the login form.

### Program 2: User Registration with PostgreSQL Only

#### Registration Fields:
- Full Name
- Email
- Password
- Phone
- Profile Picture

#### Storage:
- PostgreSQL: First Name, Password, Email, Phone, Profile Picture

#### Tables:
- **Users**: Stores First Name, Password, Email, Phone
- **Profile**: Stores Profile Picture

#### Endpoint:
- **POST /register/**: Registers a new user. Checks if the email or phone already exists.
- **GET /register/**: Displays the registration form.
- **POST /login**: Logs in a user. Checks if the email and password are correct.
- **GET /login**: Displays the login form.
- **GET /user/{user_id}**: Retrieves registered user details.

