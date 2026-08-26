
-- Add mining/artisan-specific columns to user_profiles
ALTER TABLE public.user_profiles
ADD COLUMN IF NOT EXISTS mining_state TEXT,
ADD COLUMN IF NOT EXISTS mining_lga TEXT,
ADD COLUMN IF NOT EXISTS mining_address TEXT,
ADD COLUMN IF NOT EXISTS minerals_of_interest TEXT,
ADD COLUMN IF NOT EXISTS years_mining_experience INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS mining_license_number TEXT,
ADD COLUMN IF NOT EXISTS mining_cooperative TEXT,
ADD COLUMN IF NOT EXISTS mining_type TEXT;
