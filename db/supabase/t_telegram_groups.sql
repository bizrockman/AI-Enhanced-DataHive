create table t_telegram_groups (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_group_name character varying null,
    telegram_group_chat_id bigint null,
    created_at timestamp with time zone not null default now()
)