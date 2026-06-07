# 🚀 ProjectReviewer

ProjectReviewer is a full-stack GitHub repository analysis platform that helps developers evaluate project quality, identify missing best practices, and generate recruiter-friendly insights.



## ✨ Features

- 🔍 GitHub Repository Analysis
- 📊 Automated Project Scoring
- 🏗️ Technology Stack Detection
- 📝 Recruiter Verdict Generation
- 📄 PDF Report Export
- 📚 Analysis History Tracking
- 🔐 Google OAuth Authentication
- 👤 Guest Mode Access
- 🎯 Improvement Recommendations
- 📱 Responsive Design

---

## 🛠️ Tech Stack

### Frontend
- React
- Vite
- TypeScript
- Tailwind CSS

### Backend
- FastAPI
- Python

### Database
- PostgreSQL (Supabase)

### Authentication
- Google OAuth

### Deployment
- Vercel
- Render

--

## 🚀 Live Demo

https://github.com/Vigneshkolluru101103/Github_Project_Analyzer

--

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Vigneshkolluru101103/ProjectReviewer.git
cd ProjectReviewer
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🔑 Environment Variables

Frontend (.env)

```env
VITE_API_URL=your_backend_url
VITE_GOOGLE_CLIENT_ID=your_google_client_id
```

Backend (.env)

```env
DATABASE_URL=your_database_url
GOOGLE_CLIENT_ID=your_google_client_id
JWT_SECRET_KEY=your_secret_key
```

---

## 📈 How It Works

1. Enter a GitHub repository URL
2. Select project type
3. Run analysis
4. Detect technologies and project capabilities
5. Generate project score
6. View recruiter verdict
7. Download PDF report

---

## 📋 Sample Analysis Output

```text
Overall Score: 80/100

Project Maturity: Advanced

Recruiter Verdict:
Portfolio Ready ✅

Strengths:
✓ Frontend Framework
✓ Backend Framework
✓ Database Integration
✓ Authentication

Recommendations:
• Add Automated Testing
• Improve Deployment Pipeline
```

---

## 🎯 Future Improvements

- Advanced Code Analysis
- Testing Quality Detection
- CI/CD Detection
- Docker Detection
- Public Shareable Reports

---

## 👨‍💻 Author

Vignesh Kolluru

GitHub:
https://github.com/Vigneshkolluru101103

LinkedIn:
www.linkedin.com/in/vignesh-kolluru-334983316

---

## 📄 License

This project is licensed under the MIT License.
