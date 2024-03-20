create table t_content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    t_telegram_group_id uuid null,
    group_topic_name character varying null,
    telegram_group_topic_id bigint null,
    created_at timestamp with time zone not null default now(),
)