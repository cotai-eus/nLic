-- Initial database schema for nRadar
-- This script is used by Docker Compose to initialize the DB.

-- Enable pgcrypto for gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 1. users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_superuser BOOLEAN DEFAULT FALSE NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- users: updated_at trigger
CREATE TRIGGER trg_users_updated
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- 2. interest_profiles table
CREATE TABLE IF NOT EXISTS interest_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    nome_perfil VARCHAR(100) NOT NULL,
    palavras_chave JSONB NOT NULL,
    uf CHAR(2),
    municipio_ibge VARCHAR(10),
    modalidade_contratacao VARCHAR(10),
    categoria VARCHAR(50),
    prioridade_urgencia VARCHAR(20) NOT NULL,
    notificacao_push BOOLEAN DEFAULT FALSE,
    notificacao_email BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now(),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- interest_profiles: updated_at trigger
CREATE TRIGGER trg_profiles_updated
BEFORE UPDATE ON interest_profiles
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- interest_profiles: indexes
CREATE INDEX idx_profiles_user ON interest_profiles(user_id);
CREATE INDEX idx_profiles_palavras_chave ON interest_profiles USING GIN(palavras_chave);

-- 3. notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    profile_id UUID NOT NULL,
    numero_controle_pncp VARCHAR(50) NOT NULL,
    tipo VARCHAR(10) NOT NULL, -- 'push' or 'email'
    enviado_em TIMESTAMP DEFAULT now(),
    status VARCHAR(20) DEFAULT 'sent', -- 'sent', 'failed', 'pending'
    conteudo JSONB,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (profile_id) REFERENCES interest_profiles(id)
);

-- notifications: indexes
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_profile ON notifications(profile_id);
CREATE UNIQUE INDEX idx_notif_unique ON notifications(user_id, profile_id, numero_controle_pncp);

-- 4. notification_logs table
CREATE TABLE IF NOT EXISTS notification_logs (
    id BIGSERIAL PRIMARY KEY,
    notification_id UUID,
    log JSONB,
    created_at TIMESTAMP DEFAULT now(),
    FOREIGN KEY (notification_id) REFERENCES notifications(id)
);

-- notification_logs: index
CREATE INDEX idx_logs_notification ON notification_logs(notification_id);

-- 5. api_call_logs table
CREATE TABLE IF NOT EXISTS api_call_logs (
    id BIGSERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    params JSONB,
    response_status INTEGER,
    response_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT now()
);

-- api_call_logs: index
CREATE INDEX idx_api_call_endpoint ON api_call_logs(endpoint);