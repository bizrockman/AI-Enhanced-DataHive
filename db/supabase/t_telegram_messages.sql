CREATE TABLE t_telegram_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    t_telegram_group_topic_id uuid null default gen_random_uuid (),
    content text null,
    media_content text null,
    media_url text null,
    media_type character varying(50) null,
    scheduled_for timestamp with time zone null,
    sent_at timestamp with time zone null,
    status character varying(50) null default 'planned'::character varying,
    created_at timestamp with time zone null default current_timestamp,
    updated_at timestamp with time zone null,
    creator character varying(255) null,
  )