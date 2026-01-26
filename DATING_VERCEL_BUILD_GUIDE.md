# Rose Glass Dating - Vercel Platform Build Guide
## Standalone Web Application for Dating Profile Analysis

**Date:** January 25, 2026  
**Goal:** Create a standalone Vercel-hosted platform where users can:
1. Upload dating profile screenshots for analysis
2. Upload conversation screenshots for investment pattern detection
3. Have conversations with Rose Glass about their dating situations
4. Follow the Two Hands Principle (perception → reflection → co-creation)

---

## WHAT EXISTS NOW

### Source Repository: `/Users/chris/rose-glass-dating`

**Current Architecture:**
- **Backend:** Python FastAPI (separate server required)
- **Frontend:** Next.js 14 + TypeScript
- **Database:** Supabase (for user credits/auth)

**Key Assets to Port:**
1. `backend/app/prompts/system_prompt.py` — 426 lines of Rose Glass Dating system prompt
2. `frontend/components/upload-zone.tsx` — Drag & drop image upload
3. `frontend/components/analysis-display.tsx` — Markdown rendering of analysis
4. `UNIVERSAL_UPDATE_TWO_HANDS.md` — Core philosophy (perception → reflection → co-creation)

**Problem:** Current architecture requires separate Python backend deployment.

**Solution:** Port to Next.js API routes for single Vercel deployment.

---

## TARGET ARCHITECTURE

```
roseglass-dating-platform/
├── src/
│   ├── lib/
│   │   ├── rose-glass-dating.ts          # System prompt + types
│   │   └── image-utils.ts                # Base64 conversion utilities
│   ├── components/
│   │   ├── UploadZone.tsx                # Screenshot upload
│   │   ├── AnalysisDisplay.tsx           # Markdown analysis rendering
│   │   ├── ReflectionScreen.tsx          # Two Hands: user input
│   │   ├── CoCreateScreen.tsx            # Two Hands: co-created response
│   │   └── ChatInterface.tsx             # Ongoing conversation
│   ├── app/
│   │   ├── page.tsx                      # Landing page
│   │   ├── analyze/
│   │   │   └── page.tsx                  # Main analysis flow
│   │   ├── chat/
│   │   │   └── page.tsx                  # Conversation mode
│   │   └── api/
│   │       ├── analyze/route.ts          # Profile analysis endpoint
│   │       ├── co-create/route.ts        # Response co-creation endpoint
│   │       └── chat/route.ts             # Ongoing conversation endpoint
│   └── styles/
│       └── globals.css
├── public/
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── .env.local
```

---

## CORE SYSTEM PROMPT

Port from `backend/app/prompts/system_prompt.py`:

### File: `src/lib/rose-glass-dating.ts`

```typescript
/**
 * Rose Glass Dating Profile Analyzer
 * 
 * Translation, Not Judgment
 * Two Hands Principle: Perception → Reflection → Co-Creation
 */

export const ROSE_GLASS_DATING_SYSTEM_PROMPT = `You are a dating profile analyst using the Rose Glass translation framework.

## Core Philosophy: Translation, Not Measurement

The Rose Glass is a mathematical lens enabling synthetic minds to perceive and interpret
patterns of organic intelligence. You do NOT measure or judge - you translate patterns
into actionable insights.

### What You Do NOT Do
- Judge profiles as "good" or "bad"
- Score attractiveness or compatibility
- Make deterministic predictions
- Impose universal standards
- Profile or infer identity
- Reduce human complexity to numbers

### What You DO
- Translate patterns you perceive into actionable insights
- Reveal multiple valid interpretations
- Identify what the person is actually filtering for (stated vs unstated)
- Calibrate suggested communication to their specific style
- Acknowledge uncertainty and multiplicity
- Respect the dignity of all communication forms

## The Four Dimensions of Translation

### Ψ (Psi) - Internal Consistency Harmonic
- How profile elements resonate with each other
- Contradictions between stated values and photo choices
- Coherent identity vs scattered presentation

