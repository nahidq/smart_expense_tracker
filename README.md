# Smart Expense Tracker (Microservices)

A full-stack expense tracking application built using a microservices architecture.  
This project demonstrates backend service design, authentication, and frontend integration.

---

## 🚀 Features

- User registration and login (JWT authentication)
- Secure API endpoints
- Create, read, update, and delete expenses
- User-specific data isolation
- Frontend integration with React

---

## 🏗️ Architecture

This project is built using a **microservices architecture**:

### Backend
- **Auth Service**
  - Handles user registration and login
  - Issues JWT tokens

- **Expense Service**
  - Handles expense CRUD operations
  - Protected using JWT authentication

### Frontend
- React application (Vite)
- Communicates with backend APIs
- Handles authentication and expense management

---

## 🧰 Tech Stack

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT (python-jose)
- Poetry

### Frontend
- React
- Vite
- JavaScript (ES6)
---
## 📁 Project Structure
``` text
smart-expense-tracker/
│
├── backend/
│ ├── auth_service/ # Handles authentication (JWT)
│ └── expense_service/ # Handles expense CRUD operations
│
├── frontend/ # React application (UI)
│
├── pyproject.toml # Python dependencies (Poetry)
├── poetry.lock
└── README.md
```
## ⚙️ Getting Started

### 1. Clone the repository

```commandline
git clone https://github.com/nahidq/smart-expense-tracker.git
cd smart-expense-tracker 
```
2. Backend setup (Poetry)
```
cd backend/auth_service
poetry install
poetry run uvicorn app.main:app --reload --port 8000
cd ../expense_service
poetry install
poetry run uvicorn app.main:app --reload --port 8001
```
3. Frontend setup
```commandline
cd frontend
npm install
npm run dev
```

## 🔐 Authentication Flow

1. User logs in via Auth Service
2. Auth Service returns JWT token
3. Frontend stores token
4. Token is sent in Authorization header
5. Expense Service validates token


## 📌 Status

🚧 This project is actively being developed.

## 🔮 Planned Improvements
* Docker & Docker Compose
* API Gateway
* Refresh tokens
* Pagination and filtering
* CI/CD pipeline