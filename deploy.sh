#!/bin/bash

# YUSEARCH - AUTOMATSKI CLOUD DEPLOYMENT
# Skripta koja automatski deploy-uje celu aplikaciju na cloud!

set -e

# Boje
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

clear

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║   🚀 YUSEARCH - AUTOMATSKI CLOUD DEPLOYMENT 🚀        ║"
echo "║                                                        ║"
echo "║   Ova skripta će automatski deploy-ovati              ║"
echo "║   tvoju aplikaciju na cloud!                          ║"
echo "║                                                        ║"
echo "║   Posle ovoga, dobijaš URL koji daješ klijentima!     ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Proveri Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js nije instaliran!${NC}"
    echo "Molim te instaliraj Node.js sa: https://nodejs.org/"
    exit 1
fi

echo -e "${GREEN}✓${NC} Node.js pronađen"

# Proveri npm
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ npm nije instaliran!${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} npm pronađen"
echo ""

# Izbor deployment platforme
echo -e "${BLUE}Izaberi deployment platformu:${NC}"
echo ""
echo "  1) Railway + Vercel (PREPORUČENO - potpuno besplatno)"
echo "  2) Render.com (sve na jednom mestu)"
echo "  3) Docker + bilo koji cloud"
echo ""
read -p "Izbor (1/2/3): " choice

case $choice in
    1)
        echo -e "${GREEN}Odabrao si: Railway + Vercel${NC}"
        PLATFORM="railway-vercel"
        ;;
    2)
        echo -e "${GREEN}Odabrao si: Render.com${NC}"
        PLATFORM="render"
        ;;
    3)
        echo -e "${GREEN}Odabrao si: Docker${NC}"
        PLATFORM="docker"
        ;;
    *)
        echo -e "${RED}Nevažeći izbor!${NC}"
        exit 1
        ;;
esac

echo ""

#############################################
# RAILWAY + VERCEL DEPLOYMENT
#############################################

if [ "$PLATFORM" = "railway-vercel" ]; then
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  RAILWAY + VERCEL DEPLOYMENT${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # Instaliraj Railway CLI
    echo -e "${BLUE}[1/5] Instaliram Railway CLI...${NC}"
    if ! command -v railway &> /dev/null; then
        npm install -g @railway/cli
        echo -e "${GREEN}✓${NC} Railway CLI instaliran"
    else
        echo -e "${GREEN}✓${NC} Railway CLI već instaliran"
    fi
    echo ""

    # Instaliraj Vercel CLI
    echo -e "${BLUE}[2/5] Instaliram Vercel CLI...${NC}"
    if ! command -v vercel &> /dev/null; then
        npm install -g vercel
        echo -e "${GREEN}✓${NC} Vercel CLI instaliran"
    else
        echo -e "${GREEN}✓${NC} Vercel CLI već instaliran"
    fi
    echo ""

    # Dobij API ključ
    echo -e "${BLUE}[3/5] Konfiguracija API ključeva...${NC}"
    echo ""
    echo -e "${YELLOW}Trebaš Anthropic API ključ!${NC}"
    echo "Ako nemaš, registruj se ovde: https://console.anthropic.com/"
    echo ""
    read -p "Unesi Anthropic API ključ: " ANTHROPIC_KEY
    echo ""

    # Backend deployment na Railway
    echo -e "${BLUE}[4/5] Deploy-ujem backend na Railway...${NC}"
    echo ""
    echo -e "${YELLOW}Otvaricu browser za Railway login...${NC}"
    echo "Molim te uloguj se u Railway"
    echo ""

    cd backend

    # Napravi .env za Railway
    cat > .env << EOF
ANTHROPIC_API_KEY=$ANTHROPIC_KEY
SECRET_KEY=$(openssl rand -hex 32)
ALLOWED_ORIGINS=*
DATABASE_URL=sqlite+aiosqlite:///./yusearch.db
EOF

    # Railway init i deploy
    railway login
    railway init
    railway up

    # Dobij Railway URL
    BACKEND_URL=$(railway status --json | grep -o '"url":"[^"]*' | cut -d'"' -f4)

    echo ""
    echo -e "${GREEN}✓${NC} Backend deploy-ovan na: ${CYAN}$BACKEND_URL${NC}"
    echo ""

    cd ..

    # Frontend deployment na Vercel
    echo -e "${BLUE}[5/5] Deploy-ujem frontend na Vercel...${NC}"
    echo ""
    echo -e "${YELLOW}Otvaricu browser za Vercel login...${NC}"
    echo "Molim te uloguj se u Vercel"
    echo ""

    cd frontend

    # Napravi .env za Vercel
    cat > .env.production << EOF
VITE_API_URL=$BACKEND_URL
EOF

    # Vercel deploy
    vercel login
    vercel --prod

    # Dobij Vercel URL
    FRONTEND_URL=$(vercel ls --json | head -1 | grep -o '"url":"[^"]*' | cut -d'"' -f4)

    cd ..

    echo ""
    echo -e "${GREEN}✓${NC} Frontend deploy-ovan na: ${CYAN}https://$FRONTEND_URL${NC}"
    echo ""

    # Update Railway CORS
    echo -e "${BLUE}Ažuriram CORS postavke...${NC}"
    cd backend
    railway variables --set ALLOWED_ORIGINS="https://$FRONTEND_URL"
    cd ..

    # GOTOVO!
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}  🎉 DEPLOYMENT ZAVRŠEN! 🎉${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${YELLOW}Tvoja aplikacija je LIVE na:${NC}"
    echo ""
    echo -e "  ${MAGENTA}Frontend:${NC} ${CYAN}https://$FRONTEND_URL${NC}"
    echo -e "  ${MAGENTA}Backend:${NC}  ${CYAN}$BACKEND_URL${NC}"
    echo ""
    echo -e "${YELLOW}Daješ ovaj link klijentima:${NC}"
    echo -e "  ${GREEN}➜  https://$FRONTEND_URL${NC}"
    echo ""
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}Čuvaj ove informacije:${NC}"

    # Sačuvaj deployment info
    cat > deployment-info.txt << EOF
