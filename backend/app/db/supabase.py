"""
Supabase Database Client
"""

from supabase import create_client, Client
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class SupabaseClient:
    """Supabase database operations"""

    def __init__(self, url: str, service_key: str):
        self.client: Client = create_client(url, service_key)

    async def get_or_create_user(self, clerk_id: str, email: str) -> dict:
        """Get existing user or create new one"""
        try:
            # Try to find existing user
            result = self.client.table('users') \
                .select('*') \
                .eq('clerk_id', clerk_id) \
                .execute()

            if result.data:
                return result.data[0]

            # Create new user
            result = self.client.table('users') \
                .insert({
                    'clerk_id': clerk_id,
                    'email': email,
                    'credits': 0,
                    'created_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }) \
                .execute()

            logger.info(f"Created new user: {clerk_id}")
            return result.data[0]

        except Exception as e:
            logger.error(f"Error getting/creating user: {e}")
            raise

    async def get_user_credits(self, user_id: str) -> float:
        """Get user's current credit balance"""
        try:
            result = self.client.table('users') \
                .select('credits') \
                .eq('id', user_id) \
                .execute()

            if not result.data:
                return 0.0

            return float(result.data[0]['credits'])

        except Exception as e:
            logger.error(f"Error getting credits: {e}")
            raise

    async def deduct_credits(self, user_id: str, amount: float) -> float:
        """Deduct credits from user balance, return new balance"""
        try:
            # Get current balance
            current = await self.get_user_credits(user_id)
            new_balance = current - amount

            # Update balance
            result = self.client.table('users') \
                .update({
                    'credits': new_balance,
                    'updated_at': datetime.utcnow().isoformat()
                }) \
                .eq('id', user_id) \
                .execute()

            logger.info(f"Deducted ${amount:.4f} from user {user_id}, new balance: ${new_balance:.4f}")
            return new_balance

        except Exception as e:
            logger.error(f"Error deducting credits: {e}")
            raise

    async def add_credits(self, user_id: str, amount: float) -> float:
        """Add credits to user balance, return new balance"""
        try:
            current = await self.get_user_credits(user_id)
            new_balance = current + amount

            result = self.client.table('users') \
                .update({
                    'credits': new_balance,
                    'updated_at': datetime.utcnow().isoformat()
                }) \
                .eq('id', user_id) \
                .execute()

            logger.info(f"Added ${amount:.2f} to user {user_id}, new balance: ${new_balance:.2f}")
            return new_balance

        except Exception as e:
            logger.error(f"Error adding credits: {e}")
            raise

    async def save_analysis(
        self,
        user_id: str,
        analysis_text: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: float,
        charge_usd: float,
        model_used: str
    ) -> dict:
        """Save analysis to database"""
        try:
            result = self.client.table('analyses') \
                .insert({
                    'user_id': user_id,
                    'analysis_text': analysis_text,
                    'input_tokens': input_tokens,
                    'output_tokens': output_tokens,
                    'cost_usd': cost_usd,
                    'charge_usd': charge_usd,
                    'model_used': model_used,
                    'created_at': datetime.utcnow().isoformat()
                }) \
                .execute()

            logger.info(f"Saved analysis for user {user_id}")
            return result.data[0]

        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            raise

    async def get_user_analyses(self, user_id: str, limit: int = 20) -> list:
        """Get user's analysis history"""
        try:
            result = self.client.table('analyses') \
                .select('*') \
                .eq('user_id', user_id) \
                .order('created_at', desc=True) \
                .limit(limit) \
                .execute()

            return result.data

        except Exception as e:
            logger.error(f"Error getting analyses: {e}")
            raise

    async def create_transaction(
        self,
        user_id: str,
        stripe_session_id: str,
        amount_usd: float,
        credits_added: float
    ) -> dict:
        """Create payment transaction record"""
        try:
            result = self.client.table('transactions') \
                .insert({
                    'user_id': user_id,
                    'stripe_session_id': stripe_session_id,
                    'amount_usd': amount_usd,
                    'credits_added': credits_added,
                    'status': 'pending',
                    'created_at': datetime.utcnow().isoformat()
                }) \
                .execute()

            return result.data[0]

        except Exception as e:
            logger.error(f"Error creating transaction: {e}")
            raise

    async def complete_transaction(
        self,
        stripe_session_id: str,
        stripe_payment_intent: str
    ) -> dict:
        """Mark transaction as completed"""
        try:
            result = self.client.table('transactions') \
                .update({
                    'status': 'completed',
                    'stripe_payment_intent': stripe_payment_intent
                }) \
                .eq('stripe_session_id', stripe_session_id) \
                .execute()

            return result.data[0]

        except Exception as e:
            logger.error(f"Error completing transaction: {e}")
            raise
