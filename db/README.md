# Documentação do Banco de Dados - nRadar

Este documento descreve o esquema do banco de dados PostgreSQL utilizado pelo sistema nRadar, incluindo a estrutura das tabelas, índices e funções.

## Visão Geral

O banco de dados do nRadar é responsável por armazenar informações de usuários, perfis de interesse para monitoramento de licitações, registros de notificações enviadas e logs de chamadas à API externa do PNCP. Ele é projetado para ser escalável e otimizado para performance.

## Schema

O banco de dados utiliza o schema padrão `public` para todas as suas entidades.

## Tabelas

A seguir, a descrição detalhada de cada tabela:

### 1. `users`

Armazena as informações de autenticação e dados básicos dos usuários do sistema nRadar.

| Campo         | Tipo          | Restrições                               | Descrição                                     |
|---------------|---------------|------------------------------------------|-----------------------------------------------|
| `id`          | `UUID`        | `PRIMARY KEY`, `DEFAULT gen_random_uuid()` | Chave primária UUID do usuário.               |
| `email`       | `VARCHAR(255)`| `UNIQUE`, `NOT NULL`                     | E-mail único para login.                      |
| `password_hash`| `VARCHAR(255)`| `NOT NULL`                               | Hash da senha do usuário (bcrypt/argon2).     |
| `is_active`   | `BOOLEAN`     | `NOT NULL`, `DEFAULT TRUE`               | Indica se o usuário pode acessar o sistema.   |
| `is_superuser`| `BOOLEAN`     | `NOT NULL`, `DEFAULT FALSE`              | Indica se o usuário tem permissões de administrador. |
| `created_at`  | `TIMESTAMPTZ` | `NOT NULL`, `DEFAULT NOW()`              | Data e hora de criação do registro.           |
| `updated_at`  | `TIMESTAMPTZ` | `NOT NULL`, `DEFAULT NOW()`              | Data e hora da última atualização do registro. |

### 2. `interest_profiles`

Armazena os perfis de interesse que cada usuário cria para monitorar licitações.

| Campo                  | Tipo          | Restrições                               | Descrição                                     |
|------------------------|---------------|------------------------------------------|-----------------------------------------------|
| `id`                   | `UUID`        | `PRIMARY KEY`, `DEFAULT gen_random_uuid()` | Identificador único do perfil.                |
| `user_id`              | `UUID`        | `NOT NULL`, `FK users(id) ON DELETE CASCADE` | Chave estrangeira para a tabela de usuários.  |
| `nome_perfil`          | `VARCHAR(100)`| `NOT NULL`                               | Nome identificador do perfil.                 |
| `palavras_chave`       | `JSONB`       | `NOT NULL`, `DEFAULT '[]'::jsonb`        | Array de palavras-chave para busca textual no objeto da compra. |
| `uf`                   | `CHAR(2)`     |                                          | Unidade Federativa para filtro geográfico.    |
| `municipio_ibge`       | `VARCHAR(10)` |                                          | Código IBGE para o município.                 |
| `modalidade_contratacao`| `VARCHAR(10)` |                                          | Código da modalidade de contratação (opcional). |
| `categoria`            | `VARCHAR(50)` |                                          | Categoria da licitação (Produto, Serviço, etc.). |
| `prioridade_urgencia`  | `VARCHAR(20)` | `NOT NULL`, `DEFAULT 'qualquerPrazo'`, `CHECK` | Define a urgência do prazo de encerramento da proposta (`urgente`, `proximaSemana`, `qualquerPrazo`). |
| `notificacao_push`     | `BOOLEAN`     | `NOT NULL`, `DEFAULT FALSE`              | Habilita ou não notificações push.            |
| `notificacao_email`    | `BOOLEAN`     | `NOT NULL`, `DEFAULT TRUE`               | Habilita ou não notificações por e-mail.      |
| `created_at`           | `TIMESTAMPTZ` | `NOT NULL`, `DEFAULT NOW()`              | Data e hora de criação do registro.           |
| `updated_at`           | `TIMESTAMPTZ` | `NOT NULL`, `DEFAULT NOW()`              | Data e hora da última atualização do registro. |

### 3. `notifications`

Registra todas as notificações enviadas aos usuários.