YUSEARCH Deployment Info
========================

Frontend URL: https://$FRONTEND_URL
Backend URL: $BACKEND_URL

Deployed: $(date)

Daj ovaj URL klijentima: https://$FRONTEND_URL

Kako da ažuriraš:
- Backend: cd backend && railway up
- Frontend: cd frontend && vercel --prod
EOF

    echo -e "${GREEN}✓${NC} Info sačuvan u: ${CYAN}deployment-info.txt${NC}"
    echo ""

fi

#############################################
# RENDER.COM DEPLOYMENT
#############################################

if [ "$PLATFORM" = "render" ]; then
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  RENDER.COM DEPLOYMENT${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    echo -e "${BLUE}Za Render.com deployment:${NC}"
    echo ""
    echo "1. Idi na: ${CYAN}https://render.com${NC}"
    echo "2. Klikni: ${GREEN}New → Blueprint${NC}"
    echo "3. Connectuj svoj GitHub repo"
    echo "4. Izaberi fajl: ${YELLOW}render.yaml${NC}"
    echo "5. Dodaj Environment Variable:"
    echo "   ${MAGENTA}ANTHROPIC_API_KEY${NC} = tvoj-api-kljuc"
    echo "6. Klikni: ${GREEN}Apply${NC}"
    echo ""
    echo -e "${YELLOW}Otvaricu browser...${NC}"

    if command -v xdg-open &> /dev/null; then
        xdg-open "https://dashboard.render.com/select-repo?type=blueprint" &> /dev/null
    elif command -v open &> /dev/null; then
        open "https://dashboard.render.com/select-repo?type=blueprint" &> /dev/null
    fi

    echo ""
    echo "Kada deployment završi, dobijaš URL!"
    echo ""
fi

#############################################
# DOCKER DEPLOYMENT
#############################################

if [ "$PLATFORM" = "docker" ]; then
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}  DOCKER DEPLOYMENT${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""

    # Proveri Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker nije instaliran!${NC}"
        echo "Instaliraj Docker sa: https://www.docker.com/get-started"
        exit 1
    fi

    echo -e "${GREEN}✓${NC} Docker pronađen"
    echo ""

    # Dobij API ključ
    echo -e "${BLUE}Konfiguracija...${NC}"
    echo ""
    read -p "Unesi Anthropic API ključ: " ANTHROPIC_KEY
    echo ""

    # Napravi .env
    cd backend
    cat > .env << EOF
ANTHROPIC_API_KEY=$ANTHROPIC_KEY
SECRET_KEY=$(openssl rand -hex 32)
ALLOWED_ORIGINS=*
DATABASE_URL=sqlite+aiosqlite:///./yusearch.db
EOF
    cd ..

    # Build Docker images
    echo -e "${BLUE}Building Docker images...${NC}"
    docker-compose build

    echo ""
    echo -e "${GREEN}✓${NC} Docker images built!"
    echo ""
    echo -e "${YELLOW}Za pokretanje lokalno:${NC}"
    echo "  ${CYAN}docker-compose up${NC}"
    echo ""
    echo -e "${YELLOW}Za deploy na cloud:${NC}"
    echo ""
    echo "1. ${BLUE}DigitalOcean App Platform:${NC}"
    echo "   - Idi na: https://cloud.digitalocean.com/apps"
    echo "   - Klikni: Create App"
    echo "   - Izaberi Docker Hub ili GitHub"
    echo ""
    echo "2. ${BLUE}AWS ECS:${NC}"
    echo "   - Push image na ECR"
    echo "   - Deploy na ECS"
    echo ""
    echo "3. ${BLUE}Google Cloud Run:${NC}"
    echo "   - ${CYAN}gcloud run deploy --image ...${NC}"
    echo ""
fi

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  DEPLOYMENT PROCESS ZAVRŠEN!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
