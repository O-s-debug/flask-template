
# 🚀 Flask + FastAPI Hackathon Template

A modern and secure **hackathon starter template** that combines a **Flask frontend** with a **FastAPI backend** — designed for rapid prototyping of AI/ML, data-driven, or web-based projects.

---

## 🌟 Features at a Glance

✅ User Registration and Login  
✅ Password Recovery via Email  
✅ User Blocking on Failed Attempts  
✅ Email Encryption with Fernet  
✅ SQLite Database Integration  
✅ CSRF Protection using Flask-WTF  
✅ Logging of Login Attempts  
✅ FastAPI for ML Model Hosting or Inference  
✅ Clean UI via Jinja Templates

---

## 📁 Folder Structure

```

hackathon-template/
│
├── app/                      # Flask Frontend
│   ├── __init__.py           # App factory
│   ├── routers.py            # Route definitions
│   ├── forms.py              # WTForms
│   ├── utils.py              # Helper functions
│   ├── templates/            # Jinja2 templates
│   └── static/               # Static files (css, js, images)
│
├── api_server/               # FastAPI Backend
│   ├── main.py               # FastAPI entry point
│   ├── predict.py            # Example model inference
│   ├── schemes.py            # Pydantic schemas
│   ├── utils.py              # Utility functions
│   └── models/               # Model files and loader
│
├── database/
│   ├── database.py           # SQLite DB logic
│   └── database.db           # SQLite file (auto-generated)
│
├── .env                      # Environment variables
├── requirements.txt          # Python dependencies
├── .gitignore
├── README.md                 # You're here!

````

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/diveshadivarekar/hackathon-template.git
cd hackathon-template
````

---

### 2. Create and Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> ✅ Ensure you are using Python 3.8 or newer.

---

### 4. Set Up Environment Variables

Create a `.env` file in the root directory with:

```env
FERNET_KEY=your_generated_fernet_key_here
EMAIL_SENDER=your_email@example.com
EMAIL_PASSWORD=your_email_password_or_app_password
```

#### Generate a Fernet Key

```python
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

---

### 5. Initialize the SQLite Database

```bash
python database/database.py
```

You should see:

```
Database initialized with users and login_logs tables.
Database initiated successfully
```

---

## 🚦 Running the App

### ▶️ Flask Frontend (Web UI)

```bash
flask --app app run
```

Or (if using `app/main.py`):

```bash
python app/main.py
```

Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

### ⚡ FastAPI Backend (API/Model Server)

```bash
uvicorn api_server.main:app --reload --port 8000
```

Visit Swagger docs at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

You can define your ML model logic in `predict.py` and expose endpoints using FastAPI.

---

## 🔐 Security Features

* ✅ Hashed Passwords (Werkzeug)
* ✅ Fernet Encryption for Emails
* ✅ CSRF Protection via Flask-WTF
* ✅ Email-based Password Recovery
* ✅ Login Attempt Logs & IP Tracking
* ✅ Temporary Blocking after Multiple Failures


---

## ✅ To-Do / Future Ideas

* [ ] Add OTP-based phone/email verification
* [ ] JWT-based sessions for API
* [ ] Frontend styling with TailwindCSS or Bootstrap
* [ ] Docker support for Flask + FastAPI
* [ ] Rate Limiting and IP Blacklisting
* [ ] Admin Panel with user stats
* [ ] OAuth login (Google, GitHub)

---

## 🤝 Contributing

Want to improve this template or add new features? PRs are welcome!

### 📌 Guidelines

* Fork the repo and create your branch: `git checkout -b feature/new-feature`
* Commit changes: `git commit -am 'Add new feature'`
* Push to branch: `git push origin feature/new-feature`
* Open a Pull Request

---

## 👨‍💻 Maintainer

Made with ❤️ by [Divesh Adivarekar](https://github.com/diveshadivarekar)

---

## 📜 License

MIT License. Use it freely and hack away!

