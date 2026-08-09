# 🍔 QuickBite

**QuickBite** is a full-stack food ordering web application built with **Django and Django REST Framework**.

It provides a simple ordering experience for customers while giving staff the ability to manage food items and incoming orders. The project also includes a REST API with JWT authentication, filtering, searching, pagination, and API documentation.

## ✨ Features

### 👤 Customer

* Register and log in
* Browse available food items
* View food item details
* Add and remove items from cart
* Place orders
* View order history
* Manage profile

### 👨‍💼 Staff

* Add food items
* Update and delete food items
* Manage item availability
* View received orders
* Mark orders as completed
* Staff-only access to management operations

### 🔌 API

* RESTful APIs built with Django REST Framework
* JWT authentication
* Item and Order ViewSets
* Search and filtering
* Ordering and pagination
* Serializer-based validation
* Swagger / ReDoc API documentation
* API throttling

### 📱 UI

* Responsive interface
* Tailwind CSS
* HTMX for dynamic interactions
* Food images and detailed item pages
* Paginated menu

## 🛠️ Tech Stack

| Category          | Technology                |
| ----------------- | ------------------------- |
| Backend           | Python, Django            |
| API               | Django REST Framework     |
| Database          | PostgreSQL                |
| Authentication    | Django Auth, JWT          |
| Frontend          | HTML, Tailwind CSS, HTMX  |
| API Documentation | drf-spectacular / OpenAPI |
| Filtering         | django-filter             |
| Image Handling    | Pillow                    |

## 🏗️ Project Structure

```text
QuickBite/
├── Food/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── forms.py
│   ├── urls.py
│   ├── templates/
│   └── static/
│
├── users/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── templates/
│
├── QuickBite/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── fixtures/
├── pictures/
├── manage.py
└── schema.yml
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/vaibhavkumarjak7/QuickBite.git
cd QuickBite
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install django djangorestframework djangorestframework-simplejwt django-filter drf-spectacular psycopg2-binary pillow python-dotenv
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## 📚 API Documentation

Once the server is running:

**Swagger UI**

```text
http://127.0.0.1:8000/api/schema/swagger-ui/
```

**ReDoc**

```text
http://127.0.0.1:8000/api/schema/redoc/
```

**OpenAPI Schema**

```text
http://127.0.0.1:8000/api/schema/
```

## 🔗 API Endpoints

### Items

```text
GET     /food/api/items/
POST    /food/api/items/
GET     /food/api/items/{id}/
PUT     /food/api/items/{id}/
PATCH   /food/api/items/{id}/
DELETE  /food/api/items/{id}/
```

### Orders

```text
GET     /food/api/orders/
POST    /food/api/orders/
GET     /food/api/orders/{id}/
PUT     /food/api/orders/{id}/
PATCH   /food/api/orders/{id}/
DELETE  /food/api/orders/{id}/
```

### Authentication

```text
POST /food/api/token/
POST /food/api/token/refresh/
```

## 🔐 Security & Permissions

QuickBite uses different permissions for customers and staff.

* Customers can browse items and manage their own orders.
* Staff members can manage food items and received orders.
* JWT authentication is used for API authentication.
* API requests are throttled to help prevent excessive usage.
* Serializer validation is used for API input validation.
* Sensitive configuration is managed through environment variables.

## 🎯 What I Learned

Building QuickBite helped me strengthen my understanding of:

* Full-stack Django development
* REST API design
* JWT authentication
* Role-based permissions
* Django ORM and database relationships
* CRUD operations
* API filtering, searching, and pagination
* Responsive frontend development
* API documentation with OpenAPI
* Building a project with both server-rendered pages and REST APIs

## 📸 Demo

A complete demo of the application is available in the project presentation/video.

## 🔗 Repository

[GitHub – QuickBite](https://github.com/vaibhavkumarjak7/QuickBite)

---

### Built with Python 🐍 & Django ❤️
