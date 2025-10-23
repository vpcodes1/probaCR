# YUSEARCH - Quick Start Guide

Get up and running with YUSEARCH in 5 minutes!

## What You Need

1. **Anthropic API Key** - [Get one free here](https://console.anthropic.com/)
2. Python 3.11+ and Node.js 18+

## Setup in 3 Steps

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run backend
uvicorn app.main:app --reload
```

Backend will run on http://localhost:8000

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run frontend
npm run dev
```

Frontend will run on http://localhost:5173

### 3. Generate Your First Report

1. Open http://localhost:5173 in your browser
2. Click "Start Your FREE Trial"
3. Enter prospect details:
   - **Prospect Name**: "Satya Nadella"
   - **Company Name**: "Microsoft"
4. Click "Generate Report"
5. Wait 3-5 minutes for the comprehensive report!

## What You Get

Your report includes:

- **Executive Summary** - Quick overview of prospect
- **Quick Facts** - Title, location, LinkedIn, etc.
- **Conversation Starters** - 3-5 perfect opening lines
- **Talking Points** - 8-10 relevant discussion topics
- **Personality Insights** - Communication style analysis
- **Recommended Approach** - Strategic advice for the meeting
- **Company Background** - Funding, size, industry, recent news
- **Recent News** - Latest company developments

## Export Options

- **PDF** - Professional report for client files
- **Word** - Editable document for customization

## Troubleshooting

**Backend won't start?**
- Check Python version: `python --version` (need 3.11+)
- Verify virtual environment is activated

**Frontend won't start?**
- Check Node version: `node --version` (need 18+)
- Try removing `node_modules` and running `npm install` again

**Report generation fails?**
- Verify API key is correct in `.env`
- Check backend terminal for error messages
- Ensure internet connection is working

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for advanced configuration
- Explore the API docs at http://localhost:8000/docs

## Need Help?

- Check backend logs in terminal
- Review API documentation at `/docs`
- Ensure all dependencies are installed correctly

---

**Built with**: Python, FastAPI, React, Anthropic Claude, TailwindCSS

**License**: Proprietary
