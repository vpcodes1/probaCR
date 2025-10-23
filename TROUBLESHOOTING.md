# 🐛 YUSEARCH - TROUBLESHOOTING GUIDE

## Quick Diagnostic Steps

### Step 1: Test Backend Health

Open in browser:
```
https://probacr-1.onrender.com/health
```

**Expected Response:**
```json
{"status": "healthy", "service": "YUSEARCH"}
```

**If you see this → Backend is running ✅**
**If error/timeout → Backend is down ❌**

---

### Step 2: Test API Documentation

Open:
```
https://probacr-1.onrender.com/docs
```

**Expected:** Interactive API documentation (Swagger UI)
**If you see this → API routes are working ✅**

---

### Step 3: Check Browser Console

1. Open your frontend site
2. Press F12 (or right-click → Inspect)
3. Go to "Console" tab
4. Click "Generate Report"
5. **Copy ALL red error messages**

Common errors:
- `CORS error` → Need to fix ALLOWED_ORIGINS
- `500 Internal Server Error` → Backend crash
- `Network error` → Wrong API URL
- `Failed to fetch` → Backend is down

---

### Step 4: Check Network Tab

1. F12 → Network tab
2. Click "Generate Report"
3. Look for RED request to `/api/reports/generate`
4. Click on it
5. Go to "Response" tab
6. **Copy the error message**

---

### Step 5: Check Backend Logs (MOST IMPORTANT!)

In Render Dashboard:
1. Open your backend service
2. Click "Logs" tab
3. Try to generate report
4. **Watch logs in real-time**
5. **Copy last 30 lines**

Look for:
- `ANTHROPIC_API_KEY not configured`
- `ModuleNotFoundError`
- `ImportError`
- Any red ERROR messages

---

## Common Issues & Fixes

### Issue 1: CORS Error

**Browser Console shows:**
```
Access to fetch at 'https://probacr-1.onrender.com' from origin 'https://your-frontend.vercel.app'
has been blocked by CORS policy
```

**Fix:** In Render → Environment Variables
```
ALLOWED_ORIGINS = *
```
Save → Wait for redeploy

---

### Issue 2: API Key Missing

**Backend Logs show:**
```
Anthropic API key not configured
```

**Fix:** In Render → Environment Variables
```
ANTHROPIC_API_KEY = sk-ant-api03-your-key-here
```
Save → Wait for redeploy

---

### Issue 3: Wrong API URL

**Browser Console shows:**
```
POST https://wrong-url/api/reports/generate 404 (Not Found)
```

**Fix:** In Vercel → Settings → Environment Variables
```
VITE_API_URL = https://probacr-1.onrender.com
```
Save → Redeploy frontend

---

### Issue 4: Backend Sleeping (Render Free Tier)

**Symptoms:** First request takes 30+ seconds or times out

**Why:** Render free tier sleeps after 15 minutes of inactivity

**Fix:**
- Wait 30-60 seconds for backend to wake up
- Try again
- OR upgrade to paid tier ($7/month for always-on)

---

### Issue 5: Module Not Found

**Backend Logs show:**
```
ModuleNotFoundError: No module named 'anthropic'
```

**Fix:** requirements.txt not properly installed
- Check build logs in Render
- Ensure requirements.txt is in backend/ folder
- Redeploy

---

## Environment Variables Checklist

In **Render Backend Service** → Settings → Environment:

```
✓ ANTHROPIC_API_KEY = sk-ant-api03-...
✓ ALLOWED_ORIGINS = *
✓ DATABASE_URL = sqlite+aiosqlite:///./yusearch.db
✓ SECRET_KEY = any-random-string-here
```

In **Vercel Frontend** → Settings → Environment Variables:

```
✓ VITE_API_URL = https://probacr-1.onrender.com
```

---

## Debug Checklist

Run through this:

```
☐ Backend /health returns 200 OK
☐ Backend /docs shows Swagger UI
☐ All 4 env variables set in Render
☐ Backend redeployed after adding env vars
☐ VITE_API_URL set in Vercel
☐ Frontend redeployed after setting VITE_API_URL
☐ Browser console shows NO CORS errors
☐ Backend logs show NO errors
```

---

## Get Help

If still not working, provide:

1. **Backend /health response** (screenshot or text)
2. **Browser console errors** (F12 → Console → copy all red text)
3. **Backend logs** (Render → Logs → copy last 30 lines)
4. **Environment variables list** (just names, not values)

With this info, we can fix it immediately!

---

## Quick Test

Try this API call directly in browser:

```
https://probacr-1.onrender.com/docs#/reports/generate_report_api_reports_generate_post
```

1. Click "Try it out"
2. Enter:
```json
{
  "prospect_name": "Test User",
  "company_name": "Test Company"
}
```
3. Click "Execute"

**What happens?**
- 200 OK → API works, problem is in frontend
- 500 Error → Check error message, problem is in backend
- CORS error → Need to fix ALLOWED_ORIGINS
