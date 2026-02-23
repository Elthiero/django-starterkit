# Django Starter Kit 🚀

A robust, modern Django 6.0 starter template designed for rapid application development. It features a custom user model, an HTMX-powered dynamic UI, Bootstrap 5 styling, Alpine.js for lightweight state management, and asynchronous HTML email notifications.

## ✨ Key Features

* **Custom User Model:** Replaces Django's default username with an `email` based login. Includes built-in roles (`ADMIN`, `MANAGER`, `DEFAULT`).
* **Modern Frontend Stack:** * **Bootstrap 5** (`django_bootstrap5`) for responsive, clean UI components.
  * **HTMX** for SPA-like interactions (e.g., dynamic search, filtering, and pagination without full page reloads).
  * **Alpine.js** for lightweight client-side state management (e.g., sidebar toggles, unified delete modals).
  * **Chart.js (v4)** for beautiful, responsive dashboard visualizations.
* **Asynchronous Email Notifications:** Uses Python's `threading` module to send non-blocking, beautifully styled HTML emails for:
  * Account Registration (Welcome)
  * Account Activation Approvals
  * New Sign-In Security Alerts (via Django Signals)
  * Password Changes & Resets
* **Security & Configuration:** Environment variables managed via `python-decouple`, production-ready static file serving with `whitenoise`, and robust PostgreSQL integration.

---

## 🛠️ Tech Stack

| Technology | Purpose |
| :--- | :--- |
| **Django 6.0** | Core backend framework and ORM |
| **PostgreSQL** | Primary relational database |
| **Bootstrap 5** | CSS framework and responsive grid |
| **HTMX** | Dynamic DOM updates and AJAX requests |
| **Alpine.js** | Client-side UI state management |
| **Chart.js** | Data visualization (Dashboards) |

---

## ⚙️ Prerequisites

Before you begin, ensure you have the following installed on your machine:
  **Python 3.12+**

* **PostgreSQL** (version 15+ recommended)
* `pip` and `venv` (Python virtual environments)

---

## 🚀 Local Setup & Installation

### 1. Clone the Repository & Setup Environment

```bash
git clone https://github.com/Elthiero/django-starterkit.git
cd django-starterkit
python3 -m venv venv
source venv/bin/activate

```

### 2. Install Dependencies

Ensure your `requirements.txt` includes Django, psycopg2-binary, django-bootstrap5, django-htmx, python-decouple, and whitenoise.

```bash
pip install -r requirements.txt

```

### 3. PostgreSQL Database Setup (Ubuntu/Linux)

Open your PostgreSQL prompt and configure the database and user:

```bash
sudo -u postgres psql

```

```sql
CREATE DATABASE starter_db;
CREATE USER starter_user WITH PASSWORD 'your_secure_password';
ALTER ROLE starter_user SET client_encoding TO 'utf8';
ALTER ROLE starter_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE starter_user SET timezone TO 'UTC';
ALTER DATABASE starter_db OWNER TO starter_user;
GRANT ALL ON SCHEMA public TO starter_user;
\q

```

### 4. Environment Variables (`.env`)

Refer to `.env.example` file in the same directory as your `manage.py` file and configure your variables:

```env
SECRET_KEY=your-super-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
SITE_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)
SITE_NAME=Starter Kit

# PostgreSQL Database
DB_NAME=starter_db
DB_USER=starter_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (e.g., Gmail with App Password)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_16_character_app_password
DEFAULT_FROM_EMAIL=Starter Kit <your_email@gmail.com>

```

### 5. Apply Migrations

**Important:** Because this project uses a custom User model, you must migrate the `accounts` app *first* before migrating the rest of the project.

```bash
# 1. Create migrations for the custom User model
python manage.py makemigrations accounts

# 2. Create migrations for any other apps
python manage.py makemigrations

# 3. Apply all migrations to PostgreSQL
python manage.py migrate

```

### 6. Create Superuser & Run

Create an admin account to access the dashboard and user management areas:

```bash
python manage.py createsuperuser

```

Run the development server:

```bash
python manage.py runserver

```

Visit `http://127.0.0.1:8000/` in your browser.

---

## 📁 Key Project Structure

```text
├── accounts/                  # Main authentication & user management app
│   ├── models.py              # Custom User model & UserManager
│   ├── forms.py               # Bootstrap-injected ModelForms
│   ├── signals.py             # Login alerts and background tasks
│   ├── decorators.py          # Custom decorator to manage user access. ["ADMIN","MANAGER","DEFAULT"]
│   ├── utils.py               # Asynchronous email threading logic
│   └── views.py               # Profile, User Management, Auth views
├── templates/                 # Global templates
│   ├── base.html              # Main App Shell (Sidebar, Topbar, HTMX progress)
│   ├── public/                # Auth layouts (Login, Register)
│   ├── includes/              # Includes footer, siderbar, navbar, messages, and topbar
│   ├── accounts/              # User management UI & Partials
│   └── emails/                # HTML Email templates
├── static/                    # CSS, JS, and Images
│   ├── css/style.css          # Blue Professional Theme design tokens
│   ├── img/                   # For images like favicons and others
│   └── js/main.js             # Alpine.js & HTMX event listeners
├── main/                      # Handle public pages
└── config/                    # Core Django settings & Root URL routing

```

---

## ✉️ Asynchronous Emails

This project bypasses traditional synchronous email blocking to ensure lightning-fast page loads. Emails are fired via a custom `EmailThread` class inside `accounts/utils.py`. To switch to console output for local debugging without sending real emails, update `settings.py`:

```python

# Use this to print emails to the terminal
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

