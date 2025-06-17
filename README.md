# Discussions API

A minimal Reddit-style discussion API built with Django and Django REST Framework.

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- pip
- Git
- [PostgreSQL](https://www.postgresql.org/) or [MySQL](https://www.mysql.com/) for production.
  (SQLite used locally by default)

### 📥 Installation


Clone the repository:
```
% git clone https://github.com/Ezmeer/discussions-api.git
% cd discussions-api
```



Create and activate a virtual environment:
```
% python3 -m venv .venv
% source .venv/bin/activate
```

Install dependencies:
```
% pip install -r requirements.txt
```


⚙️ Configuration
By default, the project uses SQLite for local development.

To use Postgres or MySQL in production, 
set the following environment variables (e.g., in a .env file or directly in the environment):

```
DB_ENGINE=django.db.backends.postgresql  # or django.db.backends.mysql
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432  # or 3306 for MySQL
```

Ensure your discussions/settings.py uses os.environ.get to pull these settings.


🛠️ Database Setup
Run the following commands to initialize the database:

```
% python manage.py makemigrations
% python manage.py migrate
```

You can optionally create a superuser for admin access:

```
% python manage.py createsuperuser
```


🧪 Running Tests
```
% pytest
```

Ensure the pytest and pytest-django packages are installed (included in requirements.txt).


▶️ Starting the Development Server
```
% python manage.py runserver
```
API is accessible at: http://127.0.0.1:8000/api/v1/


🧩 API Overview

🔹 Discussions:
```
GET /api/v1/discussions/ – List all discussions
GET /api/v1/discussions/{id}/ – Get a specific discussion

POST /api/v1/discussions/ – Create a new discussion
POST /api/v1/discussions/{id}/delete/ – Delete (with creator ID)
POST /api/v1/discussions/{id}/update/ – Update title
```

🔹 Comments:
```
GET /api/v1/comments/?discussion_id={id} – Top-level comments
GET /api/v1/comments/{id}/replies/ – Get replies to a comment

POST /api/v1/comments/ – Add a comment (or reply)
POST /api/v1/comments/{id}/delete/ – Delete comment
POST /api/v1/comments/{id}/update/ – Update comment
```


🧾 Production Notes

Ensure your database (Postgres or MySQL) is created and accessible.
Set DEBUG=False and configure ALLOWED_HOSTS in settings.py.


📂 Project Structure
```
discussions-api/
├── discussions/         # Django app
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── tests/
├── discussions_api/     # Project settings
│   └── settings.py
├── requirements.txt
├── manage.py
└── README.md
```