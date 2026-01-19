-- Rose Glass Dating - Transactions Table
-- Stores payment transactions from Stripe

CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stripe_session_id TEXT UNIQUE,
    stripe_payment_intent TEXT,
    amount_usd DECIMAL(10,2) NOT NULL CHECK (amount_usd > 0),
    credits_added DECIMAL(10,4) NOT NULL CHECK (credits_added > 0),
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed', 'refunded')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_transactions_stripe_session ON transactions(stripe_session_id);
CREATE INDEX IF NOT EXISTS idx_transactions_stripe_intent ON transactions(stripe_payment_intent);
CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(status);
CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions(created_at DESC);

-- RLS Policies
ALTER TABLE transactions ENABLE ROW LEVEL SECURITY;

-- Users can read their own transactions
CREATE POLICY "Users can read own transactions"
    ON transactions FOR SELECT
    USING (user_id IN (SELECT id FROM users WHERE clerk_id = auth.uid()::text));

-- Service role can do anything
CREATE POLICY "Service role full access transactions"
    ON transactions FOR ALL
    USING (auth.role() = 'service_role');

-- Comments
COMMENT ON TABLE transactions IS 'Payment transactions for credit purchases';
COMMENT ON COLUMN transactions.amount_usd IS 'Amount paid in USD';
COMMENT ON COLUMN transactions.credits_added IS 'Credits added to user account';
COMMENT ON COLUMN transactions.status IS 'Transaction status: pending, completed, failed, refunded';
