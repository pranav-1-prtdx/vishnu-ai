# Vercel Deployment Guide - Vishnu AI 1.0

## Quick Deploy Steps

### 1. GitHub Setup

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Vishnu AI 1.0 - Ready for Vercel"

# Create GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/vishnu-ai.git
git branch -M main
git push -u origin main
```

### 2. Vercel Deployment

1. **Go to**: https://vercel.com
2. **Sign in** with GitHub
3. **Click**: "Add New Project"
4. **Import** your GitHub repository
5. **Vercel will auto-detect** Flask
6. **Add Environment Variable**:
   - Key: `SECRET_KEY`
   - Value: `VishnuAI_Secret_Key_2025_MunjalKiriu_Production` (or generate a random string)
7. **Click**: "Deploy"

### 3. After Deployment

- Your app will be live at: `https://your-project.vercel.app`
- All routes will work automatically
- Static files (CSS, JS, images) are served automatically
- Database uses `/tmp` directory on Vercel

### 4. Environment Variables (Optional)

If you want to add email functionality later:

- `SMTP_HOST`: smtp.gmail.com
- `SMTP_PORT`: 587
- `SMTP_USER`: your-email@gmail.com
- `SMTP_PASS`: your-app-password

## Troubleshooting

### If you get 404 errors:
- Check `vercel.json` is in root
- Ensure `app.py` is in root
- Check build logs in Vercel dashboard

### If database errors:
- SQLite uses `/tmp` on Vercel (ephemeral storage)
- Consider using a cloud database for production

### If static files don't load:
- Ensure `static/` folder is in root
- Check file paths in templates use `/static/...`

## Success! 🎉

Your Vishnu AI platform is now live!

**Jai Vishnu AI!**

