# Rose Glass Dating Backend

FastAPI backend for dating profile analysis using the Rose Glass translation framework.

## Features

- ✅ Claude vision API integration for profile analysis
- ✅ Rose Glass four-dimensional translation (Ψ, ρ, q, f)
- ✅ Cost tracking with 100% markup
- ✅ Supabase database integration
- ✅ Clerk authentication
- ✅ Profile + conversation analysis

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in:

```bash
# Required
ANTHROPIC_API_KEY=sk-ant-api03-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJ...

# For production
CLERK_SECRET_KEY=sk_live_...
STRIPE_SECRET_KEY=sk_live_...
```

### 3. Run Database Migrations

In Supabase dashboard:
1. Go to SQL Editor
2. Run each migration file in order:
   - `001_users.sql`
   - `002_analyses.sql`
   - `003_transactions.sql`

### 4. Start Server

```bash
# Development
python app/main.py

# Or with uvicorn
uvicorn app.main:app --reload
```

Server runs on `http://localhost:8000`

API docs at `http://localhost:8000/docs`

## API Endpoints

### POST /api/analyze

Analyze dating profile through Rose Glass framework.

**Request:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Authorization: Bearer <clerk_jwt>" \
  -F "profile_images=@profile1.jpg" \
  -F "profile_images=@profile2.jpg" \
  -F "user_context=Looking for long-term relationship" \
  -F "use_premium=false"
```

**Response:**
```json
{
  "success": true,
  "analysis": "**William - Rose Glass Analysis:**\n\n| Dimension | Reading | Translation |...",
  "usage": {
    "input_tokens": 1245,
    "output_tokens": 856,
    "cost_usd": 0.0162,
    "charge_usd": 0.0324
  },
  "remaining_credits": 4.9676,
  "analysis_id": "uuid..."
}
```

### GET /api/analyze/history

Get user's analysis history.

```bash
curl http://localhost:8000/api/analyze/history?limit=20 \
  -H "Authorization: Bearer <clerk_jwt>"
```

### GET /api/analyze/credits

Get user's current credit balance.

```bash
curl http://localhost:8000/api/analyze/credits \
  -H "Authorization: Bearer <clerk_jwt>"
```

## Development Testing

For development without full auth setup, use test user:

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Authorization: dev_test_user" \
  -F "profile_images=@test.jpg"
```

## Architecture

```
backend/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Environment settings
│   ├── routers/
│   │   └── analyze.py       # Analysis endpoints
│   ├── services/
│   │   ├── claude_service.py   # Claude API integration
│   │   └── auth.py          # Clerk JWT validation
│   ├── models/
│   │   └── analysis.py      # Pydantic models
│   ├── db/
│   │   └── supabase.py      # Database client
│   └── prompts/
│       └── system_prompt.py # Rose Glass system prompt
├── requirements.txt
└── .env
```

## System Prompt

The Rose Glass analysis is powered by a comprehensive system prompt that synthesizes:

1. **Core Philosophy** from `rose-glass/README.md`
2. **Mathematical Framework** from `rose-glass/ml-models/GCT_ROSE_GLASS_ADDENDUM.md`
3. **Dating-Specific Patterns** from real-world analysis examples

See `app/prompts/system_prompt.py` for the complete prompt (200+ lines).

## Cost Calculation

**Sonnet 4** (default):
- Input: $3/1M tokens
- Output: $15/1M tokens
- Typical profile analysis: $0.02-0.04

**Opus 4** (premium):
- Input: $15/1M tokens
- Output: $75/1M tokens
- Typical profile analysis: $0.10-0.20

**Markup**: 100% (2x) applied to all costs

## Deployment

### Railway/Render

1. Connect repo
2. Set environment variables
3. Deploy automatically

### Docker

```bash
docker build -t rose-glass-backend .
docker run -p 8000:8000 --env-file .env rose-glass-backend
```

## Testing

```bash
pytest
```

## License

MIT License - See LICENSE file
