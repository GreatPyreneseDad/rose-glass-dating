# Deployment Guide - Rose Glass Dating

Complete guide for deploying the Rose Glass Dating application to production.

## Overview

The application consists of:
- **Backend**: FastAPI (Python) - Railway/Render
- **Frontend**: Next.js (TypeScript) - Vercel
- **Database**: Supabase (PostgreSQL)
- **Auth**: Clerk (Optional for MVP)
- **Payments**: Stripe (Optional for MVP)

## Prerequisites

- [ ] Anthropic API key ($5 credit minimum)
- [ ] Supabase account (free tier works)
- [ ] Railway/Render account (free tier works)
- [ ] Vercel account (free tier works)
- [ ] Domain name (optional)

## Step 1: Database Setup (Supabase)

### 1.1 Create Project

1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Choose region closest to your users
4. Set strong database password
5. Wait for provisioning (~2 minutes)

### 1.2 Run Migrations

1. Go to **SQL Editor** in Supabase dashboard
2. Create new query
3. Copy and run each migration file in order:

**Migration 001 - Users:**
```sql
-- Paste contents of supabase/migrations/001_users.sql
```

**Migration 002 - Analyses:**
```sql
-- Paste contents of supabase/migrations/002_analyses.sql
```

**Migration 003 - Transactions:**
```sql
-- Paste contents of supabase/migrations/003_transactions.sql
```

4. Verify tables created in **Table Editor**

### 1.3 Get Connection Details

1. Go to **Project Settings** > **API**
2. Copy:
   - **Project URL** (`https://xxx.supabase.co`)
   - **Service Role Key** (secret, for backend only)
3. Save these for backend deployment

## Step 2: Backend Deployment (Railway)

### 2.1 Create Railway Project

