"""
Vercel Serverless Function for Vishnu AI Flask App
"""
import sys
import os

# Add parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set Vercel environment flag
os.environ['VERCEL'] = '1'

# Import Flask app
from app import app

# Export handler for Vercel
handler = app
