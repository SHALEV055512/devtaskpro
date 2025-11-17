# 🌿 DevTaskPro

A full-stack task and team management system designed for automated workflows, user role management, and real-time collaboration.  
Built with FastAPI, React, and Docker, this project demonstrates modern backend-frontend integration and cloud deployment on AWS EC2.  
🚧 This project is still in progress and continuously evolving.

---

## 🧠 Overview

DevTaskPro is a multi-role platform (Admin / Team Leader / Developer) for managing projects and automation tasks.  
The system includes secure authentication flows, email verification, password reset, and CRUD-based task management.  
It’s containerized with Docker Compose for easy deployment and uses FastAPI + SQLAlchemy for scalable backend logic.

---

## ⚙️ Technologies Used

### 🖥️ Backend
- **FastAPI (Python)** – REST API framework for high-performance backend  
- **SQLAlchemy ORM** – Data models, validation, and CRUD operations  
- **Pydantic** – Data validation and serialization  
- **Uvicorn** – ASGI server for production deployment  

---

### 💻 Frontend
- **React (Vite)** – Dynamic UI for task dashboards and user management  
- **Chakra UI** – Modern component-based design system  
- **Axios** – Handles API requests to the backend  

---

### ☁️ DevOps & Cloud
- **Docker & Docker Compose** – Multi-container orchestration  
- **AWS EC2** – Cloud deployment with persistent storage  
- **GitHub** – Version control & CI/CD integration  

---

## 🚀 How to Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/SHALEV055512/devtaskpro
cd devtaskpro
```

---

### 2️⃣ Run with Docker Compose
```bash
docker compose up --build
```

---

### 3️⃣ Run Locally (Dev Mode)

**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

**Frontend:**
```bash
cd new_frontend
npm install
npm run dev
```

---

## 🔐 Features
- User Registration & Login (JWT authentication)  
- Email Verification & Password Reset (SMTP)  
- Role-Based Access Control (Admin / Team Leader / Developer)  
- CRUD Operations for Tasks & Teams  
- Dockerized Microservices Architecture  
- Deployed on AWS EC2 with Persistent Volumes & Health Monitoring  
- Ready for CI/CD integration (GitHub Actions / Jenkins)  

---

## 📸 Demo Snapshot
🖼️ *Coming Soon* — Live demo & dashboard screenshots will be added soon.

---

## 🤝 Contributing
Pull requests are welcome!  
Feel free to fork the project and propose improvements or bug fixes.

---

## 🛡️ Security Note
All environment variables (API keys, SMTP credentials, database URL) are stored in a `.env` file and excluded via `.gitignore`.

---

## 📬 Contact
Built with ❤️ by **Shalev Harari**  
📧 **Email:** shalev2377@gmail.com  
🔗 **GitHub:** [github.com/SHALEV055512](https://github.com/SHALEV055512)  
🔗 **LinkedIn:** [linkedin.com/in/shalev-harari](https://linkedin.com/in/shalev-harari)
