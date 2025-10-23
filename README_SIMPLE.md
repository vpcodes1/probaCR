# 🎯 YUSEARCH - AI za Prodaju

**Generiši kompletan izveštaj o klijentu za 5 minuta umesto 2+ sata.**

## 🚀 Najbrži Start

### Windows:
```bash
setup.bat
start.bat
```

### Mac/Linux:
```bash
chmod +x setup.sh && ./setup.sh
./start.sh
```

### Docker (najlakše):
```bash
docker-compose up
```

Otvori: **http://localhost:5173**

## ⚡ Šta Dobijaš

Unesi **ime klijenta** i **kompaniju**, sačekaj 5 minuta i dobijaš:

✅ **Conversation Starters** - 3-5 savršenih uvoda u razgovor
✅ **Talking Points** - 8-10 relevantnih tema za diskusiju
✅ **Personality Analysis** - Kako komunicira, kako mu prići
✅ **Company Background** - Finansiranje, veličina, industrija
✅ **Recent News** - Najnovija dešavanja u kompaniji
✅ **Recommended Approach** - Strategija za sastanak

Sve u **PDF** i **Word** formatu!

## 📋 Šta Ti Treba

1. **Python 3.11+** → https://python.org
2. **Node.js 18+** → https://nodejs.org
3. **Anthropic API ključ** (besplatan) → https://console.anthropic.com

## 📖 Instalacija - 4 Koraka

### 1. Preuzmi kod
```bash
git clone <repo-url>
cd probaCR
```

### 2. Automatski setup
```bash
./setup.sh          # Mac/Linux
setup.bat           # Windows
```

### 3. Dodaj API ključ
Otvori `backend/.env` i dodaj:
```env
ANTHROPIC_API_KEY=tvoj-kljuc-ovde
```

### 4. Pokreni
```bash
./start.sh          # Mac/Linux
start.bat           # Windows
```

## 🌐 Cloud Verzija (Bez Instalacije)

Najlakši način - deploy na cloud za **besplatno**:

**Korak 1: Backend na Railway**
1. Idi na https://railway.app
2. Klikni "New Project" → "Deploy from GitHub"
3. Izaberi ovaj repo
4. Dodaj environment varijable:
   - `ANTHROPIC_API_KEY` = tvoj ključ
5. Deploy!

**Korak 2: Frontend na Vercel**
1. Idi na https://vercel.com
2. Klikni "New Project" → Import repo
3. Izaberi `frontend` folder
4. Deploy!

**Gotovo!** Imaš online verziju bez instalacije.

## 💡 Kako Funkcioniše

```
1. Unesi prospect → 2. AI prikuplja podatke → 3. AI analizira → 4. Generisan izveštaj
   (10 sekundi)        (2-3 minuta)              (1-2 minuta)      (PDF + Word)
```

**Sve automatski!**

## 🎯 Primer Upotrebe

```
Prospect: "Satya Nadella"
Company: "Microsoft"

[Klikni Generate Report]

... 5 minuta kasnije ...

✅ 12-stranični izveštaj sa:
   - Biografija i pozadina
   - 10 talking points
   - 5 conversation starters
   - Analiza ličnosti
   - Strategija pristupa
   - Novosti o Microsoft-u
   - PDF + Word download
```

## 💰 Prodaj Kao Servis

### Opcija 1: SaaS Model
- Ti deploy-uješ na cloud (jednom)
- Klijenti dobiju nalog
- Naplaćuješ $29-99/mesec
- Ti kontrolišeš API ključeve

### Opcija 2: Self-Hosted
- Instaliraš kod klijenta
- Oni dobiju celу aplikaciju
- Jednokratna naplata
- Oni kontrolišu svoje ključeve

### Opcija 3: White Label
- Menjaš branding
- Dodaješ svoj logo
- Prodaješ kao svoj proizvod

## 🛠️ Komande

```bash
# Startuj aplikaciju
./start.sh          # Mac/Linux
start.bat           # Windows

# Zaustavi aplikaciju
./stop.sh           # Mac/Linux
stop.sh             # Windows

# Proveri da li radi
http://localhost:8000/health

# Vidi API dokumentaciju
http://localhost:8000/docs
```

## 📊 Troškovi

**Besplatno:**
- Hosting na Railway: $5/mesec (ili besplatno sa limitima)
- Hosting na Vercel: Besplatno
- Anthropic API: $0.003 po zahtevu (≈ $0.30 za 100 izveštaja)

**Ukupno:** ≈ $5-10/mesec za neograničen broj korisnika!

## ❓ Česta Pitanja

**Q: Da li mogu da prodajem ovo klijentima?**
A: Da! Možeš da deploy-uješ i prodaješ kao servis.

**Q: Koliko košta pokretanje?**
A: ≈$5/mesec za hosting + $0.003 po izveštaju za AI.

**Q: Da li trebam znanje programiranja?**
A: Ne, sve je automatizovano. Samo pokreni skriptu.

**Q: Mogu li da promenim dizajn?**
A: Da, frontend je React - lako se menja.

**Q: Podržava li druge jezike?**
A: Da, AI može da generiše na srpskom, engleskom, itd.

**Q: Koliko brzo se generiše izveštaj?**
A: 3-5 minuta za kompletan izveštaj.

## 🔒 Sigurnost

- API ključevi se čuvaju u `.env` fajlu (nikad u kodu)
- Svi API pozivi su enkriptovani (HTTPS)
- Nema čuvanja osetljivih podataka
- Izveštaji se čuvaju lokalno (možeš da obrišeš)

## 📞 Podrška

**Problemi sa instalacijom?**
Pogledaj `INSTALL.md` za detaljne instrukcije.

**API greške?**
Proveri `backend.log` za detalje.

**Frontend ne radi?**
Proveri `frontend.log` za greške.

## 🎉 Brzi Testovi

Nakon instalacije, testaj:

```bash
# Test 1: Proveri backend
curl http://localhost:8000/health

# Test 2: Proveri API
open http://localhost:8000/docs

# Test 3: Otvori app
open http://localhost:5173
```

## 🚀 Production Ready

Aplikacija je spremna za produkciju:
- ✅ Async operacije za brzinu
- ✅ Error handling
- ✅ Logging
- ✅ Rate limiting
- ✅ CORS konfiguracija
- ✅ API dokumentacija
- ✅ Docker support
- ✅ Cloud deployment

## 📈 Roadmap

Planirane funkcionalnosti:
- [ ] LinkedIn integracija
- [ ] CRM integracija (Salesforce, HubSpot)
- [ ] Chrome extension
- [ ] Mobile app
- [ ] Team collaboration
- [ ] Analytics dashboard
- [ ] Multi-language support

---

**Napravljeno sa ❤️ koristeći:**
- Python + FastAPI
- React + TailwindCSS
- Anthropic Claude AI
- Docker

**Licenca:** Proprietary (možeš prodavati)
