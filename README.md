# Vishnu AI 1.0 - AI Hiring Platform

AI-powered hiring platform for Munjal Kiriu Manesar.

## Features

- ✅ Candidate OTP Login
- ✅ Resume Upload & Management
- ✅ Admin Dashboard
- ✅ Interview Scheduling
- ✅ Dark Mode UI
- ✅ Mobile Responsive (360px+)
- ✅ Animated Backgrounds
- ✅ Chatbot Sidebar

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py
```

Visit: http://localhost:5000

## Vercel Deployment

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit - Vishnu AI 1.0"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Vercel will auto-detect Flask
6. Add Environment Variables:
   - `SECRET_KEY`: Your Flask secret key
7. Click "Deploy"

### Environment Variables

Set these in Vercel Dashboard → Settings → Environment Variables:

- `SECRET_KEY`: Flask session secret (generate a random string)

## Project Structure

```
├── app.py                 # Main Flask application
├── api/
│   └── index.py          # Vercel serverless function
├── Templates/             # HTML templates
├── static/                # CSS, JS, assets
│   ├── css/
│   ├── js/
│   └── assets/
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel configuration
└── README.md
```

## Tech Stack

- Flask 3.0.0
- SQLite (with WAL mode)
- HTML5/CSS3/JavaScript
- Font Awesome Icons
- Nunito Font

## Admin Login

- Email: `admin@vishnu.ai`
- Password: (any - email only check)

## Jai Vishnu AI! 🚀

