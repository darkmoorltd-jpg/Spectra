
-- Additional tables for gamification, history, referrals
CREATE TABLE IF NOT EXISTS public.user_streaks (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    streak_count INT DEFAULT 0,
    last_scan_date DATE
);

CREATE TABLE IF NOT EXISTS public.scan_history (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    mineral TEXT,
    confidence FLOAT,
    grade FLOAT,
    value_ngn NUMERIC,
    image_url TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.referrals (
    id BIGSERIAL PRIMARY KEY,
    referrer_user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    referred_user_id UUID UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.user_streaks ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.scan_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.referrals ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own streak" ON public.user_streaks FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own streak" ON public.user_streaks FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own streak" ON public.user_streaks FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own history" ON public.scan_history FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own history" ON public.scan_history FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own referrals" ON public.referrals FOR SELECT USING (auth.uid() = referrer_user_id);
CREATE POLICY "Users can insert referrals" ON public.referrals FOR INSERT WITH CHECK (auth.uid() = referrer_user_id);
