"""
ReflectionGate - Universal Two Hands Principle Enforcement

This class architecturally enforces the Two Hands Principle:
- Hand 1: What the system perceives about THEM (analysis)
- Hand 2: What is true for YOU (user reflection)

No output generation proceeds without passing through this gate.
"""

from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class UserReflection(BaseModel):
    """User's authentic perspective after seeing system analysis"""
    observation: str = Field(..., description="What the user noticed about the other person")
    resonance: str = Field(..., description="What resonates with user's own experience")
    intention: str = Field(..., description="What the user wants to express or share")
    context: Optional[str] = Field(None, description="Additional conversation context")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CombinedContext(BaseModel):
    """
    Combined context only available after reflection gate is passed.
    Contains both system perception AND user perspective.
    """
    system_perception: Any = Field(..., description="Original Rose Glass analysis")
    user_perspective: UserReflection = Field(..., description="User's authentic input")
    gate_passed_at: datetime = Field(default_factory=datetime.utcnow)


class ReflectionRequired(Exception):
    """
    Exception raised when attempting to proceed without user reflection.
    This is an architectural enforcement, not a validation error.
    """
    def __init__(self, message: str = "User reflection required before proceeding with co-creation"):
        self.message = message
        super().__init__(self.message)


class ReflectionGate:
    """
    Universal pattern for Two Hands principle enforcement.
    No output generation proceeds without passing through this gate.

    Usage:
        # Phase 1: Perception
        analysis = await analyze_profile(images)
        gate = ReflectionGate(analysis)

        # Return reflection prompts to user
        prompts = gate.prompt_reflection()

        # Wait for user input...

        # Phase 2: User provides reflection
        gate.receive_reflection({
            "observation": "She's a newcomer complaining about crowds",
            "resonance": "I don't mind lift lines - it's all mountain time",
            "intention": "Want to tease playfully and share my philosophy"
        })

        # Phase 3: Co-creation (only if gate passed)
        if gate.can_proceed():
            context = gate.get_combined_context()
            response = await co_create_message(context)
    """

    def __init__(self, analysis: Any, analysis_id: Optional[str] = None):
        """
        Initialize reflection gate with system's perception (Hand 1).
        Hand 2 remains empty until user provides their reflection.

        Args:
            analysis: The Rose Glass analysis result
            analysis_id: Optional ID for tracking/retrieval
        """
        self.analysis = analysis
        self.analysis_id = analysis_id
        self.user_reflection: Optional[UserReflection] = None
        self.gate_passed = False
        self.created_at = datetime.utcnow()
        self.passed_at: Optional[datetime] = None

    def prompt_reflection(self) -> List[str]:
        """
        Return context-appropriate reflection prompts.
        These prompts invite the user's truth, not confirmation of system analysis.

        Returns:
            List of open-ended reflection prompts
        """
        return [
            "What do you observe about them? What stands out?",
            "What resonates with your own experience?",
            "What do you want to express or share in your response?",
            "What is your intent in this interaction?"
        ]

    def get_reflection_prompts_structured(self) -> Dict[str, str]:
        """
        Return structured reflection prompts for API response.

        Returns:
            Dictionary with observation, resonance, and intention prompts
        """
        return {
            "observation_prompt": "What do you observe about them? What stands out?",
            "resonance_prompt": "What resonates with your own experience?",
            "intention_prompt": "What do you want to express or share in your response?"
        }

    def receive_reflection(self, user_input: Dict[str, str]) -> None:
        """
        User provides their perspective (Hand 2).
        This is the only way to pass through the gate.

        Args:
            user_input: Dictionary with observation, resonance, intention, and optional context

        Raises:
            ValueError: If required fields are missing or empty
        """
        # Validate required fields
        required = ["observation", "resonance", "intention"]
        missing = [field for field in required if not user_input.get(field)]

        if missing:
            raise ValueError(f"Missing required reflection fields: {', '.join(missing)}")

        # Validate non-empty strings
        empty = [field for field in required if not user_input.get(field, "").strip()]
        if empty:
            raise ValueError(f"Empty reflection fields not allowed: {', '.join(empty)}")

        # Create UserReflection model
        self.user_reflection = UserReflection(
            observation=user_input["observation"].strip(),
            resonance=user_input["resonance"].strip(),
            intention=user_input["intention"].strip(),
            context=user_input.get("context", "").strip() or None
        )

        # Gate is now passed
        self.gate_passed = True
        self.passed_at = datetime.utcnow()

    def can_proceed(self) -> bool:
        """
        Check if gate has been passed.

        Returns:
            True if user has provided reflection, False otherwise
        """
        return self.gate_passed and self.user_reflection is not None

    def get_combined_context(self) -> CombinedContext:
        """
        Get combined context of system perception AND user perspective.
        This is only available after the gate has been passed.

        Returns:
            CombinedContext with both hands' information

        Raises:
            ReflectionRequired: If gate has not been passed
        """
        if not self.can_proceed():
            raise ReflectionRequired(
                "Cannot access combined context without user reflection. "
                "The system can inform both hands, but cannot close them together. "
                "That is where the human lives."
            )

        return CombinedContext(
            system_perception=self.analysis,
            user_perspective=self.user_reflection
        )

    def get_co_creation_prompt(self) -> str:
        """
        Generate prompt for co-creation that integrates both hands.
        Only available after gate is passed.

        Returns:
            Formatted prompt for Claude including both perspectives

        Raises:
            ReflectionRequired: If gate has not been passed
        """
        if not self.can_proceed():
            raise ReflectionRequired()

        context = self.get_combined_context()

        prompt = f"""
## System Perception (Hand 1)

{context.system_perception}

## User Perspective (Hand 2)

**What they observed:** {context.user_perspective.observation}

**What resonates for them:** {context.user_perspective.resonance}

**What they want to share:** {context.user_perspective.intention}

{f"**Additional context:** {context.user_perspective.context}" if context.user_perspective.context else ""}

## Co-Creation Task

Based on BOTH the system's perception AND the user's authentic input, help articulate a message that:

1. **Calibrates to the other person's communication style** (from the analysis)
2. **Expresses what's genuinely true for the user** (from their reflection)
3. **Creates space for real connection** (not just engagement)

The message should feel like the user - you're helping them articulate, not generating something artificial.

Format as a quoted message they can send directly.
"""
        return prompt

    def __repr__(self) -> str:
        status = "PASSED" if self.gate_passed else "WAITING"
        return f"ReflectionGate(analysis_id={self.analysis_id}, status={status})"


# Export
__all__ = [
    'ReflectionGate',
    'UserReflection',
    'CombinedContext',
    'ReflectionRequired'
]
