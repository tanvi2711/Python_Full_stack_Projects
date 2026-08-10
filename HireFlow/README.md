# HireFlow

> A full-stack job recruitment platform built with React, Django, and MySQL.

HireFlow is a role-based recruitment platform that connects candidates and recruiters through a single application. Candidates can discover jobs, apply with resumes, track applications, save opportunities, and manage their profiles. Recruiters can create and manage job postings, review applicants, and update application statuses.

## ✨ Features

### Candidate
- Registration and secure login
- Personalized dashboard
- Job search and filtering
- Job details and skill information
- Resume and cover letter submission
- Application tracking
- Saved jobs
- Profile management

### Recruiter
- Recruiter registration and login
- Recruitment dashboard
- Create, edit, open, and close job postings
- View applicants for posted jobs
- Review resumes and cover letters
- Update application status
- Recruiter/company profile management

### Admin
- Django Admin interface
- Backend data and user management through Django Admin

## 🛠️ Tech Stack

**Frontend:** React 19, Vite, React Router, Axios, Lucide React, CSS3

**Backend:** Python, Django 5.2, Django ORM, Django Authentication, Django Sessions, Django Admin, django-cors-headers

**Database:** MySQL

**Tools:** Git, GitHub, VS Code, Postman

## 🏗️ Project Structure

```text
HireFlow/
├── backend/
│   ├── accounts/
│   ├── applications/
│   ├── jobs/
│   ├── profiles/
│   ├── config/
│   ├── media/
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 👥 User Roles

| Role | Main Capabilities |
|---|---|
| **Candidate** | Find jobs, apply, save jobs, track applications, manage profile |
| **Recruiter** | Create jobs, manage postings, view applicants, update application status |
| **Admin** | Manage backend data through Django Admin |

### Main Routes

**Candidate**
```text
/login
/register
/dashboard
/jobs
/applications
/profile
/saved
```

**Recruiter**
```text
/recruiter/dashboard
/recruiter/jobs
/recruiter/jobs/new
/recruiter/jobs/:id/edit
/recruiter/jobs/:id/applicants
/recruiter/profile
```

**Admin**
```text
/admin/
```

## 🔑 Authentication

HireFlow uses Django session-based authentication with CSRF protection and role-based access control.

```text
Login
  ↓
CSRF Token
  ↓
Django Authentication
  ↓
Session Created
  ↓
Role-Based Redirect
  ├── Candidate  → /dashboard
  └── Recruiter  → /recruiter/dashboard
```

## 🔌 Main API Endpoints

### Authentication
```text
GET  /api/auth/csrf/
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
GET  /api/auth/me/
```

### Profiles
```text
GET /api/profile/
PUT /api/profile/
```

### Jobs
```text
GET  /api/jobs/list/
GET  /api/jobs/<job_id>/
POST /api/jobs/
GET  /api/recruiter/jobs/
GET  /api/recruiter/dashboard/
```

### Applications
```text
POST  /api/jobs/<job_id>/apply/
GET   /api/applications/mine/
GET   /api/jobs/<job_id>/applicants/
PATCH /api/applications/<application_id>/status/
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- npm
- MySQL Server
- Git

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/HireFlow.git
cd HireFlow
```

### Database Setup

Create the MySQL database:

```sql
CREATE DATABASE hireflow_db;
```

### Backend Setup

```bash
cd backend
python -m venv venv
```

**Windows**
```powershell
venv\Scriptsctivate
```

**macOS/Linux**
```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install django-cors-headers
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create an admin account:

```bash
python manage.py createsuperuser
```

Start Django:

```bash
python manage.py runserver
```

Backend:
```text
http://127.0.0.1:8000/
```

Django Admin:
```text
http://127.0.0.1:8000/admin/
```

### Frontend Setup

Open another terminal:

```bash
cd frontend
npm install
```

Create `.env`:

```env
VITE_API_URL=http://localhost:8000/api
```

Start the frontend:

```bash
npm run dev
```

Frontend:
```text
http://localhost:5173/
```

## 🎨 UI Design

HireFlow follows a consistent **white, blue, and black** design system across the candidate and recruiter interfaces.

The UI focuses on:
- Clean professional layouts
- Clear typography
- Responsive dashboards and forms
- Blue primary actions
- Dark navigation
- Smooth hover and transition effects
- Desktop, tablet, and mobile support

## 🔐 Security

Before pushing the project to a public GitHub repository, keep sensitive files and credentials out of version control.

Do not commit:

```text
.env
backend/.env
backend/venv/
backend/media/
```

Database credentials and Django secret keys should be stored in environment variables.

## 📌 Current Limitations

- Saved jobs currently use browser `localStorage` rather than a dedicated database API.
- Administration currently uses Django Admin instead of a custom React admin dashboard.
- Interview and notification features are not connected to backend APIs yet.
- Production deployment configuration is not included.

## 🔮 Future Improvements

- Database-backed saved jobs
- Custom React Admin dashboard
- Interview scheduling
- Email and in-app notifications
- Recruiter analytics
- Candidate and recruiter verification
- Password reset and email verification
- Automated testing and CI/CD
- Docker and cloud deployment

## 👨‍💻 Project

**HireFlow — Full-Stack Job Recruitment Platform**

Built with **React, Django, and MySQL**.
