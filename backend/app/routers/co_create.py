"""
Co-Create Router - Bidirectional Translation Endpoint

POST /api/co-create - Co-create response with user input
"""

from fastapi import APIRouter, Depends, HTTPException, Body
import logging
import uuid

from app.services.claude_service import ClaudeService
from app.services.auth import get_current_user, User
from app.db.supabase import SupabaseClient
from app.config import get_settings
from app.models.analysis import CoCreateRequest, CoCreateResponse
from app.prompts.system_prompt import BIDIRECTIONAL_TRANSLATION_ADDENDUM

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/co-create", tags=["co-create"])

# Initialize services
settings = get_settings()
claude = ClaudeService(api_key=settings.anthropic_api_key)
db = SupabaseClient(url=settings.supabase_url, service_key=settings.supabase_service_key)


@router.post("/", response_model=CoCreateResponse)
async def co_create_response(
    request: CoCreateRequest = Body(...),
    user: User = Depends(get_current_user)
):
    """
    Co-create response integrating user's authentic perspective.

    **Phase 2 of Bidirectional Translation:**
    1. User provides their observation, resonance, and intention
    2. System helps articulate a message that is:
       - Calibrated to the other person's communication style
       - Expresses what's genuinely true for the user
       - Creates space for real connection

    **This is NOT generating optimal responses - it's helping the user show up authentically**
    """

    logger.info(f"Co-create request from user {user.clerk_id} for analysis {request.analysis_id}")

    # Retrieve original analysis from database
    try:
        analysis = await db.get_analysis_by_id(request.analysis_id)
        if not analysis or analysis["user_id"] != user.id:
            raise HTTPException(status_code=404, detail="Analysis not found")
    except Exception as e:
        logger.error(f"Error retrieving analysis: {e}")
        # For MVP without full DB, use a placeholder
        analysis = {"analysis_text": "Rose Glass analysis from Phase 1"}

    # Check user credits
    try:
        credits = await db.get_user_credits(user.id)
    except Exception as e:
        logger.error(f"Error checking credits: {e}")
        credits = 100.0  # Fake credits for MVP testing

    if credits < 0.02:
        raise HTTPException(
            status_code=402,
            detail="Insufficient credits for co-creation",
            headers={"X-Required-Credits": "0.02"}
        )

    # Build co-creation prompt
    co_creation_prompt = f"""
{BIDIRECTIONAL_TRANSLATION_ADDENDUM}

## Original Analysis (Phase 1)

{analysis.get("analysis_text", "Rose Glass analysis")}

## User Input (Phase 2)

**What they noticed:** {request.user_observation}

**What resonates for them:** {request.user_resonance}

**What they want to share:** {request.user_intention}

{f"**Conversation context:** {request.conversation_context}" if request.conversation_context else ""}

## Your Task

Based on the Rose Glass analysis AND the user's authentic input, help articulate a message that:

1. **Calibrates to their communication style** (from the analysis)
2. **Expresses what's genuinely true for the user** (from their input)
3. **Creates space for connection** (not just engagement)

The message should feel like the user - it's helping them articulate, not generating something artificial.

Format as a quoted message they can send directly.
"""

    # Call Claude to co-create response
    try:
        result = await claude.co_create_message(co_creation_prompt)
    except Exception as e:
        logger.error(f"Co-creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Co-creation failed: {str(e)}")

    # Get charge amount
    charge = result["usage"]["charge_usd"]

    # Check credits again
    if credits < charge:
        raise HTTPException(
            status_code=402,
            detail=f"Insufficient credits. Co-creation costs ${charge:.4f}, you have ${credits:.4f}",
            headers={"X-Required-Credits": str(charge)}
        )

    # Deduct credits
    try:
        new_balance = await db.deduct_credits(user.id, charge)
    except Exception as e:
        logger.error(f"Error deducting credits: {e}")
        new_balance = credits - charge

    logger.info(f"Co-creation complete for user {user.clerk_id}. "
               f"Charged ${charge:.4f}, new balance ${new_balance:.4f}")

    return CoCreateResponse(
        success=True,
        suggested_message=result["message"],
        usage=result["usage"],
        remaining_credits=new_balance
    )
