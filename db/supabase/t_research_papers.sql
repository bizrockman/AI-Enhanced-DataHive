create table t_research_papers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title text null,
  abstract text null,
  source_id text,
  authors text,
  license text null,
  paper_url character varying(255) null,
  code_url character varying(255) null,
  media_url character varying(255) null,
  reference_url character varying(255) null,
  paper_submitted_at timestamp with time zone null,
  source character varying(255) null,
  version integer null default 0,
  tags text null,
  creator character varying(255) null,
  created_at timestamp with time zone null default current_timestamp,
  updated_at timestamp with time zone null default current_timestamp
)