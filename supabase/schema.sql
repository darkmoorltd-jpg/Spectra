
-- Run this in Supabase SQL Editor

-- Profiles table (optional, for storing user details)
CREATE TABLE IF NOT EXISTS public.user_profiles (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    state TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Scans table (each user has a row with remaining scans)
CREATE TABLE IF NOT EXISTS public.user_scans (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    scans_remaining INTEGER DEFAULT 30,
    plan TEXT DEFAULT 'free',
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Payment history (for future use)
CREATE TABLE IF NOT EXISTS public.payment_history (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    amount NUMERIC,
    scans_added INTEGER,
    plan TEXT,
    reference TEXT UNIQUE,
    paid_at TIMESTAMPTZ DEFAULT now()
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_scans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.payment_history ENABLE ROW LEVEL SECURITY;

-- Policies: users can read/update their own rows
CREATE POLICY "Users can view own profile" ON public.user_profiles
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update own profile" ON public.user_profiles
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own profile" ON public.user_profiles
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own scans" ON public.user_scans
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can update own scans" ON public.user_scans
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own scans" ON public.user_scans
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own payments" ON public.payment_history
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own payments" ON public.payment_history
    FOR INSERT WITH CHECK (auth.uid() = user_id);
