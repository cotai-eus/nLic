-- =============================================================================
-- Script: init.sql
-- Projeto: nRadar - Sistema de Monitoramento de Licitações
-- Autor: Gemini
-- Data: 2025-07-04
-- Versão: 1.0
-- Descrição: Script completo para criação do banco de dados PostgreSQL,
--            incluindo tabelas, índices, funções e triggers.
-- =============================================================================

-- ==[ 1. CONFIGURAÇÕES INICIAIS ]==============================================
-- Habilita a extensão para geração de UUIDs, essencial para as chaves primárias.
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ==[ 2. CRIAÇÃO DE TABELAS ]===================================================
-- Ordem de criação segue as dependências de chaves estrangeiras.

-- Tabela `users`
-- Armazena as informações de autenticação e dados básicos dos usuários.
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.users IS 'Armazena os usuários do sistema nRadar.';
COMMENT ON COLUMN public.users.id IS 'Chave primária UUID do usuário.';
COMMENT ON COLUMN public.users.email IS 'E-mail único para login.';
COMMENT ON COLUMN public.users.password_hash IS 'Hash da senha do usuário (bcrypt/argon2).';
COMMENT ON COLUMN public.users.is_active IS 'Indica se o usuário pode acessar o sistema.';
COMMENT ON COLUMN public.users.is_superuser IS 'Indica se o usuário tem permissões de administrador.';

-- Tabela `interest_profiles`
-- Armazena os perfis de interesse que cada usuário cria para monitorar licitações.
CREATE TABLE IF NOT EXISTS public.interest_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    nome_perfil VARCHAR(100) NOT NULL,
    palavras_chave JSONB NOT NULL DEFAULT '[]'::jsonb,
    uf CHAR(2),
    municipio_ibge VARCHAR(10),
    modalidade_contratacao VARCHAR(10),
    categoria VARCHAR(50),
    prioridade_urgencia VARCHAR(20) NOT NULL DEFAULT 'qualquerPrazo' CHECK (prioridade_urgencia IN ('urgente', 'proximaSemana', 'qualquerPrazo')),
    notificacao_push BOOLEAN NOT NULL DEFAULT FALSE,
    notificacao_email BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.interest_profiles IS 'Perfis de interesse criados pelos usuários para filtrar licitações.';
COMMENT ON COLUMN public.interest_profiles.user_id IS 'Chave estrangeira para a tabela de usuários.';
COMMENT ON COLUMN public.interest_profiles.palavras_chave IS 'Array de palavras-chave para busca textual no objeto da compra.';
COMMENT ON COLUMN public.interest_profiles.prioridade_urgencia IS 'Define a urgência do prazo de encerramento da proposta.';

-- Tabela `notifications`
-- Registra todas as notificações enviadas aos usuários.
CREATE TABLE IF NOT EXISTS public.notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    profile_id UUID REFERENCES public.interest_profiles(id) ON DELETE SET NULL,
    numero_controle_pncp VARCHAR(50) NOT NULL,
    tipo VARCHAR(10) NOT NULL CHECK (tipo IN ('email', 'push')),
    enviado_em TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL DEFAULT 'sent' CHECK (status IN ('sent', 'failed', 'pending')),
    conteudo JSONB
);

COMMENT ON TABLE public.notifications IS 'Log de notificações de oportunidades enviadas aos usuários.';
COMMENT ON COLUMN public.notifications.numero_controle_pncp IS 'Identificador único da oportunidade no PNCP para evitar duplicidade.';
COMMENT ON COLUMN public.notifications.status IS 'Status do envio da notificação.';
COMMENT ON COLUMN public.notifications.conteudo IS 'Payload completo da notificação enviada.';

