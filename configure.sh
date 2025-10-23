#!/bin/bash

# YUSEARCH - API Key Configuration Helper
# Helps users easily add their API keys

echo "================================================"
echo "  YUSEARCH - API Key Configuration"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Navigate to backend
cd backend

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

echo -e "${BLUE}To use YUSEARCH, you need an Anthropic API key.${NC}"
echo ""
echo "📝 How to get your FREE Anthropic API key:"
echo "   1. Visit: https://console.anthropic.com/"
echo "   2. Sign up for a free account"
echo "   3. Go to 'API Keys' section"
echo "   4. Click 'Create Key'"
echo "   5. Copy the key"
echo ""
echo -e "${YELLOW}Opening Anthropic Console in your browser...${NC}"

# Try to open browser
if command -v xdg-open &> /dev/null; then
    xdg-open "https://console.anthropic.com/settings/keys" &> /dev/null
elif command -v open &> /dev/null; then
    open "https://console.anthropic.com/settings/keys" &> /dev/null
else
    echo "Please open: https://console.anthropic.com/settings/keys"
fi

echo ""
read -p "Press Enter when you have your API key..."
echo ""

# Get Anthropic API key
echo -e "${GREEN}Enter your Anthropic API key:${NC}"
read -p "Key: " anthropic_key

# Update .env file
if [ ! -z "$anthropic_key" ]; then
    # Check if key exists in .env
    if grep -q "ANTHROPIC_API_KEY=" .env; then
        # Update existing key
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            sed -i '' "s/ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=$anthropic_key/" .env
        else
            # Linux
            sed -i "s/ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=$anthropic_key/" .env
        fi
    else
        # Add new key
        echo "ANTHROPIC_API_KEY=$anthropic_key" >> .env
    fi
    echo -e "${GREEN}✓${NC} Anthropic API key saved!"
else
    echo -e "${YELLOW}⚠${NC} No key entered, skipping..."
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Ask about Serper API (optional)
echo -e "${BLUE}Optional: Add Serper API key for better Google search${NC}"
echo ""
echo "📝 How to get FREE Serper API key (optional but recommended):"
echo "   1. Visit: https://serper.dev/"
echo "   2. Sign up (2,500 free searches/month)"
echo "   3. Copy your API key"
echo ""
read -p "Do you want to add Serper API key? (y/n): " add_serper

if [ "$add_serper" = "y" ] || [ "$add_serper" = "Y" ]; then
    # Try to open browser
    if command -v xdg-open &> /dev/null; then
        xdg-open "https://serper.dev/" &> /dev/null
    elif command -v open &> /dev/null; then
        open "https://serper.dev/" &> /dev/null
    fi

    echo ""
    echo -e "${GREEN}Enter your Serper API key:${NC}"
    read -p "Key: " serper_key

    if [ ! -z "$serper_key" ]; then
        if grep -q "SERPER_API_KEY=" .env; then
            if [[ "$OSTYPE" == "darwin"* ]]; then
                sed -i '' "s/SERPER_API_KEY=.*/SERPER_API_KEY=$serper_key/" .env
            else
                sed -i "s/SERPER_API_KEY=.*/SERPER_API_KEY=$serper_key/" .env
            fi
        else
            echo "SERPER_API_KEY=$serper_key" >> .env
        fi
        echo -e "${GREEN}✓${NC} Serper API key saved!"
    fi
else
    echo -e "${YELLOW}ℹ${NC} Skipping Serper API key (you can add it later)"
fi

cd ..

echo ""
echo "================================================"
echo -e "${GREEN}  Configuration Complete!${NC}"
echo "================================================"
echo ""
echo "Your API keys are saved in: backend/.env"
echo ""
echo "Next steps:"
echo "  1. Run: ./start.sh"
echo "  2. Open: http://localhost:5173"
echo "  3. Generate your first report!"
echo ""
