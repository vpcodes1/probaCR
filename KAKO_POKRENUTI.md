# 🎯 KAKO POKRENUTI YUSEARCH - Za Potpune Početnike

## Video Tutorial (5 minuta)

👉 [Pogledaj video tutorial](link-to-video) - Sve pokazano korak po korak!

---

## 📋 Pre Nego Što Počneš

Trebaće ti **3 stvari**:

### 1. Python (Besplatan)
- **Preuzmi**: https://www.python.org/downloads/
- **Verzija**: 3.11 ili noviji
- **Windows**: Tokom instalacije OBAVEZNO štikliraj "Add Python to PATH"
- **Test**: Otvori terminal i kucaj `python --version`

### 2. Node.js (Besplatan)
- **Preuzmi**: https://nodejs.org/
- **Verzija**: 18 ili noviji
- **Instalacija**: Samo klikni Next, Next, Next
- **Test**: Otvori terminal i kucaj `node --version`

### 3. Anthropic API Ključ (Besplatan)
- **Registruj se**: https://console.anthropic.com/
- **Besplatno dobijaš**: $5 kredit (≈1,600 izveštaja!)
- **Vreme**: 2 minuta za registraciju

---

## 🚀 METOD 1: Najlakši (Automatski)

### Windows Korisnici:

1. **Preuzmi kod**
   - Klikni zeleno dugme "Code" → "Download ZIP"
   - Raspakuj ZIP negde (npr. Desktop)
   - Otvori folder

2. **Dvostruki klik na**: `setup.bat`
   - Sačekaj 2-3 minuta dok se instalira

3. **Dvostruki klik na**: `configure.bat`
   - Unesi Anthropic API ključ (copy-paste)
   - Pritisni Enter

4. **Dvostruki klik na**: `start.bat`
   - Gotovo! Aplikacija se otvara u browser-u

### Mac/Linux Korisnici:

1. **Otvori Terminal**

2. **Preuzmi kod**
   ```bash
   git clone <link-repozitorijuma>
   cd probaCR
   ```

3. **Pokreni automatsku instalaciju**
   ```bash
   chmod +x setup.sh configure.sh start.sh
   ./setup.sh
   ```

4. **Konfiguriši API ključ**
   ```bash
   ./configure.sh
   ```
   - Unesi Anthropic API ključ
   - Pritisni Enter

5. **Pokreni aplikaciju**
   ```bash
   ./start.sh
   ```

6. **Otvori browser**: http://localhost:5173

---

## 🐳 METOD 2: Docker (Za Napredne)

Ako znaš šta je Docker:

```bash
# 1. Konfiguriši API ključ
cd backend
cp .env.example .env
nano .env  # dodaj ANTHROPIC_API_KEY

# 2. Pokreni
cd ..
docker-compose up
```

Gotovo! Otvori http://localhost:5173

---

## 🌐 METOD 3: Cloud (Bez Instalacije!)

### Deploy na Railway (Backend)

1. Idi na https://railway.app
2. Klikni "Start New Project"
3. Izaberi "Deploy from GitHub"
4. Konektuj GitHub nalog
5. Izaberi ovaj repo
6. Dodaj Environment Variables:
   - `ANTHROPIC_API_KEY` = tvoj-ključ
7. Klikni "Deploy"
8. Sačekaj 2-3 minuta
9. Kopiraj URL (npr. `yusearch-backend.railway.app`)

### Deploy na Vercel (Frontend)

1. Idi na https://vercel.com
2. Klikni "New Project"
3. Import ovaj GitHub repo
4. Root Directory: `frontend`
5. Add Environment Variable:
   - `VITE_API_URL` = URL sa Railway
6. Klikni "Deploy"
7. Gotovo!

**Rezultat**: Online aplikacija bez instalacije! 🎉

---

## 📸 Korak-po-Korak Sa Slikama

### Kako Dobiti Anthropic API Ključ

#### Korak 1: Registracija
![Slika 1](screenshots/anthropic-signup.png)
- Idi na https://console.anthropic.com/
- Klikni "Sign Up"
- Unesi email i lozinku
- Potvrdi email

#### Korak 2: Napravi API Ključ
![Slika 2](screenshots/anthropic-create-key.png)
- Klikni na "API Keys" u meniju
- Klikni "Create Key"
- Daj mu ime (npr. "YUSEARCH")
- Klikni "Create"

#### Korak 3: Kopiraj Ključ
![Slika 3](screenshots/anthropic-copy-key.png)
- Ključ izgleda ovako: `sk-ant-api03-...`
- Klikni "Copy"
- ČUVAJ GA NEGDE SIGURNO!
- Nikad ne deli sa drugima

---

## ✅ Provera Da Li Radi

