-- Rose Glass Dating - Analyses Table
-- Stores dating profile analyses

CREATE TABLE IF NOT EXISTS analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    analysis_text TEXT NOT NULL,
    input_tokens INTEGER NOT NULL CHECK (input_tokens > 0),
    output_tokens INTEGER NOT NULL CHECK (output_tokens > 0),
    cost_usd DECIMAL(10,6) NOT NULL CHECK (cost_usd > 0),
    charge_usd DECIMAL(10,6) NOT NULL CHECK (charge_usd > 0),
    model_used TEXT DEFAULT 'claude-sonnet-4-20250514',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_analyses_user_id ON analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_analyses_user_created ON analyses(user_id, created_at DESC);

-- RLS Policies
ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;

-- Users can read their own analyses
CREATE POLICY "Users can read own analyses"
    ON analyses FOR SELECT
    USING (user_id IN (SELECT id FROM users WHERE clerk_id = auth.uid()::text));

-- Service role can do anything
CREATE POLICY "Service role full access analyses"
    ON analyses FOR ALL
    USING (auth.role() = 'service_role');

-- Comments
COMMENT ON TABLE analyses IS 'Dating profile analyses with Rose Glass framework';
COMMENT ON COLUMN analyses.analysis_text IS 'Full analysis text from Claude';
COMMENT ON COLUMN analyses.cost_usd IS 'Raw API cost from Anthropic';
COMMENT ON COLUMN analyses.charge_usd IS 'Amount charged to user (includes markup)';
