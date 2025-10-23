#!/bin/bash

# YUSEARCH - Automated Setup Script
# This script automatically sets up the entire application

set -e  # Exit on error

echo "================================================"
echo "  YUSEARCH - Automated Setup"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Please install Python 3.11+ from https://www.python.org/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is not installed${NC}"
    echo "Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi

echo -e "${GREEN}✓${NC} Python and Node.js found"
echo ""

# Step 1: Setup Backend
echo -e "${YELLOW}[1/4] Setting up Backend...${NC}"
cd backend

# Create virtual environment
echo "  Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "  Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo -e "${GREEN}✓${NC} Backend dependencies installed"
echo ""

# Step 2: Configure Environment
echo -e "${YELLOW}[2/4] Configuring Environment...${NC}"

if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${YELLOW}!"
    echo -e "  IMPORTANT: You need to add your API keys to backend/.env"
    echo -e "  "
    echo -e "  Required:"
    echo -e "  - ANTHROPIC_API_KEY (get free at https://console.anthropic.com/)"
    echo -e "  "
    echo -e "  Optional:"
    echo -e "  - SERPER_API_KEY (get free at https://serper.dev/)"
    echo -e "${NC}"

    # Try to open the file for editing
    if command -v nano &> /dev/null; then
        read -p "Press Enter to edit .env file now, or Ctrl+C to edit later..."
        nano .env
    else
        echo ""
        echo "Please edit backend/.env and add your API keys"
        read -p "Press Enter when done..."
    fi
else
    echo -e "${GREEN}✓${NC} .env file already exists"
fi

cd ..
echo ""

# Step 3: Setup Frontend
echo -e "${YELLOW}[3/4] Setting up Frontend...${NC}"
cd frontend

echo "  Installing Node.js dependencies..."
npm install --silent

echo -e "${GREEN}✓${NC} Frontend dependencies installed"
echo ""

cd ..

# Step 4: Create start script
echo -e "${YELLOW}[4/4] Creating start scripts...${NC}"

# Create start script
cat > start.sh << 'EOF'
#!/bin/bash

# Start YUSEARCH application

echo "Starting YUSEARCH..."
echo ""

# Start backend in background
echo "Starting backend on http://localhost:8000"
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 3

# Start frontend in background
echo "Starting frontend on http://localhost:5173"
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "================================================"
echo "  YUSEARCH is running!"
echo "================================================"
echo ""
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
echo "  Logs:"
echo "  - Backend:  backend.log"
echo "  - Frontend: frontend.log"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Save PIDs
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f .backend.pid .frontend.pid; echo ''; echo 'YUSEARCH stopped'; exit" INT
wait
EOF

chmod +x start.sh

# Create stop script
cat > stop.sh << 'EOF'
#!/bin/bash

echo "Stopping YUSEARCH..."

if [ -f .backend.pid ]; then
    kill $(cat .backend.pid) 2>/dev/null
    rm .backend.pid
fi

if [ -f .frontend.pid ]; then
    kill $(cat .frontend.pid) 2>/dev/null
    rm .frontend.pid
fi

# Kill any remaining processes
pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "vite" 2>/dev/null

echo "YUSEARCH stopped"
EOF

chmod +x stop.sh

echo -e "${GREEN}✓${NC} Start scripts created"
echo ""

# Setup complete
echo "================================================"
echo -e "${GREEN}  Setup Complete!${NC}"
echo "================================================"
echo ""
echo "To start YUSEARCH:"
echo -e "  ${YELLOW}./start.sh${NC}"
echo ""
echo "To stop YUSEARCH:"
echo -e "  ${YELLOW}./stop.sh${NC}"
echo ""
echo "Or use Docker:"
echo -e "  ${YELLOW}docker-compose up${NC}"
echo ""
echo "Don't forget to add your API keys to backend/.env!"
echo ""
