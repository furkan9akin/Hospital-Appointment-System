# Hospital Appointment System

A web-based appointment management application built with **Python, Flask, and SQLite**.

The system provides a simple interface for managing patients, doctors, and appointments while demonstrating backend development, relational database design, CRUD operations, form processing, and API development.

This project was originally developed as a final project during the **Kodland Python Level 3** program and was later reorganized and improved as a software portfolio project.

---

## 🏥 Project Overview

The Hospital Appointment System was created to simulate the basic workflow of an appointment management application.

Users can:

- manage patient records
- manage doctor records
- schedule appointments
- update appointment status
- delete appointments
- view today's appointments
- view upcoming appointments
- monitor appointment statistics from a dashboard

The project focuses on backend application development and the interaction between a Flask web application and a relational SQLite database.

---

## ✨ Features

### Patient Management

- Add new patients
- Store contact information
- Store date of birth
- Store address information
- View patient records

### Doctor Management

- Add new doctors
- Store medical specialization
- Store phone and email information
- View doctor records

### Appointment Management

- Schedule appointments between patients and doctors
- Select appointment date and time
- Select appointment duration
- Add appointment notes
- Update appointment status
- Delete appointments

Supported appointment statuses include:

```text
scheduled
completed
cancelled
no-show
```

### Dashboard

The dashboard displays:

- total number of appointments
- today's appointments
- appointments during the current week
- scheduled appointment count
- upcoming appointments

### Status History

Appointment status changes are stored in a separate database table, allowing the application to maintain a history of appointment status updates.

### JSON API

The application includes simple API endpoints for retrieving appointment and dashboard data.

```text
GET /api/appointments/<YYYY-MM-DD>
GET /api/stats
```

---

## 🧱 Application Architecture

The project follows a simple Flask application structure:

```text
Browser
   │
   ▼
Flask Routes
   │
   ▼
Application Logic
   │
   ▼
AppointmentDB
   │
   ▼
SQLite Database
```

Flask handles HTTP requests and page rendering, while the `AppointmentDB` class manages database operations.

---

## 🗄️ Database Design

The application uses SQLite and contains four main tables.

### Patients

Stores patient information such as:

- name
- phone
- email
- date of birth
- address

### Doctors

Stores doctor information such as:

- name
- specialization
- phone
- email

### Appointments

Connects patients and doctors and stores:

- appointment date
- appointment time
- duration
- status
- notes

### Appointment Status

Stores changes to appointment status over time.

The basic relationship can be represented as:

```text
Patient
   │
   └──── Appointment ──── Doctor
              │
              └──── Appointment Status History
```

---

## 🛠️ Technologies

### Backend

- Python
- Flask

### Database

- SQLite

### Frontend

- HTML
- CSS
- Jinja templates

### Development

- Git
- GitHub

---

## 📁 Repository Structure

```text
Hospital-Appointment-System/
│
├── README.md
├── app.py
├── database.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── index.html
│   ├── about.html
│   ├── appointments.html
│   ├── add_appointment.html
│   ├── patients.html
│   ├── add_patient.html
│   ├── doctors.html
│   └── add_doctor.html
│
└── static/
    └── css/
        └── style.css
```

The SQLite database file is generated locally and is intentionally excluded from Git using `.gitignore`.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/furkan9akin/Hospital-Appointment-System.git
```

Move into the project directory:

```bash
cd Hospital-Appointment-System
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```powershell
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

Start the application with:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

in a web browser.

The SQLite database is created automatically when the application starts for the first time.

---

## 🔐 Configuration

The Flask secret key can be provided through an environment variable:

```text
SECRET_KEY
```

Debug mode can be enabled locally using:

```text
FLASK_DEBUG=1
```

Debug mode is disabled by default.

---

## ✅ Input Validation

The application performs basic validation for:

- required patient information
- required doctor information
- email format
- date of birth
- appointment duration
- appointment status
- appointment date and time

Appointments cannot be created for a time in the past.

---

## 🌐 API Endpoints

### Appointments by Date

```http
GET /api/appointments/YYYY-MM-DD
```

Example:

```text
/api/appointments/2026-09-15
```

Returns appointments scheduled for the specified date.

### Dashboard Statistics

```http
GET /api/stats
```

Returns appointment statistics in JSON format.

---

## 🎓 What I Learned

This project helped me practice building a complete web application that connects frontend pages, backend application logic, and a relational database.

Some of the main concepts I explored include:

- Flask routing
- HTTP GET and POST requests
- HTML forms
- CRUD operations
- relational database design
- SQL queries
- foreign-key relationships
- server-side validation
- application status tracking
- JSON APIs
- environment-based configuration
- organizing a multi-page web application

The project helped me understand how different components of a web application work together rather than treating the frontend, backend, and database as separate systems.

---

## 🚀 Future Improvements

Possible future improvements include:

- prevent overlapping appointments for the same doctor
- add user authentication
- introduce different user roles
- add edit functionality for patients and doctors
- add appointment search and filtering
- add pagination
- add automated tests
- add CSRF protection
- improve accessibility
- deploy the application to a cloud platform

---

## ⚠️ Project Scope

This is an **educational software project** created to explore web application development.

It is not intended to manage real medical data or to be used as a production healthcare system.

---

## 👤 Developer

### Furkan Akın

High school senior and aspiring Computer Science major interested in software development, artificial intelligence, machine learning, robotics, and computer systems.

GitHub: [furkan9akin](https://github.com/furkan9akin)

---

## 📚 Project Context

Originally developed as a final project for:

**Kodland Python Level 3**

The project was later cleaned, documented, and expanded as part of my Computer Science portfolio.
