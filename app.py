# app.py — VISHNU AI 1.0 — FULLY WORKING (DEC 2025)
import os
import sqlite3
import time
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from contextlib import contextmanager

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'VishnuAI_Secret_Key_2025_MunjalKiriu')

# Database connection helper with proper error handling
@contextmanager
def get_db():
    """Context manager for database connections - ensures proper cleanup"""
    conn = None
    try:
        # Use /tmp for Vercel (writable directory) or local for development
        if os.environ.get('VERCEL'):
            db_path = '/tmp/candidates.db'
        else:
            db_path = 'candidates.db'
        
        # Ensure directory exists
        if os.environ.get('VERCEL'):
            os.makedirs('/tmp', exist_ok=True)
        
        conn = sqlite3.connect(db_path, timeout=10.0, check_same_thread=False)
        conn.execute('PRAGMA journal_mode=WAL')  # Enable WAL mode for better concurrency
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

# Database init
def init_db():
    with get_db() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, email TEXT, post TEXT, resume_path TEXT, status TEXT DEFAULT 'Pending', zoom_link TEXT
        )''')
        # Add zoom_link column if it doesn't exist
        try:
            c.execute('ALTER TABLE candidates ADD COLUMN zoom_link TEXT')
        except:
            pass
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE, role TEXT, created_at TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS otps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT, otp TEXT, expires_at TEXT
        )''')
        
        # Seed Admin
        c.execute('SELECT * FROM users WHERE email = ?', ('admin@vishnu.ai',))
        if not c.fetchone():
            c.execute('INSERT INTO users (email, role, created_at) VALUES (?, ?, ?)',
                      ('admin@vishnu.ai', 'interviewer', time.strftime("%Y-%m-%d %H:%M:%S")))

# Initialize database (will be called by api/index.py on Vercel)
# Skip here to avoid import-time initialization issues
if __name__ == '__main__':
    init_db()

# Login Required Decorator
def login_required(role):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'user' not in session or session['user']['role'] != role:
                flash('Please log in to continue.', 'error')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return wrapped
    return decorator

# Home
@app.route('/')
def index():
    return render_template('index.html')

# Login Page
@app.route('/login')
def login():
    # Clear OTP state if requested
    if request.args.get('clear_otp'):
        session.pop('otp_requested', None)
        session.pop('otp_email', None)
    return render_template('login.html')

# Request OTP
@app.route('/auth/request_otp', methods=['POST'])
def request_otp():
    email = request.form.get('email', '').strip()
    if not email:
        flash('Enter a valid email.', 'error')
        return redirect(url_for('login'))
    
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM users WHERE email = ? AND role = ?', (email, 'candidate'))
            if not c.fetchone():
                c.execute('INSERT INTO users (email, role, created_at) VALUES (?, ?, ?)',
                          (email, 'candidate', time.strftime("%Y-%m-%d %H:%M:%S")))
            
            otp = str(time.time())[-6:].replace('.', '')[:6]
            expires_at = (time.time() + 600)
            c.execute('DELETE FROM otps WHERE email = ?', (email,))
            c.execute('INSERT INTO otps (email, otp, expires_at) VALUES (?, ?, ?)', (email, otp, expires_at))
        
        session['otp_requested'] = True
        session['otp_email'] = email
        
        flash(f'OTP sent! (For testing: {otp})', 'success')
    except sqlite3.Error as e:
        flash('Database error. Please try again.', 'error')
        app.logger.error(f'Database error in request_otp: {e}')
    
    return redirect(url_for('login'))

# Verify OTP
@app.route('/auth/verify_otp', methods=['POST'])
def verify_otp():
    email = request.form.get('email')
    otp = request.form.get('otp')
    
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM otps WHERE email = ? AND otp = ? AND expires_at > ?', 
                      (email, otp, time.time()))
            if c.fetchone():
                session['user'] = {'email': email, 'role': 'candidate'}
                c.execute('DELETE FROM otps WHERE email = ?', (email,))
                session.pop('otp_requested', None)
                session.pop('otp_email', None)
                flash('Login successful!', 'success')
                return redirect(url_for('candidate_dashboard'))
    except sqlite3.Error as e:
        flash('Database error. Please try again.', 'error')
        app.logger.error(f'Database error in verify_otp: {e}')
        return redirect(url_for('login'))
    
    flash('Invalid or expired OTP.', 'error')
    return redirect(url_for('login'))

# Admin Login
@app.route('/auth/login', methods=['POST'])
def auth_login():
    email = request.form.get('email')
    if email == 'admin@vishnu.ai':
        session['user'] = {'email': email, 'role': 'interviewer'}
        flash('Admin logged in!', 'success')
        return redirect(url_for('admin_dashboard'))
    flash('Invalid credentials.', 'error')
    return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

