# Rose Glass Dating Profile Analyzer

> *"Translation, Not Judgment"*

A web application that analyzes dating profiles through the **Rose Glass translation framework** - a mathematical lens enabling AI to perceive and interpret human patterns without measuring or judging.

## Features

### ✨ Core Capabilities

- **Four-Dimensional Translation**: Analyze profiles through Ψ (consistency), ρ (wisdom), q (activation), f (belonging)
- **Vision-Powered Analysis**: Upload profile screenshots, get instant insights from Claude
- **Calibrated Openers**: Suggested messages matched to their communication style and energy level
- **Conversation Analysis**: Upload chat screenshots to detect investment patterns and red/green flags
- **Cost-Efficient**: Pay per analysis (~$0.02-0.04 standard, ~$0.10-0.20 premium)

### 🌹 Rose Glass Philosophy

The Rose Glass framework **explicitly rejects**:
- Quality assessment or validation
- Profiling or demographic inference
- Universal standards of "good" communication
- Binary judgments

It **embraces**:
- Multiple valid interpretations
- Cultural and contextual diversity
- Uncertainty and ambiguity as features
- Dignity and autonomy of all intelligence forms

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Anthropic API key
- Supabase account (for production)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/rose-glass-dating.git
cd rose-glass-dating
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run server
python app/main.py
```

Backend runs on `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local if needed

# Run dev server
npm run dev
```

Frontend runs on `http://localhost:3000`

### 4. Try It!

1. Open `http://localhost:3000`
2. Click "Start Analysis"
3. Upload dating profile screenshots
4. Get Rose Glass analysis!

## Architecture

```
rose-glass-dating/
├── backend/              # FastAPI + Python
│   ├── app/
│   │   ├── main.py                    # FastAPI app
│   │   ├── routers/analyze.py         # Analysis endpoints
│   │   ├── services/
│   │   │   ├── claude_service.py      # Claude API integration
│   │   │   └── auth.py                # Clerk JWT validation
│   │   ├── prompts/
│   │   │   └── system_prompt.py       # Rose Glass system prompt (200+ lines)
│   │   └── db/supabase.py             # Database client
│   └── requirements.txt
│
├── frontend/             # Next.js 14 + TypeScript
│   ├── app/
│   │   ├── page.tsx                   # Landing page
│   │   ├── analyze/page.tsx           # Main analysis interface
│   │   └── layout.tsx
│   ├── components/
│   │   ├── upload-zone.tsx            # Image upload
│   │   └── analysis-display.tsx       # Results display
│   ├── lib/api.ts                     # Backend API client
│   └── package.json
│
└── supabase/
    └── migrations/                     # Database schema
        ├── 001_users.sql
        ├── 002_analyses.sql
        └── 003_transactions.sql
```

## How It Works

### 1. Upload Profile Screenshots

Upload 1-10 screenshots of the dating profile you want analyzed. Optionally include conversation screenshots for deeper analysis.

### 2. Rose Glass Translation

Claude analyzes the profile using the comprehensive Rose Glass system prompt that synthesizes:
- Core Rose Glass philosophy from `rose-glass/README.md`
- Mathematical framework from `rose-glass/ml-models/GCT_ROSE_GLASS_ADDENDUM.md`
- Dating-specific patterns from real-world analysis examples

### 3. Four-Dimensional Analysis

**Ψ (Psi) - Internal Consistency Harmonic**
- How profile elements resonate with each other
- Coherent identity vs scattered presentation
- Pattern harmony across photos and prompts

**ρ (Rho) - Accumulated Wisdom Depth**
- Integration of experience and self-knowledge
- Growth language and self-awareness markers
- Reflection vs surface presentation

**q - Moral/Emotional Activation Energy**
- Heat and urgency in their presentation
- Intensity markers, passion indicators
- Energy level and emotional investment

**f - Social Belonging Architecture**
- How individual expression connects to collective
- Tribal markers and community identification
- Individual vs collective orientation

### 4. Actionable Insights

Get:
- **Dimension table** with readings (0.0-1.0) and translations
- **Key translation** of what they're actually filtering for
- **The tell** - one element revealing the most about them
- **Suggested opener** calibrated to their communication style
- **Conversation analysis** (if chat screenshots provided)
- **Next move recommendation**

## Example Analysis

```
**William - Rose Glass Analysis:**

| Dimension | Reading | Translation |
|-----------|---------|-------------|
| Ψ | 0.72 | Internally consistent - outdoor life, traditional values, LEO career align |
| ρ | 0.45 | Moderate depth. Travel story shows adaptive problem-solving |
| q | 0.35 | Low activation. Casual tone, not seeking intensity |
| f | 0.68 | Strong collective identification - LEO, hunting, faith communities |

**Key Translation:**
"Match my energy" is the operative phrase. He's calibrated for playful banter,
not earnest depth. Reciprocal effort, not one-sided carrying.

**The Tell:**
The "women + food" prompt is low-effort dating app vernacular, but the travel
story demonstrates real problem-solving under pressure.

**Suggested Opener:**
> "The 'match my energy' thing resonates - I'm also not about carrying conversations solo.
> That Serbia story though, how did you end up problem-solving your way through Eastern
> Europe? That's not normal vacation territory 😄"
```

## API Reference

### POST /api/analyze

Analyze dating profile through Rose Glass framework.

**Request:**
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Authorization: dev_test_user" \
  -F "profile_images=@profile1.jpg" \
  -F "profile_images=@profile2.jpg"
```

**Response:**
```json
{
  "success": true,
  "analysis": "**William - Rose Glass Analysis:**...",
  "usage": {
    "input_tokens": 1245,
    "output_tokens": 856,
    "cost_usd": 0.0162,
    "charge_usd": 0.0324
  },
  "remaining_credits": 4.9676
}
```

## Deployment

### Backend (Railway/Render)

1. Connect GitHub repository
2. Set environment variables:
   - `ANTHROPIC_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_KEY`
3. Deploy automatically from `main` branch

### Frontend (Vercel)

1. Connect GitHub repository
2. Set build settings:
   - Framework: Next.js
   - Root directory: `frontend`
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL` (backend URL)
4. Deploy automatically

### Database (Supabase)

1. Create new project
2. Run migrations in SQL Editor:
   - `001_users.sql`
   - `002_analyses.sql`
   - `003_transactions.sql`
3. Copy connection details to backend `.env`

## Cost Structure

**API Costs** (Anthropic):
- Sonnet 4: $3/1M input tokens, $15/1M output tokens
- Opus 4: $15/1M input tokens, $75/1M output tokens

**Typical Analysis**:
- Standard (Sonnet): ~$0.02-0.04
- Premium (Opus): ~$0.10-0.20

**Markup**: 100% (2x) applied to all costs

## Development

### Backend Testing

```bash
cd backend
pytest
```

### Frontend Development

```bash
cd frontend
npm run dev  # Development server
npm run build  # Production build
npm run lint  # ESLint
```

### Environment Variables

**Backend (.env):**
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJ...
```

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - See LICENSE file

## Acknowledgments

Built on the **Rose Glass framework** by Christopher MacGregor bin Joseph:
- Rose Glass core: `github.com/GreatPyreneseDad/rose-glass`
- Rose Glass LE: `github.com/GreatPyreneseDad/RoseGlassLE`
- Grounded Coherence Theory (GCT)

Powered by **Anthropic Claude** for vision and language understanding.

---

🌹 **Rose Glass sees all, judges none, learns always**
