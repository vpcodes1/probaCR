# B2B Hub - Platforma za Poslovno Umrežavanje

B2B Hub je potpuno funkcionalna web platforma koja omogućava firmama da pronađu transportere, dobavljače i druge poslovne partnere na jednom mestu.

## 🚀 Karakteristike

### Backend (Flask + Python)
- ✅ RESTful API
- ✅ SQLAlchemy ORM sa SQLite bazom podataka
- ✅ JWT autentifikacija
- ✅ Modeli za kompanije, oglase i poruke
- ✅ CRUD operacije za sve entitete
- ✅ Sistem pretrage i filtriranja
- ✅ Messaging sistem između kompanija

### Frontend (React + Vite + TailwindCSS)
- ✅ Moderna responsive UI
- ✅ React Router za navigaciju
- ✅ Registracija i autentifikacija korisnika
- ✅ Kreiranje i upravljanje oglasima
- ✅ Pretraga oglasa po kategorijama i lokaciji
- ✅ Profil kompanije
- ✅ Sistem poruka
- ✅ Mobilna optimizacija

## 📋 Kategorije

- 🚚 Transport i Logistika
- 📦 Dobavljači
- 🏭 Proizvodnja
- 💼 Poslovne Usluge
- 🏗️ Građevina
- 🛒 Trgovina
- 💻 IT i Tehnologija
- 📢 Marketing i PR
- 💰 Finansije i Računovodstvo
- 📋 Ostalo

## 🛠️ Instalacija i Pokretanje

### Preduslovi

- Python 3.8+
- Node.js 16+
- npm ili yarn

### Backend Setup

1. Pozicionirajte se u backend direktorijum:
```bash
cd backend
```

2. Instalirajte Python zavisnosti:
```bash
pip install -r requirements.txt
```

3. Pokrenite backend server:
```bash
python -m app.main
```

Backend će biti dostupan na `http://localhost:5000`

### Frontend Setup

1. Pozicionirajte se u frontend direktorijum:
```bash
cd frontend
```

2. Instalirajte npm zavisnosti:
```bash
npm install
```

3. Pokrenite development server:
```bash
npm run dev
```

Frontend će biti dostupan na `http://localhost:5173`

## 🔌 API Endpoints

### Autentifikacija
- `POST /api/auth/register` - Registracija nove kompanije
- `POST /api/auth/login` - Prijava
- `GET /api/auth/me` - Trenutni korisnik

### Oglasi
- `GET /api/listings` - Lista oglasa (sa filterima)
- `GET /api/listings/:id` - Detalji oglasa
- `POST /api/listings` - Kreiranje oglasa (zahteva autentifikaciju)
- `PUT /api/listings/:id` - Ažuriranje oglasa
- `DELETE /api/listings/:id` - Brisanje oglasa
- `GET /api/listings/my` - Moji oglasi
- `GET /api/listings/categories` - Lista kategorija

### Kompanije
- `GET /api/companies` - Lista kompanija
- `GET /api/companies/:id` - Detalji kompanije
- `PUT /api/companies/profile` - Ažuriranje profila

### Poruke
- `GET /api/messages` - Lista poruka
- `GET /api/messages/:id` - Detalji poruke
- `POST /api/messages` - Slanje poruke
- `PUT /api/messages/:id/read` - Označavanje kao pročitano
- `GET /api/messages/unread-count` - Broj nepročitanih

## 📊 Baza Podataka

SQLite baza podataka se automatski kreira pri prvom pokretanju backenda. Nalazi se u `backend/b2b_hub.db`

### Tabele:
- **companies** - Kompanije/korisnici
- **listings** - Oglasi
- **messages** - Poruke između kompanija

## 🎨 Frontend Struktura

```
frontend/src/
├── components/
│   ├── Navbar.jsx          # Navigacija
│   ├── Home.jsx            # Početna strana
│   ├── Login.jsx           # Prijava
│   ├── Register.jsx        # Registracija
│   ├── Listings.jsx        # Lista oglasa
│   ├── ListingDetail.jsx   # Detalji oglasa
│   ├── CreateListing.jsx   # Kreiranje oglasa
│   ├── MyListings.jsx      # Moji oglasi
│   ├── Messages.jsx        # Poruke
│   ├── Profile.jsx         # Profil
│   └── Companies.jsx       # Lista kompanija
├── utils/
│   └── api.js              # API helper funkcije
├── App.jsx                 # Glavna aplikacija
└── main.jsx               # Entry point
```

## 🔐 Autentifikacija

Sistem koristi JWT tokene za autentifikaciju. Token se čuva u localStorage i automatski se šalje sa svakim zahtevom.

## 💡 Korišćenje

1. **Registracija**: Kreirajte nalog za vašu kompaniju
2. **Pregledanje**: Pretražujte oglase i kompanije
3. **Postavljanje oglasa**: Postavite oglase za vaše usluge/proizvode
4. **Komunikacija**: Kontaktirajte kompanije putem poruka
5. **Upravljanje**: Upravljajte svojim oglasima i profilom

## 🚀 Production Deployment

### Backend
```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app.main:app
```

### Frontend
```bash
cd frontend
npm run build
# Serviranje dist/ foldera sa nginx ili drugim web serverom
```

## 🔧 Environment Variables

### Backend (.env)
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///b2b_hub.db
PORT=5000
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:5000
```

## 📝 Licenca

Ovaj projekat je kreiran za B2B Hub platformu.

## 👥 Podrška

Za pitanja i podršku, kontaktirajte tim B2B Hub-a.

---

**Napravljeno sa ❤️ za B2B zajednicu**
