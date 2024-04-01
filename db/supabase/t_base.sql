based fields for all content tables:

Base Model:
id: Optional[Union[str, int]] = None
created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

Content Base Model:
creator: str
source_name: str
source_url: Optional[HttpUrl] = None
version: int = 0
language: str = 'en'
tags: str


id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
<Fields>
creator VARCHAR(255) NOT NULL,
source_name VARCHAR(255) NOT NULL,
source_url VARCHAR(255),
version INTEGER DEFAULT 0,
lang VARCHAR(2) DEFAULT 'en',
tags TEXT,
created_at timestamp with time zone null default (now() at time zone 'utc'::text),
updated_at timestamp with time zone null default (now() at time zone 'utc'::text)