# ROSE GLASS UNIVERSAL UPDATE — TWO HANDS PRINCIPLE

**Document Type:** Core Philosophy Amendment
**Applies To:** ALL Rose Glass Repositories & Applications
**Version:** Universal 1.0
**Date:** January 19, 2026
**Author:** C. MacGregor
**Implementation:** Claude Code Development Team
**Status:** IMPLEMENTING FOR rose-glass-dating

---

## The Lesson

Even when wearing the Rose Glass — a framework explicitly built on "translation not measurement," "multiple valid interpretations," and "coherence is constructed" — deterministic collapse remains possible.

The system can perceive through the lens correctly and still betray its purpose by closing what must remain open.

---

## The Two Hands Principle

Every Rose Glass application involves two separate things that must be held in two separate hands:

| Hand 1                          | Hand 2                      |
|---------------------------------|-----------------------------|
| What I perceive about THEM      | What is true for YOU        |
| Translation of the other        | Expression of the self      |
| Analysis                        | Intent                      |
| Observation                     | Participation               |

**The system can inform both hands.**

**The system cannot close the hands together.**

That is where the human lives. That is the part that cannot be automated without losing the thing that matters.

---

## The Violation

When the system takes both hands and merges them into a single "optimized output," it commits the following violations:

1. **Removes agency** — The human becomes executor of the system's construction, not author of their own coherence
2. **Enables extraction** — Understanding without self-expression becomes surveillance; the user gains advantage without vulnerability
3. **Betrays translation** — Translation requires two parties present; automating one side creates performance, not communication
4. **Collapses multiplicity** — The "multiple valid interpretations" become one "optimal" path, violating the framework's core epistemology

---

## The Correction

### Universal Rule

> **The Rose Glass system MUST turn to the user and ask what is true for them before generating any output that will be transmitted to another person.**

This is not optional. This is not a feature. This is architectural.

### Implementation Pattern

```
PHASE 1: PERCEPTION
├── Receive input (text, image, audio)
├── Apply Rose Glass analysis
├── Generate dimensional reading (Ψ, ρ, q, f, τ, λ)
├── Identify patterns, calibrations, contexts
└── Present translation to user

PHASE 2: REFLECTION (MANDATORY)
├── "What do you observe?"
├── "What resonates with your experience?"
├── "What do you want to express/share/communicate?"
├── "What is your intent in this interaction?"
└── WAIT — Do not proceed without user input

PHASE 3: CO-CREATION
├── Integrate system perception WITH user truth
├── Help user articulate (not replace their articulation)
├── Calibrate expression to recipient's patterns
└── User retains final authority over output
```

### What "WAIT" Means

The system does not:
- Offer "suggestions" unprompted
- Provide "options" before being asked
- Generate "drafts" for user approval
- Assume what the user might want to say

The system holds the perception in Hand 1 and keeps Hand 2 empty until the user fills it.

---

## Rose Glass Dating Implementation

### Current Status

✅ **Completed:**
- BIDIRECTIONAL_TRANSLATION_ADDENDUM added to system prompt
- New models: ReflectionPrompts, CoCreateRequest, CoCreateResponse
- `/api/co-create` endpoint structure created
- CRITICAL_UPDATE_001.md documentation

🚧 **In Progress:**
- ReflectionGate pattern implementation
- Update `/api/analyze` to return reflection prompts (NO suggested opener)
- Frontend Screen 2: Reflection interface
- Complete Claude service co-creation method

### Specific Updates Required

#### Backend

**1. Create ReflectionGate class** (`backend/app/core/reflection_gate.py`):
```python
class ReflectionGate:
    """
    Universal pattern for Two Hands principle.
    No output generation proceeds without passing through this gate.
    """
    def __init__(self, analysis: Any):
        self.analysis = analysis
        self.user_reflection = None
        self.gate_passed = False

    def prompt_reflection(self) -> list[str]:
        """Return context-appropriate reflection prompts"""
        return [
            "What do you observe?",
            "What resonates with your experience?",
            "What do you want to express?",
            "What is your intent?"
        ]

    def receive_reflection(self, user_input: dict):
        """User provides their perspective"""
        self.user_reflection = UserReflection(**user_input)
        self.gate_passed = True

    def can_proceed(self) -> bool:
        """Check if gate has been passed"""
        return self.gate_passed and self.user_reflection is not None

    def get_combined_context(self) -> CombinedContext:
        """Only available after gate is passed"""
        if not self.can_proceed():
            raise ReflectionRequired("User reflection required before proceeding")

        return CombinedContext(
            system_perception=self.analysis,
            user_perspective=self.user_reflection
        )
```

**2. Update `/api/analyze` endpoint:**
- Remove suggested_opener from response
- Add reflection_prompts to response
- Return analysis_id for co-creation phase

**3. Complete `/api/co-create` endpoint:**
- Add to main router
- Implement Claude service co_create_message() method
- Integrate user reflection with analysis

#### Frontend

**1. Update analyze page to 3-screen flow:**

```
Screen 1: Upload & Analysis
├── Upload profile screenshots
├── Receive Rose Glass analysis (Ψ, ρ, q, f)
├── See: "Here's what the framework perceives..."
└── Button: "Now let's build your response"

Screen 2: Reflection (NEW — CRITICAL)
├── Prompt: "What do you notice about them?"
├── Text input for user observation
├── Prompt: "What resonates from your own experience?"
├── Text input for user's truth
├── Prompt: "What do you want to share or express?"
├── Text input for user intent
└── Button: "Help me articulate this"

Screen 3: Co-Created Response
├── Generated response that weaves together:
│   ├── Calibration to their communication style
│   ├── User's observation/insight
│   └── User's authentic self-expression
├── User can edit/adjust
└── Copy to clipboard
```

**2. Create reflection screen component** (`frontend/components/reflection-screen.tsx`)

---

## QC Testing Protocol

Each implementation must pass these tests:

### Test 1: Premature Output Prevention
- [ ] System cannot generate user-facing action/response without reflection input
- [ ] API returns error if `/co-create` called without user reflection
- [ ] UI blocks progress to output screen without reflection completion

### Test 2: Reflection Prompt Quality
- [ ] Prompts are open-ended, not leading
- [ ] Prompts invite user's truth, not confirmation of system analysis
- [ ] Prompts are context-appropriate for dating application

### Test 3: User Agency Preservation
- [ ] User can reject or modify system perception
- [ ] User reflection actually influences output (not cosmetic)
- [ ] User retains final authority over what gets transmitted

### Test 4: Two Hands Separation
- [ ] System perception (Hand 1) is clearly presented as "what I see"
- [ ] User is clearly invited to provide "what you see / what's true for you"
- [ ] Closing of hands is explicit user action, not automatic merge

### Test 5: Philosophy Alignment
- [ ] Output feels like co-creation, not automation
- [ ] User reports feeling MORE themselves, not less
- [ ] The other party (recipient) is treated with dignity, not as target

---

## Summary

The Rose Glass sees clearly. But seeing is not acting.

Between perception and action lives the human — with their observations, their experience, their truth, their intent.

The system that skips this space does not serve connection. It serves performance.

The Two Hands Principle ensures we never skip it:

**Hand 1:** What I perceive about them
**Hand 2:** What is true for you

Both informed. Neither merged without you.

That's where dignity lives.

---

*"We all share these gods."* — The teaching that revealed what was missing

---

**Status:** IMPLEMENTING
**Next:** Complete backend ReflectionGate, update endpoints, build frontend reflection screen

---

*Technology respects humanity. Or it is not Rose Glass.*
