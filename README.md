# 🏠 Spaces for Rent - Backend API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

**RESTful API backend for the Spaces for Rent platform**

[Frontend Repo](https://github.com/binabdimalik/space-for-rent--frontend) · [API Docs](#-api-endpoints) · [Report Bug](https://github.com/binabdimalik/space-for-rent-backend/issues)

</div>

---

## 📌 Overview

This is the **Flask-based REST API** backend for the Spaces for Rent platform. It handles all data operations for spaces, users, bookings, and reviews. The API uses **SQLAlchemy ORM** for database operations and **Flask-CORS** for frontend integration.

### ✨ Key Features

| Feature                   | Description                             |
| ------------------------- | --------------------------------------- |
| 🏢 **Spaces Management**  | Full CRUD operations for rental spaces  |
| 👤 **User Management**    | User registration and profile handling  |
| 📅 **Bookings System**    | Create, update, and manage reservations |
| ⭐ **Reviews**            | Rating and review system for spaces     |
| 💳 **Payment Simulation** | Invoice generation for bookings         |

---

## 🛠️ Tech Stack

| Category       | Technology                       |
| -------------- | -------------------------------- |
| **Framework**  | Flask 2.x                        |
| **ORM**        | SQLAlchemy                       |
| **Database**   | SQLite (dev) / PostgreSQL (prod) |
| **Migrations** | Flask-Migrate (Alembic)          |
| **CORS**       | Flask-CORS                       |
| **Testing**    | Postman                          |

---

## 📂 Project Structure

```
space-for-rent-backend/
├── app.py                # Main application with models & routes
├── models/
│   ├── __init__.py       # Package initialization
│   └── space.py          # Space model (alternative)
├── migrations/           # Database migration files
├── instance/
│   └── app.db            # SQLite database file
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

---

## 🚀 Running the Whole Project

### Prerequisites

- **Python 3.9+** installed
- **Node.js 16+** installed (for frontend)
- **Git** installed

---

### Step 1: Clone Both Repositories

```bash
# Create project folder
mkdir spaces-for-rent && cd spaces-for-rent

# Clone backend
git clone https://github.com/binabdimalik/space-for-rent-backend.git

# Clone frontend
git clone https://github.com/binabdimalik/space-for-rent--frontend.git
```

---

### Step 2: Setup & Run Backend

```bash
# Navigate to backend folder
cd space-for-rent-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
python app.py
```

✅ **Backend will run on:** `http://localhost:5555`

---

### Step 3: Setup & Run Frontend

```bash
# Open a NEW terminal window
# Navigate to frontend folder
cd space-for-rent--frontend

# Install dependencies
npm install

# Run the frontend server
npm start
```

✅ **Frontend will run on:** `http://localhost:3000`

---

### Step 4: Access the Application

| Service                 | URL                         |
| ----------------------- | --------------------------- |
| 🌐 **Frontend (React)** | http://localhost:3000       |
| 🔌 **Backend API**      | http://localhost:5555       |
| 👤 **Admin Panel**      | http://localhost:3000/admin |

---

## 🔐 Demo Credentials

| Role            | Email                          | Password      |
| --------------- | ------------------------------ | ------------- |
| **Super Admin** | `superadmin@spacesforrent.com` | `admin123`    |
| **Client**      | `john@example.com`             | `password123` |

---

## 📡 API Endpoints

### Spaces

| Method   | Endpoint          | Description      |
| -------- | ----------------- | ---------------- |
| `GET`    | `/api/spaces`     | Get all spaces   |
| `GET`    | `/api/spaces/:id` | Get single space |
| `POST`   | `/api/spaces`     | Create new space |
| `PUT`    | `/api/spaces/:id` | Update space     |
| `DELETE` | `/api/spaces/:id` | Delete space     |

### Users

| Method | Endpoint     | Description     |
| ------ | ------------ | --------------- |
| `GET`  | `/api/users` | Get all users   |
| `POST` | `/api/users` | Create new user |

### Bookings

| Method | Endpoint                | Description        |
| ------ | ----------------------- | ------------------ |
| `GET`  | `/api/bookings`         | Get all bookings   |
| `GET`  | `/api/bookings/:id`     | Get single booking |
| `POST` | `/api/bookings`         | Create booking     |
| `PUT`  | `/api/bookings/:id`     | Update booking     |
| `POST` | `/api/bookings/:id/pay` | Process payment    |

### Reviews

| Method | Endpoint       | Description     |
| ------ | -------------- | --------------- |
| `GET`  | `/api/reviews` | Get all reviews |
| `POST` | `/api/reviews` | Create review   |

---

## 🔌 API Testing with Postman

1. Import the API endpoints into Postman
2. Set base URL: `http://localhost:5555`
3. Set headers:
   ```json
   {
     "Content-Type": "application/json"
   }
   ```
4. Test each endpoint

### Example: Create a Space

```bash
POST http://localhost:5555/api/spaces
Content-Type: application/json

{
  "title": "Modern Office Space",
  "description": "Great for meetings",
  "price_per_night": 150.00,
  "location": "Nairobi, Kenya",
  "capacity": 10,
  "amenities": "WiFi, Projector, AC"
}
```

---

## � Database Models

| Model       | Description                                       |
| ----------- | ------------------------------------------------- |
| **User**    | User accounts with roles (user/admin/super_admin) |
| **Space**   | Rental space listings                             |
| **Booking** | Reservations linking users to spaces              |
| **Review**  | User reviews and ratings for spaces               |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feat/your-name/feature`)
3. Commit your changes (`git commit -m 'feat: add new feature'`)
4. Push to the branch (`git push origin feat/your-name/feature`)
5. Open a Pull Request

---

## 👤 Authors

- **Abdimalik Kulow**
- **Peter Emu**
- **Elly Owuor**
- **Yvonne Kajuju**
- **Ephraihim Anyanje**

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

Made with ❤️ by the Spaces for Rent Team

</div>
