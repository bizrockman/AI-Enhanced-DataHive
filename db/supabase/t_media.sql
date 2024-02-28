CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- Aktiviert die Unterstützung für UUID-Funktionen in PostgreSQL

CREATE TABLE t_media (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(), -- Generiert automatisch eine neue UUID für jede Zeile
    media_url VARCHAR(255),
    media_b64_content TEXT,
    media_type VARCHAR(50) NOT NULL,
    title VARCHAR(255),
    description TEXT,
    likes INTEGER DEFAULT 0,
    hearts INTEGER DEFAULT 0,
    prompt TEXT,
    model VARCHAR(255),
    author VARCHAR(255),
    tags TEXT,
    source VARCHAR(255),
    reference_url VARCHAR(255),
    media_reference_id UUID, -- Referenz als UUID; könnte ein Fremdschlüssel sein
    media_created_at TIMESTAMP WITHOUT TIME ZONE,
    creator VARCHAR(255) NOT NULL,
    version INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Fremdschlüsselbeziehung definieren, wenn media_reference_id auf eine andere Zeile in derselben Tabelle verweisen soll
ALTER TABLE t_media ADD CONSTRAINT fk_media_reference FOREIGN KEY (media_reference_id) REFERENCES t_media(id) ON DELETE SET NULL;