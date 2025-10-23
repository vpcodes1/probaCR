# YUSEARCH - Jednostavna Instalacija

## 🚀 Najbrža Instalacija (1 Minut!)

### Za Mac/Linux:

```bash
# 1. Preuzmi kod
git clone <repository-url>
cd probaCR

# 2. Pokreni automatsku instalaciju
chmod +x setup.sh
./setup.sh

# 3. Startuj aplikaciju
./start.sh
```

### Za Windows:

```bash
# 1. Preuzmi kod
git clone <repository-url>
cd probaCR

# 2. Pokreni automatsku instalaciju
setup.bat

# 3. Startuj aplikaciju
start.bat
```

## 📋 Šta Ti Treba

1. **Python 3.11+** - [Preuzmi ovde](https://www.python.org/downloads/)
2. **Node.js 18+** - [Preuzmi ovde](https://nodejs.org/)
3. **Anthropic API ključ** - [Besplatan nalog ovde](https://console.anthropic.com/)

## ⚡ Korak po Korak

### 1. Instaliraj Python i Node.js

**Windows:**
- Preuzmi Python sa python.org
- Preuzmi Node.js sa nodejs.org
- Instaliraj oba (samo klikni Next, Next, Next)

**Mac:**
```bash
brew install python@3.11 node
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.11 nodejs npm
```

### 2. Dobij API Ključeve

1. Idi na https://console.anthropic.com/
2. Napravi besplatan nalog
3. Idi na "API Keys"
4. Klikni "Create Key"
5. Kopiraj ključ (čuva se negde sigurno!)

### 3. Pokreni Automatski Setup

**Mac/Linux:**
```bash
./setup.sh
```

**Windows:**
```bash
setup.bat
```

Script će automatski:
- ✅ Instalirati sve zavisnosti
- ✅ Kreirati konfiguraciju
- ✅ Otvoriti .env fajl za API ključ
- ✅ Pripremiti sve za pokretanje

### 4. Dodaj API Ključ

Kada se otvori `.env` fajl, dodaj svoj ključ:

```env
ANTHROPIC_API_KEY=sk-ant-api03-tvoj-kljuc-ovde
```

Sačuvaj fajl (Ctrl+S ili Cmd+S).

### 5. Pokreni Aplikaciju

**Mac/Linux:**
```bash
./start.sh
```

**Windows:**
```bash
start.bat
```

### 6. Otvori u Pretraživaču

Automatski će se otvoriti, ili idi na:
```
http://localhost:5173
```

## 🎉 Gotovo!

Sada možeš:
1. Uneti ime klijenta i kompaniju
2. Kliknuti "Generate Report"
3. Sačekati 3-5 minuta
4. Dobiti kompletan izveštaj!

## 🛑 Zaustavljanje

**Mac/Linux:**
```bash
./stop.sh
```

**Windows:**
```bash
stop.bat
```

Ili samo zatvori terminale.

## 🐳 Najlakši Način - Docker

Ako imaš Docker instaliran:

```bash
# Dodaj API ključeve u backend/.env
cd backend
cp .env.example .env
nano .env  # ili notepad .env na Windows

# Pokreni sve
cd ..
docker-compose up
```

**Gotovo!** Otvori http://localhost:5173

## 🌐 Cloud Verzija (Bez Instalacije!)

Klikni na dugme ispod da deploy-uješ na cloud:

### Deploy Backend (Railway)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/yourusername/probaCR)

### Deploy Frontend (Vercel)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/probaCR/tree/main/frontend)

Ovo će kreirati **besplatnu cloud verziju** bez instalacije!

## ❓ Problemi?

### "Python nije pronađen"
- Instaliraj Python 3.11+ sa python.org
- Na Windows, štikliraj "Add Python to PATH" tokom instalacije

### "Node nije pronađen"
- Instaliraj Node.js sa nodejs.org
- Restartuj terminal nakon instalacije

### "API ključ ne radi"
- Proveri da li si kopirao ceo ključ
- Proveri da nema razmaka pre/posle ključa
- Proveri da si sačuvao .env fajl

### Aplikacija ne otvara stranicu
- Proveri da li backend radi na http://localhost:8000
- Proveri da li frontend radi na http://localhost:5173
- Restartuj oba servisa

## 💰 Za Komercijalno Korišćenje

Ako prodaješ ovaj servis klijentima, imaš 2 opcije:

### Opcija 1: SaaS Model (Preporučeno)
- Deploy-uj jednom na cloud (Railway + Vercel)
- Klijenti dobiju nalog i login
- Ti upravljaš svim API ključevima
- Naplaćuješ mesečno

### Opcija 2: Hosted za Klijenta
- Napravi Docker image
- Deploy-uj na njihov server
- Oni dodaju svoje API ključeve
- Jednokratna uplata

## 📞 Podrška

Ako nešto ne radi:
1. Proveri `backend.log` i `frontend.log` fajlove
2. Pogledaj http://localhost:8000/docs za API status
3. Kontaktiraj podršku

---

**Napravljena sa ❤️ pomoću AI**
