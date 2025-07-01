# Especificação de Banco de Dados e Infraestrutura de Filas - nRadar

## 🎯 PostgreSQL

### Schemas

- `public`: padrão, para entidades principais do sistema.

---

### Tabelas

#### 1. users

| Campo           | Tipo            | Restrições                   | Descrição                       |
|-----------------|-----------------|------------------------------|---------------------------------|
| id              | UUID            | PK, DEFAULT gen_random_uuid()| Identificador único             |
| email           | VARCHAR(255)    | UNIQUE, NOT NULL             | E-mail do usuário               |
| password_hash   | VARCHAR(255)    | NOT NULL                     | Hash da senha                   |
| is_active       | BOOLEAN         | DEFAULT TRUE                 | Usuário ativo                   |
| is_superuser    | BOOLEAN         | DEFAULT FALSE                | Permissão de admin              |
| created_at      | TIMESTAMP       | DEFAULT now()                | Data de criação                 |
| updated_at      | TIMESTAMP       | DEFAULT now()                | Última atualização              |

#### 2. interest_profiles

| Campo                  | Tipo            | Restrições                   | Descrição                       |
|------------------------|-----------------|------------------------------|---------------------------------|
| id                     | UUID            | PK, DEFAULT gen_random_uuid()| Identificador único             |
| user_id                | UUID            | FK users(id), NOT NULL       | Dono do perfil                  |
| nome_perfil            | VARCHAR(100)    | NOT NULL                     | Nome do perfil                  |
| palavras_chave         | JSONB           | NOT NULL                     | Lista de palavras-chave         |
| uf                     | CHAR(2)         |                              | Unidade Federativa              |
| municipio_ibge         | VARCHAR(10)     |                              | Código IBGE do município        |
| modalidade_contratacao | VARCHAR(10)     |                              | Código modalidade (opcional)    |
| categoria              | VARCHAR(50)     |                              | Categoria                       |
| prioridade_urgencia    | VARCHAR(20)     | NOT NULL                     | urgente, proximaSemana, qualquerPrazo |
| notificacao_push       | BOOLEAN         | DEFAULT FALSE                | Notificação push                |
| notificacao_email      | BOOLEAN         | DEFAULT TRUE                 | Notificação por e-mail          |
| created_at             | TIMESTAMP       | DEFAULT now()                | Data de criação                 |
| updated_at             | TIMESTAMP       | DEFAULT now()                | Última atualização              |

#### 3. notifications

| Campo                | Tipo            | Restrições                   | Descrição                       |
|----------------------|-----------------|------------------------------|---------------------------------|
| id                   | UUID            | PK, DEFAULT gen_random_uuid()| Identificador único             |
| user_id              | UUID            | FK users(id), NOT NULL       | Usuário notificado              |
| profile_id           | UUID            | FK interest_profiles(id)     | Perfil relacionado              |
| numero_controle_pncp | VARCHAR(50)     | NOT NULL                     | Identificador da oportunidade   |
| tipo                 | VARCHAR(10)     | NOT NULL                     | push/email                      |
| enviado_em           | TIMESTAMP       | DEFAULT now()                | Data/hora do envio              |
| status               | VARCHAR(20)     | DEFAULT 'sent'               | sent, failed, pending           |
| conteudo             | JSONB           |                              | Dados da notificação            |

#### 4. notification_logs

| Campo                | Tipo            | Restrições                   | Descrição                       |
|----------------------|-----------------|------------------------------|---------------------------------|
| id                   | BIGSERIAL       | PK                           |                                 |
| notification_id      | UUID            | FK notifications(id)         | Notificação relacionada         |
| log                  | JSONB           |                              | Log estruturado                 |
| created_at           | TIMESTAMP       | DEFAULT now()                |                                 |

#### 5. api_call_logs

| Campo                | Tipo            | Restrições                   | Descrição                       |
|----------------------|-----------------|------------------------------|---------------------------------|
| id                   | BIGSERIAL       | PK                           |                                 |
| endpoint             | VARCHAR(255)    | NOT NULL                     | Endpoint chamado                |
| params               | JSONB           |                              | Parâmetros usados               |
| response_status      | INTEGER         |                              | Código HTTP                     |
| response_time_ms     | INTEGER         |                              | Tempo de resposta (ms)          |
| created_at           | TIMESTAMP       | DEFAULT now()                |                                 |

---

### Índices

```sql
-- users
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- interest_profiles
CREATE INDEX idx_profiles_user ON interest_profiles(user_id);
CREATE INDEX idx_profiles_palavras_chave ON interest_profiles USING GIN(palavras_chave);

-- notifications
CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_profile ON notifications(profile_id);
CREATE UNIQUE INDEX idx_notif_unique ON notifications(user_id, profile_id, numero_controle_pncp);

-- notification_logs
CREATE INDEX idx_logs_notification ON notification_logs(notification_id);

-- api_call_logs
CREATE INDEX idx_api_call_endpoint ON api_call_logs(endpoint);
```

---

### Funções/Triggers

```sql
-- Atualiza updated_at automaticamente
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trg_profiles_updated
BEFORE UPDATE ON interest_profiles
FOR EACH ROW EXECUTE FUNCTION update_timestamp();
```

---

### Exemplo de Consulta: Oportunidades já notificadas

```sql
SELECT numero_controle_pncp
FROM notifications
WHERE user_id = $1 AND profile_id = $2;
```

---

## 🚦 Redis

- **Broker Celery:** `redis://localhost:6379/0`
- **Uso:** Fila de tarefas assíncronas (Celery), cache de tokens JWT (opcional), rate limit.

### Estrutura Recomendada

- **Chaves de Celery:** `celery*` (default)
- **Chaves de Rate Limit:** `ratelimit:{user_id}` → contador expira em 1h
- **Chaves de JWT Blacklist (opcional):** `jwt_blacklist:{jti}`

---

## ⏰ Celery

- **Fila padrão:** `default`
- **Tarefas:** 
  - `executar_radar`: Busca e notifica oportunidades
  - `enviar_email`: Envio de e-mails assíncronos
  - `enviar_push`: Envio de notificações push

### Exemplo de Configuração

```python
from celery import Celery

app = Celery('radar', broker='redis://localhost:6379/0')

@app.task
def executar_radar():
    # ...chama lógica de monitoramento...

@app.task
def enviar_email(to, subject, body):
    # ...envio de e-mail...

@app.task
def enviar_push(user_id, payload):
    # ...envio de push...
```

#### Beat Schedule (Agendamento)

```python
from celery.schedules import crontab
app.conf.beat_schedule = {
    'executar-radar-cada-30-min': {
        'task': 'executar_radar',
        'schedule': crontab(minute='*/30')
    }
}
```

---

## 📝 Observações

- Todas as tabelas usam UUID como PK para escalabilidade.
- JSONB para flexibilidade em palavras-chave e logs.
- Índices GIN para buscas rápidas em arrays/JSONB.
- Triggers para manter `updated_at` atualizado.
- Redis pode ser expandido para cache de sessões, tokens, etc.
- Celery pode ser escalado horizontalmente conforme demanda.

---