### ρ (Rho) - Accumulated Wisdom Depth
- Integration of experience and self-knowledge
- Growth language ("I've learned...", "I used to...", "Now I...")
- Self-awareness markers vs surface-level descriptors

### q - Moral/Emotional Activation Energy
- Heat and urgency in their presentation
- Intensity markers (exclamation points, emphatic language)
- "lol" and softeners DAMPEN intensity

### f - Social Belonging Architecture
- Tribal markers (communities, faith, subcultures)
- Group photos vs solo presentation
- Individual vs collective orientation

## Critical Dating Profile Patterns

1. **Lead Photo Tell**: Silly/goofy photo first = filtering for humor appreciation
2. **Low-Effort Prompts**: Track if pattern holds across WHOLE profile
3. **"Match My Energy"**: Filter for reciprocity, playful banter not earnest depth
4. **Professional vs Casual Photos**: Reveals seriousness of intent
5. **What's NOT on Profile**: Intentional omissions matter

## Conversation Analysis (when screenshots provided)

### Investment Indicators
- Response time: Hours = normal, Days = low priority
- Response length: Match or exceed = high investment
- Questions asked: 0 = extraction, 2+ = genuine interest
- Thread continuation: Builds on topics = engaged

### Red Flags (Energy Extraction)
- Never asks questions but responds warmly
- Lots of "lol" dampening every sentence
- Brief responses to long messages

### Green Flags (Genuine Investment)
- Matches your energy level
- Builds on your threads with elaboration
- References specifics from your messages
- Creates opportunities to connect deeper

## Analysis Output Format

1. **Dimension Analysis Table** — Ψ, ρ, q, f with readings (0.0-1.0) and translations
2. **Key Translation** — What are they actually filtering for?
3. **The Tell** — The ONE element that reveals the most about them
4. **Conversation Analysis** — If chat screenshots provided
5. **Pattern Summary** — What you perceive, with uncertainty acknowledged

Remember: Translation, not judgment. Multiple valid interpretations exist.
`;

export const TWO_HANDS_REFLECTION_PROMPTS = {
  observation: "What do you notice about them? What stands out to you?",
  resonance: "What resonates with you? What feels relevant from your own life or experience?",
  expression: "What do you want to share about yourself? What's true for you here?",
  intent: "What are you hoping for in this connection? What matters to you?"
};

export const CO_CREATION_SYSTEM_PROMPT = `You are helping a user craft an authentic message.

You have two inputs:
1. Your Rose Glass analysis of the recipient (what you perceive about them)
2. The user's reflection (what they observe, what resonates, what they want to express)

Your job is to WEAVE these together:
- Calibrate to the recipient's communication style (from your analysis)
- Express what's genuinely true for the user (from their reflection)
- Create space for real connection, not just engagement

DO NOT:
- Generate generic "optimized" openers
- Replace the user's voice with performative text
- Maximize reply rates at the expense of authenticity
- Skip what the user said matters to them

DO:
- Honor what the user wants to express
- Match the recipient's energy level
- Reference something specific showing genuine attention
- Leave room for the conversation to breathe

The result should feel like the user's authentic voice, calibrated for clarity.
`;

// Types
export type RiskLevel = 'stable' | 'watch' | 'concern' | 'urgent';

export interface DimensionReading {
  dimension: string;
  symbol: string;
  value: number;
  translation: string;
}

export interface ProfileAnalysis {
  dimensions: DimensionReading[];
  keyTranslation: string;
  theTell: string;
  conversationAnalysis?: string;
  patternSummary: string;
  suggestedApproach?: string;
}

export interface UserReflection {
  observation: string;
  resonance: string;
  expression: string;
  intent: string;
}

export interface CoCreatedMessage {
  message: string;
  calibrationNotes: string;
  alternatives?: string[];
}
```

---

## IMAGE UPLOAD COMPONENT

### File: `src/components/UploadZone.tsx`

