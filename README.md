# School Feeding Management System - Backend

A Django REST Framework based backend system for managing school feeding operations, food delivery tracking, challan management, reporting, and dashboard analytics.

---

## Features

### Authentication

* JWT Authentication
* Login API
* Role-based access control
* Admin users
* Field Staff users

### School Management

* Create School
* Update School
* Delete School
* School List
* EMIS Code Management
* Student Count Management

### Holiday Management

* Government Holidays
* Weekly Holidays
* Monthly Feeding Calendar Generation

### Ration Settings

* Configure Food Types
* Bun Distribution Settings
* Egg Distribution Settings
* Banana Distribution Settings

### Delivery Management

* Daily Food Delivery Entry
* Bun Delivery Tracking
* Egg Delivery Tracking
* Banana Delivery Tracking
* Challan Number Management
* Challan Date Management
* Challan Image Upload

### Dashboard

#### Admin Dashboard

* Total Students
* Total Food Delivered
* Total Shortfall
* Total Bun Delivered
* Total Egg Delivered
* Total Banana Delivered
* School-wise Delivery Summary
* School-wise Shortfall Report

#### Staff Dashboard

* Today's Deliveries
* Total Schools Covered
* Total Bun Delivered
* Total Egg Delivered
* Total Banana Delivered
* Delivery History

### Reports

#### Form-04

Monthly Food Receiving Report

#### Form-07

Food Supply Summary Report

#### Form-10

Invoice Report

#### Form-12

School Stock Register

#### Form-13

Distribution Register

---

## Technology Stack

### Backend

* Python 3.11+
* Django 5+
* Django REST Framework
* Simple JWT

### Database

* SQLite (Development)
* MySQL (Production)

### Storage

* Local Media Storage
* Challan Image Uploads

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-repository/backend.git

cd backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### Install Requirements

```bash
pip install -r requirements.txt
```

### Environment Variables

Create `.env`

```env
SECRET_KEY=your_secret_key

DEBUG=True

ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_NAME=db.sqlite3
```

### Run Migration

```bash
python manage.py makemigrations

python manage.py migrate
```

### Create Super User

```bash
python manage.py createsuperuser
```

### Run Server

```bash
python manage.py runserver
```

Backend:

```text
http://127.0.0.1:8000
```

---

## API Endpoints

### Authentication

| Method | Endpoint              | Description   |
| ------ | --------------------- | ------------- |
| POST   | `/api/token/`         | Login         |
| POST   | `/api/token/refresh/` | Refresh Token |

### Dashboard

| Method | Endpoint                |
| ------ | ----------------------- |
| GET    | `/api/dashboard/`       |
| GET    | `/api/staff-dashboard/` |

### Schools

| Method | Endpoint             |
| ------ | --------------------- |
| GET    | `/api/schools/`      |
| POST   | `/api/schools/`      |
| PUT    | `/api/schools/{id}/` |
| DELETE | `/api/schools/{id}/` |

### Holidays

| Method | Endpoint         |
| ------ | ---------------- |
| GET    | `/api/holidays/` |
| POST   | `/api/holidays/` |

### Deliveries

| Method | Endpoint                |
| ------ | ------------------------ |
| GET    | `/api/deliveries/`      |
| POST   | `/api/deliveries/`      |
| PUT    | `/api/deliveries/{id}/` |
| DELETE | `/api/deliveries/{id}/` |

### Reports

| Method | Endpoint                                    |
| ------ | -------------------------------------------- |
| GET    | `/api/reports/form4/?month=9&year=2026`     |
| GET    | `/api/reports/form07/?month=9&year=2026`    |
| GET    | `/api/reports/form10/?month=9&year=2026`    |
| GET    | `/api/reports/form12-13/?month=9&year=2026` |

---

## Media Files

Uploaded challan images are stored in:

```text
media/

├── chalans/
│   ├── bun/
│   ├── egg/
│   └── banana/
```

---

## Project Structure

```text
backend/

├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── services.py
│   ├── urls.py
│
├── media/
│
├── project/
│   ├── settings.py
│   ├── urls.py
│
├── manage.py
│
└── requirements.txt
```

---

## Default User Roles

### ADMIN

Can:

* Manage Schools
* Manage Holidays
* Manage Deliveries
* View Reports
* View Dashboard

### FIELD

Can:

* Create Delivery Records
* Upload Challans
* View Own Dashboard
* View Reports

---

## Author

**Munazer Montasir Akash**

* MSc Student, CSE, BUET
* Adjunct Faculty, IIUC
* Software Engineer & AI Researcher

---

## License

This project is developed for the **School Feeding Program Management System** and intended for organizational use.