1. Go to [railway.app](https://railway.app)
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Connect your `rose-glass-dating` repository
5. Select **backend** as root directory

### 2.2 Configure Environment Variables

In Railway project settings, add:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJ...

# App Configuration
ENVIRONMENT=production
BACKEND_URL=https://your-backend.up.railway.app
APP_URL=https://your-frontend.vercel.app

# CORS (update after frontend deployment)
CORS_ORIGINS=["https://your-frontend.vercel.app"]

# Optional (for full features)
CLERK_SECRET_KEY=sk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 2.3 Configure Build

Railway should auto-detect Python. If not, set:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Root Directory**: `backend`

### 2.4 Deploy

1. Click **Deploy**
2. Wait for build to complete (~2-3 minutes)
3. Check logs for errors
4. Visit generated URL to verify: `https://your-backend.up.railway.app/health`

Should return:
```json
{
  "status": "healthy",
  "environment": "production",
  "services": {
    "api": "ok",
    "claude": "configured",
    "database": "configured"
  }
}
```

### 2.5 Test API

```bash
curl -X POST https://your-backend.up.railway.app/api/analyze \
  -H "Authorization: dev_test_user" \
  -F "profile_images=@test.jpg"
```

## Step 3: Frontend Deployment (Vercel)

### 3.1 Create Vercel Project

1. Go to [vercel.com](https://vercel.com)
2. Click **Add New** > **Project**
3. Import `rose-glass-dating` repository
4. Configure project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 3.2 Configure Environment Variables

In Vercel project settings > **Environment Variables**, add:

```bash
# Backend API
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app

# App URL (update after deployment)
NEXT_PUBLIC_APP_URL=https://your-frontend.vercel.app

# Optional (for auth)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_...
CLERK_SECRET_KEY=sk_live_...
```

### 3.3 Deploy

1. Click **Deploy**
2. Wait for build (~1-2 minutes)
3. Visit generated URL
4. Should see landing page

### 3.4 Update CORS

Go back to Railway backend and update `CORS_ORIGINS`:
```bash
CORS_ORIGINS=["https://your-actual-frontend-url.vercel.app"]
```

Redeploy backend.

## Step 4: Verification

### 4.1 Health Checks

**Backend:**
```bash
curl https://your-backend.up.railway.app/health
```

**Frontend:**
Visit `https://your-frontend.vercel.app` - should load

### 4.2 Full Flow Test

1. Go to frontend URL
2. Click **Start Analysis**
3. Upload test dating profile screenshot
4. Should receive analysis within 30 seconds
5. Verify analysis contains:
   - Dimension table
   - Suggested opener
   - Rose Glass insights

### 4.3 Monitor Costs

**Anthropic Console:**
- Go to [console.anthropic.com](https://console.anthropic.com)
- Check **Usage** to see API costs
- Each analysis should be ~$0.01-0.02

**Railway:**
- Check **Metrics** for bandwidth/compute usage
- Free tier: 500 hours/month, $5 credit

**Vercel:**
- Check **Usage** for bandwidth
- Free tier: 100GB bandwidth/month

## Step 5: Custom Domain (Optional)

### 5.1 Frontend Domain

1. In Vercel project, go to **Settings** > **Domains**
2. Add your domain (e.g., `roseglass.dating`)
3. Add DNS records as shown:
   - Type: `A` or `CNAME`
   - Value: Vercel's IP/hostname
4. Wait for DNS propagation (~5-60 minutes)

### 5.2 Backend Domain

1. In Railway project, go to **Settings** > **Domains**
2. Add custom domain (e.g., `api.roseglass.dating`)
3. Add DNS record:
   - Type: `CNAME`
   - Value: Railway hostname
4. Update frontend `NEXT_PUBLIC_API_URL` in Vercel
5. Update backend `CORS_ORIGINS` in Railway

## Step 6: Production Hardening

### 6.1 Authentication (Clerk)

For production, replace `dev_test_user` auth:

1. Create Clerk application
2. Add environment variables to frontend and backend
3. Update `app/services/auth.py` to use real JWT verification
4. Redeploy

### 6.2 Rate Limiting

Add to backend `app/routers/analyze.py`:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/")
@limiter.limit("10/minute")
async def analyze_profile(...):
    ...
```

### 6.3 Monitoring

**Sentry** (Error Tracking):
```bash
pip install sentry-sdk
```

In `app/main.py`:
```python
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

**PostHog** (Analytics):
Add to frontend for usage tracking.

### 6.4 Backups

**Supabase:**
- Enable **Point-in-Time Recovery** (paid plan)
- Or configure daily backups

### 6.5 Security Headers

In `app/main.py`:
```python
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

## Cost Estimates

**Anthropic API:**
- 100 analyses/day = ~$2-4/day = $60-120/month
- 1000 analyses/day = ~$20-40/day = $600-1200/month

**Infrastructure:**
- Railway: Free tier → $20/month (hobby)
- Vercel: Free tier → $20/month (pro)
- Supabase: Free tier → $25/month (pro)

**Total Minimum:**
- Free tier: $0/month + API costs
- Paid tier: $65/month + API costs

## Troubleshooting

### Backend Won't Start

**Check logs:**
```bash
railway logs
```

**Common issues:**
- Missing `ANTHROPIC_API_KEY`
- Invalid Supabase credentials
- Port binding (use `$PORT` env variable)

### Frontend Build Fails

**Check build logs in Vercel**

**Common issues:**
- Missing environment variables
- TypeScript errors
- Node version mismatch

### CORS Errors

**Fix:**
1. Check `CORS_ORIGINS` in backend includes frontend URL
2. Ensure no trailing slash in URLs
3. Redeploy backend after changes

### Analysis Fails

**Check:**
1. Anthropic API key has credits
2. Image file size < 5MB
3. Backend logs for detailed error
4. Network tab in browser for 4xx/5xx errors

## Scaling Considerations

**For >1000 analyses/day:**

1. **Rate Limiting**: Protect against abuse
2. **CDN**: Add CloudFlare for static assets
3. **Database Connection Pooling**: Use Supabase connection pooling
4. **Caching**: Cache common profile patterns
5. **Queue System**: Celery + Redis for background processing

## Support

For issues:
1. Check logs (Railway, Vercel, Browser console)
2. Review [Troubleshooting](#troubleshooting) section
3. Open GitHub issue with:
   - Error message
   - Environment (backend/frontend)
   - Steps to reproduce

---

**Deployment Complete!** 🎉

Visit your site and start analyzing profiles through the Rose Glass.