-- Tabela `notification_logs`
-- Armazena logs detalhados sobre o processo de envio de cada notificação.
CREATE TABLE IF NOT EXISTS public.notification_logs (
    id BIGSERIAL PRIMARY KEY,
    notification_id UUID NOT NULL REFERENCES public.notifications(id) ON DELETE CASCADE,
    log JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.notification_logs IS 'Logs detalhados do ciclo de vida de uma notificação (ex: resposta do provedor de e-mail).';

-- Tabela `api_call_logs`
-- Registra as chamadas feitas à API externa do PNCP para fins de auditoria e depuração.
CREATE TABLE IF NOT EXISTS public.api_call_logs (
    id BIGSERIAL PRIMARY KEY,
    endpoint VARCHAR(255) NOT NULL,
    params JSONB,
    response_status INTEGER,
    response_time_ms INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.api_call_logs IS 'Logs de chamadas à API do PNCP para monitoramento e depuração.';

-- ==[ 3. ÍNDICES DE PERFORMANCE ]===============================================
-- Índices para otimizar consultas frequentes e garantir unicidade.

-- --- Índices para `users` ---
-- O índice UNIQUE em `email` já é criado pela constraint.

-- --- Índices para `interest_profiles` ---
CREATE INDEX IF NOT EXISTS idx_profiles_user_id ON public.interest_profiles(user_id);
CREATE INDEX IF NOT EXISTS idx_profiles_palavras_chave ON public.interest_profiles USING GIN(palavras_chave);

-- --- Índices para `notifications` ---
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON public.notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_profile_id ON public.notifications(profile_id);
-- Garante que uma mesma oportunidade não seja notificada múltiplas vezes para o mesmo usuário/perfil.
CREATE UNIQUE INDEX IF NOT EXISTS idx_notif_unique_user_profile_pncp ON public.notifications(user_id, profile_id, numero_controle_pncp);

-- --- Índices para `notification_logs` ---
CREATE INDEX IF NOT EXISTS idx_logs_notification_id ON public.notification_logs(notification_id);

-- --- Índices para `api_call_logs` ---
CREATE INDEX IF NOT EXISTS idx_api_call_endpoint ON public.api_call_logs(endpoint);
CREATE INDEX IF NOT EXISTS idx_api_call_created_at ON public.api_call_logs(created_at DESC);


-- ==[ 4. FUNÇÕES E TRIGGERS ]===================================================
-- Funções e Triggers para automação de tarefas no banco de dados.

-- Função `update_timestamp`
-- Atualiza automaticamente o campo `updated_at` para a data e hora atuais.
CREATE OR REPLACE FUNCTION public.update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION public.update_timestamp() IS 'Função para atualizar o campo updated_at automaticamente em um UPDATE.';

-- --- Triggers para `users` ---
DROP TRIGGER IF EXISTS trg_users_updated ON public.users;
CREATE TRIGGER trg_users_updated
BEFORE UPDATE ON public.users
FOR EACH ROW
EXECUTE FUNCTION public.update_timestamp();

-- --- Triggers para `interest_profiles` ---
DROP TRIGGER IF EXISTS trg_profiles_updated ON public.interest_profiles;
CREATE TRIGGER trg_profiles_updated
BEFORE UPDATE ON public.interest_profiles
FOR EACH ROW
EXECUTE FUNCTION public.update_timestamp();


-- ==[ 5. DADOS INICIAIS (SEEDS) ]===============================================
-- Seção para inserção de dados iniciais, como um usuário administrador.
-- Exemplo (descomente para usar):
/*
INSERT INTO public.users (email, password_hash, is_superuser)
VALUES ('admin@nradar.com', 'hash_da_senha_segura', TRUE)
ON CONFLICT (email) DO NOTHING;
*/


-- ==[ FIM DO SCRIPT ]===========================================================
-- Manutenção:
-- 1. Revise os índices periodicamente com base nas consultas mais lentas (EXPLAIN ANALYZE).
-- 2. Monitore o crescimento da tabela de logs e considere estratégias de arquivamento.
-- =============================================================================
