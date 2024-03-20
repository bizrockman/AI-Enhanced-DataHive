create table t_content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title text null,
    content text null,
    media_url text null,
    media_type character varying(50) null,
    media_created_at timestamp with time zone null,
    reference_url text null,
    reference_type character varying(50) null,
    reference_created_at timestamp with time zone null,
    version integer null default 0,
    created_at timestamp with time zone null default current_timestamp,
    updated_at timestamp with time zone null,
    creator character varying(255) null,
    scheduled_for timestamp with time zone null,
    tags text null
);
