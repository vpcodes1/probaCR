"""Vercel serverless entry point for FastAPI."""
from app.main import app

# Vercel expects this
handler = app
