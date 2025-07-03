-- Habilita a extensão pgcrypto para gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Função para atualizar o campo updated_at automaticamente
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Tabela: users
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Trigger para users.updated_at
CREATE TRIGGER trg_users_updated
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- Tabela: interest_profiles
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
    CONSTRAINT fk_user
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Trigger para interest_profiles.updated_at
CREATE TRIGGER trg_profiles_updated
BEFORE UPDATE ON interest_profiles
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- Tabela: notifications
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    profile_id UUID,
    numero_controle_pncp VARCHAR(50) NOT NULL,
    tipo VARCHAR(10) NOT NULL,
    enviado_em TIMESTAMP DEFAULT now(),
    status VARCHAR(20) DEFAULT 'sent',
    conteudo JSONB,
    CONSTRAINT fk_user_notif
        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_profile_notif
        FOREIGN KEY(profile_id)
        REFERENCES interest_profiles(id)
        ON DELETE SET NULL
);

-- Tabela: notification_logs
CREATE TABLE IF NOT EXISTS notification_logs (
    id BIGSERIAL PRIMARY KEY,
    notification_id UUID,
    log JSONB,
    created_at TIMESTAMP DEFAULT now(),
    CONSTRAINT fk_notification_log
        FOREIGN KEY(notification_id)
        REFERENCES notifications(id)
        ON DELETE CASCADE
);

-- Tabela: api_call_logs
CREATE TABLE IF NOT EXISTS api_call_logs (
    id BIGSERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    params JSONB,
    response_status INTEGER,
    response_time_ms INTEGER,
    created_at TIMESTAMP DEFAULT now()
);

-- Índices
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_profiles_user ON interest_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_profiles_palavras_chave ON interest_profiles USING GIN(palavras_chave);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_profile ON notifications(profile_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_notif_unique ON notifications(user_id, profile_id, numero_controle_pncp);
CREATE INDEX IF NOT EXISTS idx_logs_notification ON notification_logs(notification_id);
CREATE INDEX IF NOT EXISTS idx_api_call_endpoint ON api_call_logs(endpoint);
