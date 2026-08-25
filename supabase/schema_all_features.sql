
-- New tables for all features
CREATE TABLE IF NOT EXISTS public.mineral_buyers (
    id BIGSERIAL PRIMARY KEY,
    mineral TEXT,
    name TEXT,
    phone TEXT,
    price_offer TEXT,
    state TEXT,
    rating FLOAT
);

CREATE TABLE IF NOT EXISTS public.price_alerts (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    mineral TEXT,
    target_price FLOAT,
    active BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS public.find_of_day_submissions (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    mineral TEXT,
    image_url TEXT,
    votes INT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Add RLS policies
ALTER TABLE public.mineral_buyers ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.price_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.find_of_day_submissions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public buyers view" ON public.mineral_buyers FOR SELECT USING (true);
CREATE POLICY "Users can manage own alerts" ON public.price_alerts FOR ALL USING (auth.uid() = user_id);
CREATE POLICY "Users can insert submissions" ON public.find_of_day_submissions FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Public view submissions" ON public.find_of_day_submissions FOR SELECT USING (true);
