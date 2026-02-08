# Project Name

## 📌 Overview

This project is a **Flask-based REST API** designed to serve as the backend for a web application. It uses **Flask**, **SQLAlchemy**, and **Flask-Migrate**, and is built to be easily connected to a frontend (e.g. React) via **CORS**.

The API follows standard REST principles and supports CRUD operations, authentication-ready structure, and database migrations.

---

## 🛠 Tech Stack

* **Backend:** Flask (Python)
* **Database:** SQLite / PostgreSQL (via SQLAlchemy)
* **ORM:** SQLAlchemy
* **Migrations:** Flask-Migrate (Alembic)
* **API Testing:** Postman
* **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
project-root/
│
├── app.py                # Main application entry point
├── models.py             # Database models
├── routes/               # API route definitions
├── migrations/           # Database migration files
├── instance/             # Instance-specific config (DB file)
├── requirements.txt      # Python dependencies
├── alembic.ini           # Migration configuration
└── README.md             # Project documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone <repository-url>
cd project-root
```

---

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Environment variables (if applicable)

Create a `.env` file and add:

```
FLASK_APP=app.py
FLASK_ENV=development
```

---

### 5️⃣ Database setup

If migrations already exist:

```bash
flask db upgrade
```

If starting fresh:

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

### 6️⃣ Run the application

```bash
flask run
```

The API will be available at:

```
http://127.0.0.1:5000
```

---

## 🔌 API Testing

Use **Postman** or similar tools:

* Base URL: `http://127.0.0.1:5000`
* Test GET, POST, PUT, DELETE endpoints
* Ensure headers include:

```json
{
  "Content-Type": "application/json"
}
```

---

## 🔁 Git Workflow

* `main` → stable production-ready code
* feature branches → active development

To update your branch with `main`:

```bash
git fetch origin
git merge origin/main
```

---

## 🚀 Future Improvements

* Authentication & authorization
* Input validation
* Unit & integration tests
* Deployment (Docker / Render / Railway)

---

## 👤 Author

**Abdimalik Kulow**
**Peter Emu**
**Elly Owuor**
**Yvonne Kajuju**
**Ephraihim Anyanje**
	


---

## 📄 License

This project is licensed under the MIT License.
