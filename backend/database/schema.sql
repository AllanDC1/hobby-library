-- Executar no SQL Editor do Supabase (supabase.com → seu projeto → SQL Editor)

CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Habilitar RLS (Row Level Security) - desativado para simplificar
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Política pública (para uso sem autenticação)
CREATE POLICY "Allow all" ON users FOR ALL USING (true) WITH CHECK (true);
