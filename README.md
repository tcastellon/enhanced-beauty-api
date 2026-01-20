# Enhanced Beauty App - Backend API

A Django REST Framework API backend for the Enhanced Beauty App. This API provides user authentication, client management, visit tracking, and service management endpoints for service-based businesses.

## Features

- **Token-Based Authentication**: Secure user registration and login with token authentication
- **Client Management**: Full CRUD operations for client profiles with user isolation
- **Visit Tracking**: Record and manage client visits with associated services
- **User Data Isolation**: Each user can only access their own clients and visits
- **CORS Support**: Configured for frontend development servers

## Tech Stack

- **Django 5.2** - Python web framework
- **Django REST Framework** - RESTful API toolkit
- **SQLite** - Database (development)
- **django-cors-headers** - Cross-Origin Resource Sharing support
- **python-decouple** - Environment variable management

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.10 or higher
- pipenv (recommended) or pip
- Git

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/tcastellon/enhanced-beauty-app.git
cd enhanced-beauty-app/enhanced_beauty_backend
```

### 2. Set Up Virtual Environment

Using pipenv (recommended):

```bash
pipenv install
pipenv shell
```

Or using pip:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install django djangorestframework django-cors-headers python-decouple
```

### 3. Run Database Migrations

```bash
python manage.py migrate
```

### 4. Create a Superuser (Optional)

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

### 5. Start the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Register a new user |
| POST | `/api/login/` | Login and receive auth token |

### Clients (Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/clients/` | List all clients for authenticated user |
| POST | `/api/clients/` | Create a new client |
| GET | `/api/clients/{id}/` | Retrieve a specific client |
| PUT | `/api/clients/{id}/` | Update a client |
| DELETE | `/api/clients/{id}/` | Delete a client |

### Visits (Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/visits/` | List all visits for authenticated user |
| GET | `/api/visits/?client_id={id}` | List visits for a specific client |
| POST | `/api/visits/` | Create a new visit |
| GET | `/api/visits/{id}/` | Retrieve a specific visit |
| PUT | `/api/visits/{id}/` | Update a visit |
| DELETE | `/api/visits/{id}/` | Delete a visit |

### Services (Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/services/` | List all services |
| POST | `/api/services/` | Create a new service |
| GET | `/api/services/{id}/` | Retrieve a specific service |
| PUT | `/api/services/{id}/` | Update a service |
| DELETE | `/api/services/{id}/` | Delete a service |

### Visit Services (Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/visitservices/` | List all visit services |
| GET | `/api/visitservices/?visit_id={id}` | List services for a specific visit |
| POST | `/api/visitservices/` | Add a service to a visit |
| GET | `/api/visitservices/{id}/` | Retrieve a specific visit service |
| PUT | `/api/visitservices/{id}/` | Update a visit service |
| DELETE | `/api/visitservices/{id}/` | Remove a service from a visit |

## Authentication

The API uses token-based authentication. After registering or logging in, include the token in the `Authorization` header:

```
Authorization: Token your_token_here
```

### Register Request Example

```json
POST /api/register/
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword",
    "first_name": "John",
    "last_name": "Doe"
}
```

### Login Request Example

```json
POST /api/login/
{
    "username": "johndoe",
    "password": "securepassword"
}
```

### Login Response Example

```json
{
    "token": "your_auth_token",
    "user": {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe"
    }
}
```

## Project Structure

```
enhanced_beauty_backend/
├── backend/                          # Django project configuration
│   ├── __init__.py
│   ├── settings.py                   # Project settings
│   ├── urls.py                       # Root URL configuration
│   ├── asgi.py                       # ASGI config
│   └── wsgi.py                       # WSGI config
├── enhanced_beauty_api/              # Main Django app
│   ├── migrations/                   # Database migrations
│   ├── __init__.py
│   ├── admin.py                      # Admin panel configuration
│   ├── apps.py                       # App configuration
│   ├── models.py                     # Database models
│   ├── serializers.py                # DRF serializers
│   ├── views.py                      # API views and viewsets
│   └── tests.py                      # Unit tests
├── manage.py                         # Django CLI utility
├── Pipfile                           # Pipenv dependencies
├── Pipfile.lock                      # Locked dependencies
├── db.sqlite3                        # SQLite database
└── README.md                         # This file
```

## Data Models

### Client

| Field | Type | Description |
|-------|------|-------------|
| name | CharField | Client's full name |
| street_address | CharField | Street address |
| city | CharField | City |
| state | CharField | State (2 characters) |
| zip_code | CharField | ZIP code (5 characters) |
| phone_number | CharField | Phone number |
| email | EmailField | Email address |
| date_of_birth | DateField | Date of birth |
| created_by_user | ForeignKey | User who created the client |
| created_at | DateTimeField | Record creation timestamp |
| updated_at | DateTimeField | Last update timestamp |

### Visit

| Field | Type | Description |
|-------|------|-------------|
| client | ForeignKey | Associated client |
| created_by_user | ForeignKey | User who created the visit |
| note_content | TextField | Visit notes (optional) |
| visit_date | DateTimeField | Date and time of visit |
| created_at | DateTimeField | Record creation timestamp |
| updated_at | DateTimeField | Last update timestamp |

### Service

| Field | Type | Description |
|-------|------|-------------|
| name | CharField | Service name |

### VisitService

| Field | Type | Description |
|-------|------|-------------|
| visit | ForeignKey | Associated visit |
| service | ForeignKey | Associated service |
| created_at | DateTimeField | Record creation timestamp |

## Configuration

### CORS Settings

The API is configured to accept requests from the following origins:

- `http://localhost:3000` (React development)
- `http://localhost:5173` (Vite development)

To add additional origins, update `CORS_ALLOWED_ORIGINS` in `backend/settings.py`.

### Timezone

The API is configured for `America/Chicago` timezone. Update `TIME_ZONE` in `backend/settings.py` if needed.

## Development Status

This application is currently in development and is not ready for production deployment. For production use:

- Set `DEBUG = False`
- Use environment variables for `SECRET_KEY`
- Configure a production database (PostgreSQL recommended)
- Set appropriate `ALLOWED_HOSTS`
- Configure HTTPS

## Available Commands

```bash
# Run development server
python manage.py runserver

# Apply database migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations

# Create superuser for admin access
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Run tests
python manage.py test
```

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` using superuser credentials. The admin panel provides direct database management for:

- Users
- Clients
- Visits
- Services
- Visit Services

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is private and not currently licensed for public use.

## Related Repositories

- **Frontend Application**: [enhanced-beauty-app (frontend)](https://github.com/tcastellon/enhanced-beauty-client)

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.
