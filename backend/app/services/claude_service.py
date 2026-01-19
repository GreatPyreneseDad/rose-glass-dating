"""
Claude Service - The Rose Glass Analysis Engine

This is where dating profiles are translated through the Rose Glass lens.
"""

import anthropic
from decimal import Decimal
from typing import Optional
import logging

from app.prompts.system_prompt import ROSE_GLASS_DATING_SYSTEM_PROMPT


logger = logging.getLogger(__name__)


class CostTracker:
    """
    Track API costs and apply markup.

    Pricing per 1M tokens (as of January 2025):
    - Sonnet 4: Input $3, Output $15
    - Opus 4: Input $15, Output $75
    """

    PRICING = {
        "claude-sonnet-4-20250514": {
            "input": Decimal("0.003"),   # per 1K tokens
            "output": Decimal("0.015"),
        },
        "claude-opus-4-20250514": {
            "input": Decimal("0.015"),
            "output": Decimal("0.075"),
        }
    }

    def calculate_cost(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> Decimal:
        """Calculate raw API cost in USD"""
        prices = self.PRICING.get(model, self.PRICING["claude-sonnet-4-20250514"])

        input_cost = (Decimal(input_tokens) / 1000) * prices["input"]
        output_cost = (Decimal(output_tokens) / 1000) * prices["output"]

        return input_cost + output_cost


class ClaudeService:
    """
    Rose Glass Dating Profile Analyzer powered by Claude.

    Uses Claude's vision capabilities to analyze dating profile screenshots
    and translate patterns through the Rose Glass framework.
    """

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.cost_tracker = CostTracker()

        # Use Sonnet for cost efficiency, Opus for complex analysis
        self.default_model = "claude-sonnet-4-20250514"
        self.premium_model = "claude-opus-4-20250514"

    async def analyze_profile(
        self,
        images: list[str],
        user_context: Optional[str] = None,
        conversation_images: Optional[list[str]] = None,
        use_premium: bool = False
    ) -> dict:
        """
        Analyze dating profile images through Rose Glass.

        Args:
            images: Base64 encoded profile screenshots
            user_context: Optional context about the user doing the analysis
            conversation_images: Optional conversation screenshots
            use_premium: Use Opus for more complex analysis

        Returns:
            Analysis results with usage metrics
        """
        model = self.premium_model if use_premium else self.default_model

        logger.info(f"Analyzing profile with {model}, {len(images)} profile images, "
                   f"{len(conversation_images) if conversation_images else 0} conversation images")

        # Build message content
        content = self._build_message_content(
            images,
            user_context,
            conversation_images
        )

        try:
            # Call Claude API
            response = self.client.messages.create(
                model=model,
                max_tokens=2500,
                temperature=1.0,  # Allow creative interpretation
                system=ROSE_GLASS_DATING_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": content}]
            )

            # Extract analysis text
            analysis_text = response.content[0].text

            # Calculate costs
            usage = response.usage
            cost = self.cost_tracker.calculate_cost(
                model=model,
                input_tokens=usage.input_tokens,
                output_tokens=usage.output_tokens
            )

            # Apply 100% markup
            charge = cost * 2

            logger.info(f"Analysis complete. Input: {usage.input_tokens}, "
                       f"Output: {usage.output_tokens}, Cost: ${float(cost):.4f}, "
                       f"Charge: ${float(charge):.4f}")

            return {
                "analysis": analysis_text,
                "model_used": model,
                "usage": {
                    "input_tokens": usage.input_tokens,
                    "output_tokens": usage.output_tokens,
                    "cost_usd": float(cost),
                    "charge_usd": float(charge)
                }
            }

        except anthropic.APIError as e:
            logger.error(f"Claude API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during analysis: {e}")
            raise

    def _build_message_content(
        self,
        images: list[str],
        user_context: Optional[str],
        conversation_images: Optional[list[str]]
    ) -> list[dict]:
        """Build the message content with images and text."""
        content = []

        # Add profile images
        for i, img_b64 in enumerate(images):
            content.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": self._detect_media_type(img_b64),
                    "data": img_b64
                }
            })

        # Add conversation images if provided
        if conversation_images:
            content.append({
                "type": "text",
                "text": "\n---\n**CONVERSATION SCREENSHOTS FOLLOW:**\n"
            })
            for img_b64 in conversation_images:
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": self._detect_media_type(img_b64),
                        "data": img_b64
                    }
                })

        # Build the analysis request
        analysis_request = self._build_analysis_request(
            user_context,
            has_conversation=bool(conversation_images)
        )

        content.append({
            "type": "text",
            "text": analysis_request
        })

        return content

    def _build_analysis_request(
        self,
        user_context: Optional[str],
        has_conversation: bool
    ) -> str:
        """Build the analysis request prompt."""

        request = "Analyze this dating profile through the Rose Glass framework.\n\n"

        if user_context:
            request += f"**User Context:** {user_context}\n\n"

        request += """Provide:

1. **Dimension Analysis Table** — Ψ, ρ, q, f with readings (0.0-1.0) and translations

2. **Key Translation** — What are they actually filtering for? (2-3 sentences)

3. **The Tell** — The ONE element that reveals the most about them

4. **Suggested Opener** — Calibrated to their specific communication style, formatted as a quoted message
"""

        if has_conversation:
            request += """
5. **Conversation Analysis** — Investment level, trajectory, red/green flags

6. **Next Move** — Clear recommendation on what to do/send next
"""

        request += """

Remember:
- Translation, not judgment
- Multiple valid interpretations exist
- Match their energy level in the opener
- Be specific, reference actual profile elements
- Never comment on physical appearance"""

        return request

    def _detect_media_type(self, base64_data: str) -> str:
        """Detect image media type from base64 content."""
        # Check first few characters to identify format
        if base64_data.startswith('/9j/'):
            return "image/jpeg"
        elif base64_data.startswith('iVBORw'):
            return "image/png"
        elif base64_data.startswith('R0lGOD'):
            return "image/gif"
        elif base64_data.startswith('UklGR'):
            return "image/webp"

        # Default to PNG
        return "image/png"