# Candidate Dashboard
@app.route('/candidate/dashboard')
@login_required('candidate')
def candidate_dashboard():
    candidate = None
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM candidates WHERE email = ? ORDER BY id DESC LIMIT 1', (session['user']['email'],))
            candidate = c.fetchone()
    except sqlite3.Error as e:
        flash('Error loading dashboard. Please try again.', 'error')
        app.logger.error(f'Database error in candidate_dashboard: {e}')
    
    return render_template('candidate_dashboard.html', candidate=candidate)

# Submit Resume
@app.route('/submit_resume', methods=['GET', 'POST'])
@login_required('candidate')
def submit_resume():
    if request.method == 'POST':
        name = request.form.get('name')
        post = request.form.get('post')
        resume = request.files.get('resume')
        
        if not all([name, post, resume]):
            flash('All fields required!', 'error')
            return redirect(url_for('submit_resume'))
        
        if not resume.filename.lower().endswith('.pdf'):
            flash('Only PDF allowed!', 'error')
            return redirect(url_for('submit_resume'))
        
        # Use /tmp/resumes for Vercel or local resumes folder
        if os.environ.get('VERCEL'):
            resumes_dir = '/tmp/resumes'
        else:
            resumes_dir = 'resumes'
        os.makedirs(resumes_dir, exist_ok=True)
        filename = f"{name}_{int(time.time())}.pdf"
        path = os.path.join(resumes_dir, filename)
        resume.save(path)
        
        try:
            with get_db() as conn:
                c = conn.cursor()
                # Check if candidate already exists
                c.execute('SELECT id FROM candidates WHERE email = ?', (session['user']['email'],))
                existing = c.fetchone()
                
                if existing:
                    # Update existing record
                    c.execute('UPDATE candidates SET name = ?, post = ?, resume_path = ?, status = ? WHERE email = ?',
                              (name, post, path, 'Pending', session['user']['email']))
                else:
                    # Insert new record
                    c.execute('INSERT INTO candidates (name, email, post, resume_path, status) VALUES (?, ?, ?, ?, ?)',
                              (name, session['user']['email'], post, path, 'Pending'))
            
            flash('Resume submitted! Our AI is reviewing...', 'success')
            return redirect(url_for('thank_you'))
        except sqlite3.Error as e:
            flash('Database error. Please try again.', 'error')
            app.logger.error(f'Database error in submit_resume: {e}')
            return redirect(url_for('submit_resume'))
    
    return render_template('submit_resume.html')

# Thank You Page
@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

# Admin Dashboard
@app.route('/admin_dashboard')
@login_required('interviewer')
def admin_dashboard():
    candidates = []
    try:
        with get_db() as conn:
            c = conn.cursor()
            c.execute('SELECT id, name, email, post, status, resume_path, zoom_link FROM candidates ORDER BY id DESC')
            candidates = c.fetchall()
    except sqlite3.Error as e:
        flash('Error loading dashboard. Please try again.', 'error')
        app.logger.error(f'Database error in admin_dashboard: {e}')
    
    return render_template('admin_dashboard.html', candidates=candidates)

# Download Resume
@app.route('/download/<path:filename>')
@login_required('interviewer')
def download_resume(filename):
    # Extract just the filename from the path
    if '/' in filename:
        filename = filename.split('/')[-1]
    if os.environ.get('VERCEL'):
        resumes_dir = '/tmp/resumes'
    else:
        resumes_dir = 'resumes'
    return send_from_directory(resumes_dir, filename, as_attachment=True)

# Schedule Interview Page
@app.route('/schedule_interview/<int:candidate_id>', methods=['GET', 'POST'])
@login_required('interviewer')
def schedule_interview(candidate_id):
    if request.method == 'POST':
        zoom_link = request.form.get('zoom_link', '').strip()
        if not zoom_link:
            flash('Please enter a Zoom link.', 'error')
            return redirect(url_for('schedule_interview', candidate_id=candidate_id))
        
        try:
            with get_db() as conn:
                c = conn.cursor()
                c.execute('UPDATE candidates SET status = ?, zoom_link = ? WHERE id = ?', 
                          ('Interview Scheduled', zoom_link, candidate_id))
            flash('Interview scheduled! AI Bot will join soon.', 'success')
            return redirect(url_for('admin_dashboard'))
        except sqlite3.Error as e:
            flash('Database error. Please try again.', 'error')
            app.logger.error(f'Database error in schedule_interview: {e}')
            return redirect(url_for('schedule_interview', candidate_id=candidate_id))
    
    return render_template('schedule_interview.html', candidate_id=candidate_id)

# Update Status
@app.route('/update_status/<int:candidate_id>', methods=['POST'])
@login_required('interviewer')
def update_status(candidate_id):
    new_status = request.form.get('status')
    if new_status:
        try:
            with get_db() as conn:
                c = conn.cursor()
                c.execute('UPDATE candidates SET status = ? WHERE id = ?', (new_status, candidate_id))
            flash(f'Status updated to {new_status}!', 'success')
        except sqlite3.Error as e:
            flash('Database error. Please try again.', 'error')
            app.logger.error(f'Database error in update_status: {e}')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)