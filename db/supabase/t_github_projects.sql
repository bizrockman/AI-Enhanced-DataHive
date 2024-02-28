CREATE TABLE t_github_projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    description TEXT,
    program_language VARCHAR(255),
    total_stars INTEGER,
    forks INTEGER,
    new_stars INTEGER,
    contributors TEXT,
    since VARCHAR(50) NOT NULL,
    tags TEXT,
    creator VARCHAR(255) NOT NULL,
    version INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT (CURRENT_TIMESTAMP AT TIME ZONE 'UTC')
);