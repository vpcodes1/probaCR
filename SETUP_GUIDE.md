# YUSEARCH Setup Guide

Complete step-by-step guide to get YUSEARCH up and running.

## Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn
- Git

## API Keys Required

You'll need the following API keys:

1. **Anthropic API Key** (Required for AI analysis)
   - Sign up at: https://console.anthropic.com/
   - Get your API key from the dashboard

2. **Serper API Key** (Optional but recommended for better Google search)
   - Sign up at: https://serper.dev/
   - Free tier: 2,500 searches/month

## Step 1: Clone the Repository

```bash
git clone <repository-url>
cd probaCR
```

## Step 2: Backend Setup

### 2.1 Create Python Virtual Environment

```bash
cd backend
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 2.2 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.3 Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your favorite text editor
nano .env  # or vim, code, etc.
```

Add your API keys to `.env`:

```env
ANTHROPIC_API_KEY=your_actual_anthropic_key_here
SERPER_API_KEY=your_actual_serper_key_here
SECRET_KEY=change-this-to-a-random-string
```

### 2.4 Test Backend

```bash
# Run the backend server
uvicorn app.main:app --reload

# You should see:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

Visit `http://localhost:8000/docs` to see the API documentation.

## Step 3: Frontend Setup

### 3.1 Install Dependencies

```bash
cd ../frontend
npm install
```

### 3.2 Run Frontend Development Server

```bash
npm run dev

# You should see:
# VITE ready in X ms
# ➜  Local:   http://localhost:5173/
```

## Step 4: Test the Application

1. Open your browser to `http://localhost:5173`
2. Click "Start Your FREE Trial"
3. Enter a prospect name and company (e.g., "Elon Musk" and "Tesla")
4. Click "Generate Report"
5. Wait 3-5 minutes for the report to complete

## Using Docker (Alternative)

If you prefer Docker:

```bash
# Make sure you have .env file configured in backend/
cd probaCR

# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Troubleshooting

### Issue: "No module named 'app'"

**Solution**: Make sure you're in the backend directory and the virtual environment is activated.

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### Issue: "Anthropic API key not configured"

**Solution**: Check your `.env` file has the correct API key without quotes:

```env
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Issue: Frontend can't connect to backend

**Solution**: Make sure both servers are running:
- Backend on port 8000
- Frontend on port 5173

Check the proxy configuration in `frontend/vite.config.js`.

### Issue: Reports take too long or timeout

**Solution**:
1. Check your internet connection
2. Verify API keys are valid
3. Try with a well-known person/company first
4. Check backend logs for errors

### Issue: PDF/Word export not working

**Solution**: Make sure the `reports` directory exists:

```bash
cd backend
mkdir -p reports
```

## Production Deployment

For production deployment, see `DEPLOYMENT.md` (to be created).

Key considerations:
- Use a production-grade database (PostgreSQL)
- Set up proper authentication
- Use environment-specific configurations
- Enable HTTPS
- Set up rate limiting
- Configure monitoring and logging

## Development Workflow

1. **Make changes to backend**:
   - Edit files in `backend/app/`
   - Backend auto-reloads with `--reload` flag

2. **Make changes to frontend**:
   - Edit files in `frontend/src/`
   - Frontend auto-reloads with Vite HMR

3. **Run tests**:
   ```bash
   # Backend tests
   cd backend
   pytest

   # Frontend tests (if added)
   cd frontend
   npm test
   ```

## Next Steps

- Add user authentication
- Implement subscription management
- Add more data sources (LinkedIn API, etc.)
- Enhance AI analysis prompts
- Add analytics dashboard
- Create Chrome extension

## Support

For issues or questions:
- Check the main `README.md`
- Review API docs at `/docs`
- Check logs in terminal
- Contact support (if available)

## License

Proprietary - All rights reserved
