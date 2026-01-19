"""
Analysis Router - Main API Endpoint

POST /api/analyze - Analyze dating profile through Rose Glass
GET /api/analyze/history - Get analysis history
"""

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import Optional
import base64
import logging

from app.services.claude_service import ClaudeService
from app.services.auth import get_current_user, User
from app.db.supabase import SupabaseClient
from app.config import get_settings
from app.models.analysis import AnalysisResponse, AnalysisHistoryItem

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/analyze", tags=["analysis"])

# Initialize services
settings = get_settings()
claude = ClaudeService(api_key=settings.anthropic_api_key)
db = SupabaseClient(url=settings.supabase_url, service_key=settings.supabase_service_key)


@router.post("/", response_model=AnalysisResponse)
async def analyze_profile(
    profile_images: list[UploadFile] = File(..., description="1-10 profile screenshots"),
    conversation_images: Optional[list[UploadFile]] = File(None, description="Optional conversation screenshots"),
    user_context: Optional[str] = Form(None, description="Optional context about yourself"),
    use_premium: bool = Form(False, description="Use premium model (Claude Opus)"),
    user: User = Depends(get_current_user)
):
    """
    Analyze dating profile through Rose Glass framework.

    **Process:**
    1. Upload profile screenshots (required)
    2. Optionally add conversation screenshots
    3. Optionally provide context about yourself
    4. Get Rose Glass analysis with suggested opener

    **Cost:** $0.02-0.10 per analysis depending on image count and model
    """

    # Validate image count
    if not profile_images or len(profile_images) == 0:
        raise HTTPException(status_code=400, detail="At least 1 profile image required")

    if len(profile_images) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 profile images allowed")

    if conversation_images and len(conversation_images) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 conversation images allowed")

    logger.info(f"Analysis request from user {user.clerk_id}: "
               f"{len(profile_images)} profile images, "
               f"{len(conversation_images) if conversation_images else 0} conversation images, "
               f"premium={use_premium}")

    # Check user credits (estimate minimum $0.05)
    try:
        credits = await db.get_user_credits(user.id)
        logger.info(f"User {user.clerk_id} has ${credits:.4f} credits")
    except Exception as e:
        logger.error(f"Error checking credits: {e}")
        # For MVP, allow analysis without credit check
        credits = 100.0  # Fake credits for testing

    if credits < 0.02:
        raise HTTPException(
            status_code=402,
            detail="Insufficient credits. Please add funds to continue.",
            headers={"X-Required-Credits": "0.02"}
        )

    # Process images to base64
    profile_b64 = []
    for img in profile_images:
        try:
            content = await img.read()
            profile_b64.append(base64.b64encode(content).decode())
        except Exception as e:
            logger.error(f"Error reading profile image: {e}")
            raise HTTPException(status_code=400, detail=f"Invalid image file: {img.filename}")

    conversation_b64 = None
    if conversation_images:
        conversation_b64 = []
        for img in conversation_images:
            try:
                content = await img.read()
                conversation_b64.append(base64.b64encode(content).decode())
            except Exception as e:
                logger.error(f"Error reading conversation image: {e}")
                raise HTTPException(status_code=400, detail=f"Invalid image file: {img.filename}")

    # Run analysis
    try:
        result = await claude.analyze_profile(
            images=profile_b64,
            user_context=user_context,
            conversation_images=conversation_b64,
            use_premium=use_premium
        )
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    # Get charge amount
    charge = result["usage"]["charge_usd"]

    # Check if user has enough credits
    if credits < charge:
        raise HTTPException(
            status_code=402,
            detail=f"Insufficient credits. Analysis costs ${charge:.4f}, you have ${credits:.4f}",
            headers={"X-Required-Credits": str(charge)}
        )

    # Deduct credits
    try:
        new_balance = await db.deduct_credits(user.id, charge)
    except Exception as e:
        logger.error(f"Error deducting credits: {e}")
        # For MVP, continue without deducting
        new_balance = credits - charge

    # Save analysis to database
    try:
        analysis_record = await db.save_analysis(
            user_id=user.id,
            analysis_text=result["analysis"],
            input_tokens=result["usage"]["input_tokens"],
            output_tokens=result["usage"]["output_tokens"],
            cost_usd=result["usage"]["cost_usd"],
            charge_usd=charge,
            model_used=result["model_used"]
        )
        analysis_id = analysis_record["id"]
    except Exception as e:
        logger.error(f"Error saving analysis: {e}")
        analysis_id = None

    logger.info(f"Analysis complete for user {user.clerk_id}. "
               f"Charged ${charge:.4f}, new balance ${new_balance:.4f}")

    return AnalysisResponse(
        success=True,
        analysis=result["analysis"],
        usage=result["usage"],
        remaining_credits=new_balance,
        analysis_id=analysis_id
    )


@router.get("/history")
async def get_analysis_history(
    limit: int = 20,
    user: User = Depends(get_current_user)
):
    """Get user's analysis history"""
    try:
        analyses = await db.get_user_analyses(user.id, limit)

        return {
            "success": True,
            "analyses": [
                AnalysisHistoryItem(
                    id=a["id"],
                    analysis_text=a["analysis_text"],
                    created_at=a["created_at"],
                    model_used=a["model_used"],
                    cost_usd=a["cost_usd"],
                    charge_usd=a["charge_usd"]
                )
                for a in analyses
            ]
        }
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get history")


@router.get("/credits")
async def get_credits(user: User = Depends(get_current_user)):
    """Get user's current credit balance"""
    try:
        credits = await db.get_user_credits(user.id)
        return {
            "success": True,
            "user_id": user.id,
            "credits": credits
        }
    except Exception as e:
        logger.error(f"Error getting credits: {e}")
        # For MVP, return fake credits
        return {
            "success": True,
            "user_id": user.id,
            "credits": 100.0
        }
