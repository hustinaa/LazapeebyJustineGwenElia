## 🧾 LAZAPEE Payroll System

**LAZAPEE** is a simple Django-based payroll management system that lets you manage employee records, update salary details, and add overtime hours. It features a clean dashboard for tracking employee pay data and generating payslips with ease.

---

## 📁 Repository Setup

Follow the steps below to clone and run the project locally.

### ✅ Prerequisites

Make sure you have the following installed on your machine:

- [Python 3.x](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- pip (comes with Python)
- Optional: `venv` or `virtualenv` for virtual environments

---

## 📥 Cloning the Repository

```bash
[git clone https://github.com/yourusername/your-repo-name.git](https://github.com/hustinaa/LazapeebyJustineGwenElia.git)
cd LazapeebyJustineGwenElia
```

---

## 🐍 Setting Up a Virtual Environment (Recommended)

```bash
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
```

---

## 📦 Installing Dependencies

Make sure you're in the root project folder, then run:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Running the Project

Apply migrations and run the development server:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Go to `http://127.0.0.1:8000/` in your browser to view the app.

---

## 🧭 Project Structure

```
LazapeebyJustineGwenElia/
├── Lazapee/          # Django project settings
├── payroll_app/      # Main app with employee & payroll logic
├── db.sqlite3        # SQLite database (for local dev)
└── manage.py         # Django management script
```

---

## 👩‍💻 About the Developer

Developed by Justine Evora, Elia Ching, and Gwyneth Pamplona 
Currently studying **Management Information Systems** at **Ateneo de Manila University**.

If you find this project helpful, feel free to give it a ⭐ and connect!
