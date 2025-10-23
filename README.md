# YUSEARCH - AI-Powered Prospect Research Tool

## Overview

YUSEARCH is an AI-powered sales intelligence platform that generates comprehensive prospect reports in under 5 minutes, replacing hours of manual research.

## Features

- **5-Minute Intelligence Reports**: Complete prospect analysis in minutes
- **AI-Powered Insights**: Personality analysis, talking points, and conversation starters
- **Comprehensive Data**: Company background, news, funding, personal insights
- **Multiple Export Formats**: PDF and Word document exports
- **Enterprise Intelligence at SMB Prices**: Affordable for small businesses and freelancers

## System Architecture

```
┌─────────────────┐
│   Frontend      │  React SPA
│   (React)       │
└────────┬────────┘
         │
┌────────▼────────┐
│   API Layer     │  FastAPI
│   (FastAPI)     │
└────────┬────────┘
         │
┌────────▼────────────────────────┐
│   Research Orchestrator         │
├─────────────────────────────────┤
│ ┌──────────┐ ┌───────────────┐ │
│ │ Company  │ │   Person      │ │
│ │ Research │ │   Research    │ │
│ └──────────┘ └───────────────┘ │
│ ┌──────────┐ ┌───────────────┐ │
│ │   News   │ │   Social      │ │
│ │ Research │ │   Media       │ │
│ └──────────┘ └───────────────┘ │
└────────┬────────────────────────┘
         │
┌────────▼────────┐
│   AI Analysis   │  Claude API
│   Engine        │
└────────┬────────┘
         │
┌────────▼────────┐
│   Report        │  PDF/Word
│   Generator     │
└─────────────────┘
```

## Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **AI**: Anthropic Claude API
- **Data Collection**: BeautifulSoup4, Requests, Serper API (Google Search)
- **Reports**: ReportLab (PDF), python-docx (Word)
- **Database**: SQLite
- **Frontend**: React 18, Vite, TailwindCSS
- **Deployment**: Docker

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Anthropic API Key (for AI analysis)
- Serper API Key (optional, for enhanced Google search)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd probaCR
```

2. Set up backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. Set up frontend:
```bash
cd ../frontend
npm install
```

### Running the Application

1. Start the backend:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2. Start the frontend:
```bash
cd frontend
npm run dev
```

3. Access the application at `http://localhost:5173`

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

## Configuration

Edit `.env` file with your credentials:

```env
# AI Configuration
ANTHROPIC_API_KEY=your_api_key_here
OPENAI_API_KEY=optional_openai_key

# Search Configuration
SERPER_API_KEY=your_serper_key_here

# Database
DATABASE_URL=sqlite:///./yusearch.db

# Security
SECRET_KEY=your_secret_key_here
```

## Project Structure

```
probaCR/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration
│   │   ├── models/              # Database models
│   │   ├── api/                 # API routes
│   │   ├── core/                # Core business logic
│   │   │   ├── orchestrator.py  # Research orchestration
│   │   │   ├── collectors/      # Data collectors
│   │   │   ├── analyzers/       # AI analyzers
│   │   │   └── generators/      # Report generators
│   │   └── utils/               # Utilities
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API services
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
└── README.md
```

## Usage

1. **Create a Report**:
   - Enter prospect name and company
   - Click "Generate Report"
   - Wait ~3-5 minutes for comprehensive analysis

2. **View Report**:
   - Review company background
   - Check personal insights
   - Read AI-generated talking points
   - Use conversation starters

3. **Export**:
   - Download as PDF for client files
   - Export to Word for editing

## Features in Detail

### Company Research
- Funding information
- Recent news and press releases
- Company growth metrics
- Industry positioning
- Key executives

### Personal Insights
- Educational background
- Career trajectory
- Shared interests
- Communication style analysis

### AI-Powered Analysis
- Personality insights
- Recommended approach
- Custom talking points
- Conversation starters (3-5 per report)

### Export Options
- Professional PDF reports
- Editable Word documents
- Email-friendly format

## Development

### Running Tests
```bash
cd backend
pytest
```

### Code Quality
```bash
# Format code
black app/
isort app/

# Lint
flake8 app/
pylint app/
```

## Deployment

### Using Docker
```bash
docker-compose up -d
```

### Manual Deployment
See `DEPLOYMENT.md` for detailed production deployment instructions.

## Pricing Tiers (Planned)

- **Free Trial**: 3 reports/month
- **Professional**: $29/month - 50 reports/month
- **Business**: $99/month - Unlimited reports
- **Enterprise**: Custom pricing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

Proprietary - All rights reserved

## Support

For support, email support@yusearch.com or visit our documentation at https://docs.yusearch.com

## Roadmap

- [ ] Core MVP (v1.0)
- [ ] LinkedIn integration
- [ ] CRM integrations (Salesforce, HubSpot)
- [ ] Chrome extension
- [ ] Mobile app
- [ ] Team collaboration features
- [ ] Advanced analytics dashboard

---

Built with ❤️ to help sales professionals compete at the highest level.
