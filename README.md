# Smart Expense Tracker

A full-stack expense tracking application built with **FastAPI, React, PostgreSQL, and a microservices architecture**.

The project includes separate authentication and expense services, JWT-based authorization, automated backend and frontend validation, Docker containerization, and CI/CD workflows with GitHub Actions.

## Features

* User registration and login with JWT authentication
* Secure REST API endpoints
* Create, read, update, and delete expenses
* User-specific data isolation
* React frontend for authentication and expense management
* Separate authentication and expense microservices
* PostgreSQL persistence with SQLAlchemy
* Automated unit and integration testing
* Docker and Docker Compose support
* CI/CD automation with GitHub Actions

## Architecture

The application separates authentication and expense management into independent backend services.

### Auth Service

* Handles user registration and login
* Stores user data in PostgreSQL
* Issues JWT access tokens
* Exposes authentication REST API endpoints

### Expense Service

* Handles expense CRUD operations
* Stores expense data in a separate PostgreSQL database
* Validates JWT tokens
* Restricts expense data to the authenticated user

### Frontend

* Built with React and Vite
* Communicates with the backend through REST APIs
* Handles authentication and expense-management workflows
* Sends JWT tokens with authenticated requests

## Tech Stack

### Backend

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* JWT / python-jose
* Poetry
* pytest

### Frontend

* React
* Vite
* JavaScript
* ESLint

### DevOps & CI/CD

* Docker
* Docker Compose
* GitHub Actions
* GitHub Container Registry (GHCR)
* PostgreSQL 16 containers

## Project Structure

```text
smart_expense_tracker/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yaml
│
├── backend/
│   ├── auth_service/
│   │   ├── app/
│   │   ├── tests/
│   │   └── Dockerfile
│   │
│   └── expense_service/
│       ├── app/
│       ├── tests/
│       └── Dockerfile
│
├── frontend/
│   └── src/
│
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/nahidq/smart_expense_tracker.git
cd smart_expense_tracker
```

### 2. Run the backend with Docker Compose

Docker Compose starts:

* Auth Service
* Expense Service
* PostgreSQL database for authentication
* PostgreSQL database for expenses

```bash
docker compose up --build
```

The backend services are available at:

```text
Auth Service:    http://localhost:8000
Expense Service: http://localhost:8001
```

FastAPI automatically exposes interactive API documentation:

```text
Auth API:    http://localhost:8000/docs
Expense API: http://localhost:8001/docs
```

### 3. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

## Authentication Flow

1. A user registers or logs in through the Auth Service.
2. The Auth Service validates the credentials and returns a JWT token.
3. The frontend stores the token.
4. Authenticated requests send the token in the `Authorization` header.
5. The Expense Service validates the token before processing requests.
6. Expense operations are restricted to data belonging to the authenticated user.

## Testing

Backend tests are implemented with **pytest** for both services.

Run the authentication-service tests:

```bash
cd backend/auth_service
poetry run pytest tests
```

Run the expense-service tests:

```bash
cd backend/expense_service
poetry run pytest tests
```

Frontend quality checks include linting and a production build:

```bash
cd frontend
npm run lint
npm run build
```

## CI/CD

The project uses **GitHub Actions** for continuous integration and container-image delivery.

### Continuous Integration

The CI workflow runs automatically on pushes and pull requests targeting `main`.

It:

* Creates a PostgreSQL 16 test environment
* Installs Python dependencies with Poetry
* Runs pytest for the Auth Service
* Runs pytest for the Expense Service
* Installs frontend dependencies
* Runs frontend lint checks
* Builds the React application

The backend services are tested independently through a GitHub Actions matrix configuration.

### Continuous Delivery

The CD workflow runs on pushes to `main`.

It:

* Builds Docker images for the Auth Service and Expense Service
* Uses Docker Buildx
* Tags container images with the commit SHA and `latest`
* Authenticates with GitHub Container Registry
* Publishes the service images to GHCR

This provides an automated build, test, and container-publishing workflow for changes merged into the main branch.

## Containerization

The backend is containerized using separate Dockerfiles for the authentication and expense services.

`docker-compose.yml` orchestrates:

* Auth Service
* Expense Service
* Users PostgreSQL database
* Expenses PostgreSQL database

Docker Compose provides a reproducible local environment for running the backend services and databases together.

## Status

The core full-stack application is implemented and includes:

* Authentication and authorization
* Expense CRUD operations
* User-level data isolation
* React frontend integration
* PostgreSQL persistence
* Automated testing
* Docker containerization
* Docker Compose orchestration
* GitHub Actions CI
* Automated Docker image publishing through GitHub Actions

The project remains open for additional features and infrastructure improvements.

## Planned Improvements

* API Gateway
* Refresh-token support
* Pagination and filtering
* Additional frontend test coverage
* Application monitoring and observability
* Deployment to a hosted environment
