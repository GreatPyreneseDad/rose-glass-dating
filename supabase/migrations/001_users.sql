-- Rose Glass Dating - Users Table
-- Stores user accounts and credit balances

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clerk_id TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    credits DECIMAL(10,4) DEFAULT 0 CHECK (credits >= 0),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_users_clerk_id ON users(clerk_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at DESC);

-- RLS Policies (Row Level Security)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Users can read their own data
CREATE POLICY "Users can read own data"
    ON users FOR SELECT
    USING (auth.uid()::text = clerk_id);

-- Service role can do anything
CREATE POLICY "Service role full access"
    ON users FOR ALL
    USING (auth.role() = 'service_role');

-- Comment
COMMENT ON TABLE users IS 'User accounts with Clerk authentication and credit balances';
COMMENT ON COLUMN users.credits IS 'User credit balance in USD (1 credit = $1)';