Nakon pokretanja:

### 1. Backend Test
Otvori u browser-u: http://localhost:8000/health

Treba da vidiš:
```json
{
  "status": "healthy",
  "service": "YUSEARCH"
}
```

### 2. Frontend Test
Otvori: http://localhost:5173

Treba da vidiš lepu stranicu sa "YUSEARCH" logom.

### 3. API Docs Test
Otvori: http://localhost:8000/docs

Treba da vidiš interaktivnu API dokumentaciju.

---

## 🎯 Prvi Izveštaj - Test

1. **Klikni**: "Start Your FREE Trial"

2. **Unesi podatke**:
   - **Prospect Name**: `Elon Musk`
   - **Company Name**: `Tesla`

3. **Klikni**: "Generate Report"

4. **Sačekaj**: 3-5 minuta (prati status)

5. **Rezultat**: Kompletan 12-stranični izveštaj!
   - Download PDF
   - Download Word
   - Sve informacije o Elon Musk-u

---

## ❌ Najčešći Problemi

### Problem 1: "Python nije pronađen"

**Rešenje**:
1. Instaliraj Python sa python.org
2. **Windows**: Tokom instalacije štikliraj "Add Python to PATH"
3. Restartuj računar
4. Otvori NOVI terminal
5. Kucaj: `python --version`

### Problem 2: "uvicorn: command not found"

**Rešenje**:
```bash
cd backend
source venv/bin/activate  # Mac/Linux
# ili
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Problem 3: "API key not configured"

**Rešenje**:
1. Proveri da si sačuvao `.env` fajl
2. Proveri da nema razmaka: `ANTHROPIC_API_KEY=sk-ant-...`
3. Proveri da ključ počinje sa `sk-ant-`
4. Restartuj aplikaciju

### Problem 4: "Port 8000 already in use"

**Rešenje**:
```bash
# Zaustavi prethodnu instancu
./stop.sh  # Mac/Linux
stop.bat   # Windows

# Ili ubij proces ručno:
# Mac/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <broj_procesa> /F
```

### Problem 5: Aplikacija se ne otvara u browser-u

**Rešenje**:
- Ručno otvori browser
- Idi na: http://localhost:5173
- Ako ne radi, proveri `frontend.log` za greške

---

## 📞 Još Uvek Ne Radi?

### Proveri Log Fajlove

```bash
# Backend log
cat backend.log

# Frontend log
cat frontend.log
```

### Test API Direktno

```bash
# Test health endpoint
curl http://localhost:8000/health

# Treba da vidiš: {"status":"healthy"}
```

### Potpuno Resetuj

```bash
# Zaustavi sve
./stop.sh  # ili stop.bat

# Obriši sve
rm -rf backend/venv
rm -rf frontend/node_modules

# Ponovo instaliraj
./setup.sh  # ili setup.bat
```

---

## 💡 Pro Tips

### Tip 1: Brže generisanje
- Dodaj Serper API ključ (bolji Google search)
- Registruj se na serper.dev (besplatno)

### Tip 2: Vidi šta se dešava
- Otvori terminal gde radi backend
- Vidi real-time log kako prikuplja podatke

### Tip 3: Testiraj sa poznatim ljudima
- Prvo testiraj sa poznatim CEO-ima (Elon Musk, Satya Nadella)
- Posle probaj sa svojim realnim klijentima

### Tip 4: Zaustavljanje
```bash
./stop.sh   # Mac/Linux
stop.bat    # Windows

# ili samo zatvori terminale
```

---

## 🎓 Naučio Si!

Sada znaš kako da:
- ✅ Instaliraš YUSEARCH
- ✅ Konfigurišeš API ključeve
- ✅ Pokreneš aplikaciju
- ✅ Generišeš izveštaje
- ✅ Rešavaš probleme

---

## 🚀 Sledeći Koraci

### Za Upotrebu:
- Generiši izveštaje za svoje klijente
- Eksportuj u PDF za sastanke
- Koristi conversation starters

### Za Prodaju:
- Deploy na cloud (Railway + Vercel)
- Dodaj svoj branding
- Naplaćuj $29-99/mesec

### Za Development:
- Promeni dizajn (TailwindCSS)
- Dodaj nove features
- Integriši sa CRM-om

---

## 📚 Dodatni Resursi

- **Detaljan Setup**: `SETUP_GUIDE.md`
- **API Dokumentacija**: http://localhost:8000/docs
- **Tehnički README**: `README.md`
- **Jednostavni README**: `README_SIMPLE.md`

---

**Napravljeno sa ❤️ uz pomoć AI**

_Ako nešto ne radi, pročitaj ponovo ovaj fajl polako. 99% problema je opisano ovde!_
