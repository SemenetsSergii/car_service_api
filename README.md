# Car Service API

## Description
Car Service API is a RESTful API designed for managing users, cars, mechanics, services, and appointments in a car service center. The API allows creating, viewing, updating, and deleting records for clients, cars, mechanics, services, and appointments.

---

## Features

- **Users**:
  - Add new users
  - User authentication
  - View profiles and list users
  - Update user data

- **Cars**:
  - Add cars
  - View the list of cars and their details
  - Update car information
  - Delete cars

- **Services**:
  - Add services
  - View the list of services
  - Update service information
  - Delete services

- **Mechanics**:
  - Add mechanics
  - View the list of mechanics
  - Update mechanic information
  - Delete mechanics

- **Appointments**:
  - Create appointments
  - View appointments
  - Update appointment status
  - Delete appointments

---

## Tech Stack

- **Python**: Core programming language
- **FastAPI**: Framework for building APIs
- **SQLAlchemy**: ORM for database interactions
- **MySQL**: Database
- **Alembic**: Tool for database migrations
- **Pydantic**: For data validation and schema creation
- **Uvicorn**: ASGI server to run FastAPI
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration

---

## Requirements

- Python 3.10+
- MySQL 8+
- Python Virtual Environment (`venv`)
- Docker and Docker Compose (for containerized setup)

---

## Installation and Setup

### Local Environment

```bash
# Clone the repository
git clone https://github.com/SemenetsSergii/car_service_api

# Navigate to the project directory
cd car_service_api

# Create a virtual environment
python -m venv venv
source venv/bin/activate # For Linux/MacOS
venv\Scripts\activate  # For Windows

# Install dependencies
pip install -r requirements.txt

# Set up .env file
cp .env.sample .env
# Update the .env file with your configuration

# Initialize the database
alembic upgrade head

# Run the server
uvicorn main:app --reload
# The API will be available at: http://127.0.0.1:8000
```

### Docker Setup

```bash
# Ensure Docker and Docker Compose are installed

# Build and start the containers
docker-compose up --build

# The API will be available at: http://localhost:8000
```

---

## Load Test Data

```bash
# Create a JSON file with test data (example in `example_data.json`)

# Run the script to load data
python load_data.py
```

For Docker setup, mount the `example_data.json` file in the container or ensure it’s included in the image build.

---

## Environment Variables

The application requires the following environment variables. Use the `.env` file to configure them:

### Database
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host (e.g., `mysql_db` for Docker, `localhost` for local setup)
- `DB_PORT`: Database port (default: `3306`)
- `DB_NAME`: Name of the database

### Email Notifications
- `SMTP_SERVER`: Your SMTP server address (e.g., `smtp.gmail.com`)
- `SMTP_PORT`: SMTP server port (e.g., `587`)
- `EMAIL_USERNAME`: Email address used to send notifications
- `EMAIL_PASSWORD`: Password for the email account

### Application Secrets
- `SECRET_KEY`: Secret key for JWT authentication
- `ALGORITHM`: Algorithm for JWT (e.g., `HS256`)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT expiration time in minutes

---

## Example Requests

### Users:

```http
# Create a new user
POST /users/
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "password": "SecurePassword123",
    "role": "CUSTOMER"
}

# View all users
GET /users/
```

### Cars:

```http
# Add a car
POST /cars/
{
    "user_id": 1,
    "brand": "Toyota",
    "model": "Corolla",
    "year": 2015,
    "plate_number": "AA1234BB",
    "vin": "JTDBE30KX03012345"
}

# View all cars
GET /cars/
```

---

## Testing

```bash
# Install pytest
pip install pytest

# Run tests
pytest
```

---

## Author
- **Full Name**: Sergii Semenets
- **Email**: serheysemenets@gmail.com
- **Telegram**: [@SergiiSemenets](https://t.me/SergiiSemenets)

---


