# Smart CRM – Customer Relationship & Sales Management System

Smart CRM is a web-based Customer Relationship Management (CRM) system developed using Django and Python.

The application helps businesses manage customers, leads, sales deals, follow-ups, tasks, and business reports from a single platform.

---

## 🚀 Project Overview

Smart CRM is designed to simplify customer and sales management activities.

The system provides a centralized platform to:

- Manage customer information
- Track potential leads
- Manage sales deals
- Schedule follow-up tasks
- Monitor sales pipeline
- Track revenue
- Generate business reports
- Manage user accounts securely

---

## ✨ Features

### 🔐 Authentication

- User Signup
- User Login
- User Logout
- Forgot Password
- Password Reset
- Remember Me
- Profile Management

### 👥 Customer Management

- Add customers
- View customer details
- Edit customer information
- Delete customers
- Search customers
- Filter customers by status
- Active / Inactive / Pending status

### 🎯 Lead Management

- Add new leads
- Edit leads
- Delete leads
- Search leads
- Filter by lead status
- Filter by lead source
- Track lead conversion

### 💰 Sales Management

- Create sales deals
- Assign customers
- Link leads to deals
- Track deal amount
- Manage sales stages
- Track Open / Won / Lost deals
- Calculate revenue
- Track pipeline value

### 📋 Task & Follow-up Management

- Create tasks
- Assign tasks to customers
- Set task type
- Set due date and time
- Set priority
- Track task status
- Search tasks
- Filter tasks

### 📊 Dashboard

The dashboard provides an overview of:

- Total customers
- Active customers
- Total leads
- Active leads
- Total deals
- Open deals
- Won deals
- Total revenue
- Pending tasks
- Recent customers
- Upcoming tasks
- Sales performance

### 📈 Reports

The Reports module provides:

- Customer Overview
- Lead Performance
- Sales Pipeline
- Deal Status
- Revenue Summary
- Task Overview
- Task Priority Analysis

---

## 🛠️ Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- Python
- Django

### Database

- SQLite

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

## 📂 Project Structure

```text
SmartCRM/
│
├── manage.py
│
├── smartcrm/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── customers/
│   ├── migrations/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── leads/
│   ├── migrations/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── sales/
│   ├── migrations/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── tasks/
│   ├── migrations/
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── reports/
│   ├── migrations/
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── profile.html
│   ├── dashboard.html
│   ├── customers.html
│   ├── customer_form.html
│   ├── leads.html
│   ├── lead_form.html
│   ├── sales.html
│   ├── deal_form.html
│   ├── tasks.html
│   ├── task_form.html
│   ├── reports.html
│   ├── password_reset.html
│   ├── password_reset_done.html
│   ├── password_reset_confirm.html
│   └── password_reset_complete.html
│
├── static/
│   └── css/
│       └── style.css
│
├── db.sqlite3
│
└── README.md