| Campo                  | Tipo          | Restrições                               | Descrição                                     |
|------------------------|---------------|------------------------------------------|-----------------------------------------------|
| `id`                   | `UUID`        | `PRIMARY KEY`, `DEFAULT gen_random_uuid()` | Identificador único da notificação.           |
| `user_id`              | `UUID`        | `NOT NULL`, `FK users(id) ON DELETE CASCADE` | Usuário que recebeu a notificação.            |
| `profile_id`           | `UUID`        | `FK interest_profiles(id) ON DELETE SET NULL` | Perfil de interesse relacionado à notificação. |
| `numero_controle_pncp` | `VARCHAR(50)` | `NOT NULL`                               | Identificador único da oportunidade no PNCP para evitar duplicidade. |
| `tipo`                 | `VARCHAR(10)` | `NOT NULL`, `CHECK`                      | Tipo de notificação (`email` ou `push`).      |
| `enviado_em`           | `TIMESTAMPTZ` | `NOT NULL`, `DEFAULT NOW()`              | Data e hora do envio da notificação.          |
| `status`               | `VARCHAR(20)` | `NOT NULL`, `DEFAULT 'sent'`, `CHECK`    | Status do envio da notificação (`sent`, `failed`, `pending`). |
| `conteudo`             | `JSONB`       |                                          | Payload completo da notificação enviada.      |

### 4. `notification_logs`

Armazena logs detalhados sobre o processo de envio de cada notificação.

| Campo             | Tipo          | Restrições                               | Descrição                                     |
|-------------------|---------------|------------------------------------------|-----------------------------------------------|
| `id`              | `BIGSERIAL`   | `PRIMARY KEY`                            | Identificador único do log.                   |
| `notification_id` | `UUID`        | `NOT NULL`, `FK notifications(id) ON DELETE CASCADE` | Notificação relacionada ao log.               |
| `log`             | `JSONB`       |                                          | Log estruturado com detalhes do evento.       |
| `created_at`      | `TIMESTAMPTZ` | `NOT NULL`, `DEFAULT NOW()`              | Data e hora de criação do log.                |

### 5. `api_call_logs`

Registra as chamadas feitas à API externa do PNCP para fins de auditoria e depuração.

| Campo              | Tipo          | Restrições                               | Descrição                                     |
|--------------------|---------------|------------------------------------------|-----------------------------------------------|
| `id`               | `BIGSERIAL`   | `PRIMARY KEY`                            | Identificador único do log de chamada.        |
| `endpoint`         | `VARCHAR(255)`| `NOT NULL`                               | Endpoint da API do PNCP que foi chamado.      |
| `params`           | `JSONB`       |                                          | Parâmetros utilizados na chamada.             |
| `response_status`  | `INTEGER`     |                                          | Código de status HTTP da resposta.            |
| `response_time_ms` | `INTEGER`     |                                          | Tempo de resposta da API em milissegundos.    |
| `created_at`       | `TIMESTAMPTZ` | `NOT NULL`, `DEFAULT NOW()`              | Data e hora da chamada à API.                 |

## Índices de Performance

Os seguintes índices foram criados para otimizar o desempenho das consultas e garantir a unicidade dos dados:

*   **`users`**: `idx_users_email` (UNIQUE) no campo `email`.
*   **`interest_profiles`**:
    *   `idx_profiles_user_id` no campo `user_id`.
    *   `idx_profiles_palavras_chave` (GIN) no campo `palavras_chave` para buscas eficientes em JSONB.
*   **`notifications`**:
    *   `idx_notifications_user_id` no campo `user_id`.
    *   `idx_notifications_profile_id` no campo `profile_id`.
    *   `idx_notif_unique_user_profile_pncp` (UNIQUE) nos campos `user_id`, `profile_id` e `numero_controle_pncp` para evitar notificações duplicadas.
*   **`notification_logs`**: `idx_logs_notification_id` no campo `notification_id`.
*   **`api_call_logs`**:
    *   `idx_api_call_endpoint` no campo `endpoint`.
    *   `idx_api_call_created_at` no campo `created_at` (decrescente).

## Funções e Triggers

### `update_timestamp()`

Esta função PL/pgSQL é responsável por atualizar automaticamente o campo `updated_at` de uma tabela para a data e hora atuais sempre que um registro é modificado.

```sql
CREATE OR REPLACE FUNCTION public.update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

**Triggers Associados:**

*   `trg_users_updated`: Executado `BEFORE UPDATE` na tabela `users`.
*   `trg_profiles_updated`: Executado `BEFORE UPDATE` na tabela `interest_profiles`.

## Inicialização do Banco de Dados

O banco de dados é inicializado automaticamente ao subir a stack Docker. O script `db/init.sql` é executado pelo serviço `postgres` na primeira vez que o container é criado. Certifique-se de que o arquivo `.env` esteja configurado corretamente com as variáveis de ambiente do PostgreSQL.

Para iniciar a stack e criar o banco de dados, utilize os seguintes comandos na raiz do projeto:

```bash
cp .env.example .env # Se ainda não o fez
make build
make up
```

Para acessar o shell do PostgreSQL e verificar as tabelas e funções:

```bash
make db-shell
```