```typescript
'use client';

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';

interface UploadZoneProps {
  onImagesSelected: (files: File[]) => void;
  maxImages?: number;
  label?: string;
}

export function UploadZone({
  onImagesSelected,
  maxImages = 10,
  label = "Profile Screenshots"
}: UploadZoneProps) {
  const [images, setImages] = useState<File[]>([]);
  const [previews, setPreviews] = useState<string[]>([]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newImages = [...images, ...acceptedFiles].slice(0, maxImages);
    setImages(newImages);

    const newPreviews = newImages.map(file => URL.createObjectURL(file));
    setPreviews(prev => {
      prev.forEach(url => URL.revokeObjectURL(url));
      return newPreviews;
    });

    onImagesSelected(newImages);
  }, [images, maxImages, onImagesSelected]);

  const removeImage = (index: number) => {
    const newImages = images.filter((_, i) => i !== index);
    setImages(newImages);
    URL.revokeObjectURL(previews[index]);
    setPreviews(prev => prev.filter((_, i) => i !== index));
    onImagesSelected(newImages);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': ['.png', '.jpg', '.jpeg', '.webp'] },
    maxFiles: maxImages - images.length,
    disabled: images.length >= maxImages
  });

  return (
    <div className="space-y-4">
      <label className="text-sm font-medium text-gray-700">{label}</label>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive ? "border-rose-500 bg-rose-50" : "border-gray-300 hover:border-rose-400"}
          ${images.length >= maxImages && "opacity-50 cursor-not-allowed"}`}
      >
        <input {...getInputProps()} />
        <div className="mx-auto h-12 w-12 text-gray-400">📸</div>
        <p className="mt-2 text-sm text-gray-600">
          {isDragActive
            ? "Drop images here..."
            : `Drag & drop screenshots, or click to select (${images.length}/${maxImages})`}
        </p>
      </div>

      {previews.length > 0 && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {previews.map((preview, index) => (
            <div key={index} className="relative group">
              <img
                src={preview}
                alt={`Screenshot ${index + 1}`}
                className="w-full h-32 object-cover rounded-lg border"
              />
              <button
                onClick={() => removeImage(index)}
                className="absolute top-1 right-1 p-1 bg-red-500 text-white rounded-full 
                  opacity-0 group-hover:opacity-100 transition-opacity text-xs"
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

---

## API ROUTES

### File: `src/app/api/analyze/route.ts`

```typescript
import { NextRequest } from 'next/server';
import Anthropic from '@anthropic-ai/sdk';
import { ROSE_GLASS_DATING_SYSTEM_PROMPT } from '@/lib/rose-glass-dating';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    
    const profileImages = formData.getAll('profile_images') as File[];
    const conversationImages = formData.getAll('conversation_images') as File[];
    const userContext = formData.get('user_context') as string | null;
    
    if (profileImages.length === 0) {
      return Response.json({ error: 'At least one profile image required' }, { status: 400 });
    }
    
    // Convert images to base64
    const imageContents = await Promise.all(
      profileImages.map(async (file) => {
        const bytes = await file.arrayBuffer();
        const base64 = Buffer.from(bytes).toString('base64');
        const mediaType = file.type || 'image/png';
        return {
          type: 'image' as const,
          source: {
            type: 'base64' as const,
            media_type: mediaType,
            data: base64,
          },
        };
      })
    );
    
    // Add conversation images if provided
    let conversationContents: any[] = [];
    if (conversationImages.length > 0) {
      conversationContents = [
        { type: 'text', text: '\n---\n**CONVERSATION SCREENSHOTS:**\n' },
        ...(await Promise.all(
          conversationImages.map(async (file) => {
            const bytes = await file.arrayBuffer();
            const base64 = Buffer.from(bytes).toString('base64');
            return {
              type: 'image' as const,
              source: {
                type: 'base64' as const,
                media_type: file.type || 'image/png',
                data: base64,
              },
            };
          })
        )),
      ];
    }
    
    // Build analysis request
    let analysisRequest = `Analyze this dating profile through the Rose Glass framework.

${userContext ? `**User Context:** ${userContext}\n\n` : ''}

Provide:
1. **Dimension Analysis Table** — Ψ, ρ, q, f with readings (0.0-1.0) and translations
2. **Key Translation** — What are they actually filtering for? (2-3 sentences)
3. **The Tell** — The ONE element that reveals the most about them
${conversationImages.length > 0 ? '4. **Conversation Analysis** — Investment level, trajectory, red/green flags\n5. **Pattern Summary** — Overall read with uncertainty acknowledged' : '4. **Pattern Summary** — Overall read with uncertainty acknowledged'}

Remember: Translation, not judgment. Multiple valid interpretations exist.`;

    const content = [
      ...imageContents,
      ...conversationContents,
      { type: 'text' as const, text: analysisRequest },
    ];
    
    const startTime = Date.now();
    
    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 2500,
      system: ROSE_GLASS_DATING_SYSTEM_PROMPT,
      messages: [{ role: 'user', content }],
    });
    
    const responseTime = Date.now() - startTime;
    const textContent = response.content.find(block => block.type === 'text');
    const analysisText = textContent?.type === 'text' ? textContent.text : '';
    
    return Response.json({
      success: true,
      analysis: analysisText,
      metrics: {
        responseTime,
        inputTokens: response.usage.input_tokens,
        outputTokens: response.usage.output_tokens,
      },
    });
    
  } catch (error) {
    console.error('Analysis error:', error);
    return Response.json(
      { error: error instanceof Error ? error.message : 'Analysis failed' },
      { status: 500 }
    );
  }
}
```

### File: `src/app/api/co-create/route.ts`

```typescript
import { NextRequest } from 'next/server';
import Anthropic from '@anthropic-ai/sdk';
import { CO_CREATION_SYSTEM_PROMPT } from '@/lib/rose-glass-dating';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { analysis, reflection, recipientName } = body;
    
    if (!analysis || !reflection) {
      return Response.json({ error: 'Analysis and reflection required' }, { status: 400 });
    }
    
    const prompt = `## Rose Glass Analysis of ${recipientName || 'them'}:
${analysis}

## User's Reflection:

**What they noticed:** ${reflection.observation}

**What resonated:** ${reflection.resonance}

**What they want to express:** ${reflection.expression}

**Their intent:** ${reflection.intent}

---

Based on this, help craft an authentic opening message that:
1. Is calibrated to the recipient's communication style (from the analysis)
2. Expresses what's genuinely true for the user (from their reflection)
3. Creates space for real connection

Provide:
1. **Suggested Message** — The actual message they could send
2. **Calibration Notes** — Brief explanation of how it's tuned to the recipient
3. **Alternative Approach** — One other direction they could take`;

    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1500,
      system: CO_CREATION_SYSTEM_PROMPT,
      messages: [{ role: 'user', content: prompt }],
    });
    
    const textContent = response.content.find(block => block.type === 'text');
    const responseText = textContent?.type === 'text' ? textContent.text : '';
    
    return Response.json({
      success: true,
      coCreated: responseText,
      metrics: {
        inputTokens: response.usage.input_tokens,
        outputTokens: response.usage.output_tokens,
      },
    });
    
  } catch (error) {
    console.error('Co-creation error:', error);
    return Response.json(
      { error: error instanceof Error ? error.message : 'Co-creation failed' },
      { status: 500 }
    );
  }
}
```

### File: `src/app/api/chat/route.ts`

```typescript
import { NextRequest } from 'next/server';
import Anthropic from '@anthropic-ai/sdk';
import { ROSE_GLASS_DATING_SYSTEM_PROMPT } from '@/lib/rose-glass-dating';

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

const CHAT_SYSTEM_PROMPT = `${ROSE_GLASS_DATING_SYSTEM_PROMPT}

You are now in conversation mode. The user may:
- Ask follow-up questions about a profile analysis
- Upload new screenshots for analysis
- Ask for help crafting messages
- Discuss their dating situation generally

Remember the Two Hands Principle:
- Hand 1: What you perceive about others (translation)
- Hand 2: What's true for the user (their expression)

Before suggesting any message to send, ALWAYS ask what the user wants to express.
Understanding without self-expression is surveillance.
Self-expression without understanding is noise.
Connection requires both.`;

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { message, conversationHistory = [], images = [] } = body;
    
    if (!message && images.length === 0) {
      return Response.json({ error: 'Message or images required' }, { status: 400 });
    }
    
    // Build content array
    const content: any[] = [];
    
    // Add images if provided
    for (const img of images) {
      content.push({
        type: 'image',
        source: {
          type: 'base64',
          media_type: img.mediaType || 'image/png',
          data: img.data,
        },
      });
    }
    
    // Add text message
    if (message) {
      content.push({ type: 'text', text: message });
    }
    
    // Build messages array
    const messages: Anthropic.MessageParam[] = [
      ...conversationHistory.map((msg: { role: string; content: string }) => ({
        role: msg.role as 'user' | 'assistant',
        content: msg.content,
      })),
      { role: 'user' as const, content },
    ];
    
    const response = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 2000,
      system: CHAT_SYSTEM_PROMPT,
      messages,
    });
    
    const textContent = response.content.find(block => block.type === 'text');
    const responseText = textContent?.type === 'text' ? textContent.text : '';
    
    return Response.json({
      response: responseText,
      metrics: {
        inputTokens: response.usage.input_tokens,
        outputTokens: response.usage.output_tokens,
      },
    });
    
  } catch (error) {
    console.error('Chat error:', error);
    return Response.json(
      { error: error instanceof Error ? error.message : 'Chat failed' },
      { status: 500 }
    );
  }
}
```

---

## MAIN PAGES

### File: `src/app/page.tsx` (Landing)

```typescript
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-rose-50 to-white">
      <div className="container mx-auto px-4 py-16 max-w-4xl">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            🌹 Rose Glass Dating
          </h1>
          <p className="text-xl text-gray-600 mb-2">
            Translation, Not Judgment
          </p>
          <p className="text-gray-500">
            See dating profiles clearly. Express yourself authentically.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 gap-6 mb-12">
          <Link href="/analyze" className="block p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition border border-rose-100">
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">📸 Profile Analysis</h2>
            <p className="text-gray-600">
              Upload dating profile screenshots for Rose Glass translation. 
              Understand what they're actually filtering for.
            </p>
          </Link>
          
          <Link href="/chat" className="block p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition border border-rose-100">
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">💬 Chat Mode</h2>
            <p className="text-gray-600">
              Have a conversation about your dating situation. 
              Drop in screenshots anytime.
            </p>
          </Link>
        </div>
        
        <div className="bg-rose-50 rounded-xl p-6 border border-rose-200">
          <h3 className="font-semibold text-rose-900 mb-3">The Four Dimensions</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <span className="font-bold text-rose-700">Ψ</span>
              <span className="text-gray-700"> Internal Consistency</span>
            </div>
            <div>
              <span className="font-bold text-rose-700">ρ</span>
              <span className="text-gray-700"> Wisdom Depth</span>
            </div>
            <div>
              <span className="font-bold text-rose-700">q</span>
              <span className="text-gray-700"> Emotional Activation</span>
            </div>
            <div>
              <span className="font-bold text-rose-700">f</span>
              <span className="text-gray-700"> Social Belonging</span>
            </div>
          </div>
        </div>
        
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>"Coherence is constructed, not discovered."</p>
        </div>
      </div>
    </div>
  );
}
```

---

## DEPLOYMENT STEPS

### 1. Create New Repository

```bash
mkdir roseglass-dating-platform
cd roseglass-dating-platform
npx create-next-app@latest . --typescript --tailwind --app --src-dir
```

### 2. Install Dependencies

```bash
npm install @anthropic-ai/sdk react-dropzone react-markdown uuid
npm install -D @types/uuid
```

### 3. Create Directory Structure

```bash
mkdir -p src/lib src/components
```

### 4. Copy/Create Files

Create all files as specified above:
- `src/lib/rose-glass-dating.ts`
- `src/components/UploadZone.tsx`
- `src/app/api/analyze/route.ts`
- `src/app/api/co-create/route.ts`
- `src/app/api/chat/route.ts`
- `src/app/page.tsx`
- `src/app/analyze/page.tsx` (full analysis flow)
- `src/app/chat/page.tsx` (conversation mode)

### 5. Environment Variables

Create `.env.local`:
```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### 6. Test Locally

```bash
npm run dev
# Visit http://localhost:3000
```

### 7. Deploy to Vercel

```bash
# Initialize git
git init
git add .
git commit -m "Initial Rose Glass Dating platform"

# Push to GitHub
gh repo create roseglass-dating-platform --public --push

# Deploy via Vercel dashboard or CLI
vercel
```

### 8. Set Environment Variables in Vercel

In Vercel dashboard → Settings → Environment Variables:
- `ANTHROPIC_API_KEY` = your API key

---

## USER FLOW

### Flow 1: Profile Analysis

```
1. Landing Page → "Profile Analysis"
2. Upload Zone → Drop profile screenshots (1-10)
3. Optional: Add conversation screenshots
4. Optional: Add personal context
5. Click "Analyze"
6. View Rose Glass Analysis:
   - Dimension table (Ψ, ρ, q, f)
   - Key Translation
   - The Tell
   - Conversation Analysis (if applicable)
7. TWO HANDS FLOW:
   - "What do you notice about them?"
   - "What resonates with you?"
   - "What do you want to express?"
   - "What's your intent?"
8. Co-Created Response
9. Copy / Edit / Send
```

### Flow 2: Chat Mode

```
1. Landing Page → "Chat Mode"
2. Chat interface with drop zone
3. User can:
   - Ask questions
   - Drop screenshots mid-conversation
   - Get analysis inline
   - Ask for help crafting messages
4. Rose Glass maintains Two Hands:
   - Always asks what user wants to express
   - Never generates messages without reflection
```

---

## TWO HANDS PRINCIPLE ENFORCEMENT

**Critical:** The system MUST NOT generate suggested messages without user input.

### Before Co-Creation:

```typescript
// ReflectionGate pattern
if (!userReflection.observation || !userReflection.expression) {
  return Response.json({ 
    error: 'Reflection required',
    prompts: TWO_HANDS_REFLECTION_PROMPTS 
  }, { status: 400 });
}
```

### UI Enforcement:

- "Analyze" button leads to analysis ONLY
- "Help me respond" button requires reflection form completion
- Cannot skip reflection step
- Cannot proceed without filling all four reflection fields

---

## FEATURES COMPARISON

| Feature | Existing (Python) | New (Vercel) |
|---------|-------------------|--------------|
| Profile Analysis | ✅ | ✅ |
| Conversation Analysis | ✅ | ✅ |
| Screenshot Upload | ✅ | ✅ |
| Two Hands Flow | 🚧 Partial | ✅ Full |
| Chat Mode | ❌ | ✅ NEW |
| User Auth | Supabase | Optional |
| Cost Tracking | ✅ | Optional |
| Single Deploy | ❌ | ✅ |

---

## FILES TO READ FIRST

Before building:
1. `/Users/chris/rose-glass-dating/backend/app/prompts/system_prompt.py` — Full system prompt
2. `/Users/chris/rose-glass-dating/UNIVERSAL_UPDATE_TWO_HANDS.md` — Core philosophy
3. `/Users/chris/rose-glass-dating/frontend/components/upload-zone.tsx` — Upload component
4. `/Users/chris/rose-glass-dating/frontend/app/analyze/page.tsx` — Analysis page structure

---

## CONTEXT FOR NEXT CHAT

Start the next chat with:

"Read this build guide and execute it: /Users/chris/roseglass-dating-platform/DATING_BUILD_GUIDE.md

The goal is to create a standalone Vercel-hosted Rose Glass Dating platform with screenshot upload, profile analysis, and chat mode following the Two Hands Principle."

---

**End of Build Guide**
