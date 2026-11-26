CREATE TABLE IF NOT EXISTS accounts (
    username TEXT PRIMARY KEY,
    organization TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('requester', 'support'))
);

CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY,
    organization TEXT NOT NULL,
    author TEXT NOT NULL REFERENCES accounts(username),
    title TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('OPEN', 'ASSIGNED', 'CLOSED')),
    assignee TEXT REFERENCES accounts(username),
    closed_at TEXT
);

CREATE TABLE IF NOT EXISTS ticket_history (
    id INTEGER PRIMARY KEY,
    ticket_id INTEGER NOT NULL REFERENCES tickets(id),
    event TEXT NOT NULL,
    actor TEXT NOT NULL REFERENCES accounts(username),
    happened_at TEXT NOT NULL
);
