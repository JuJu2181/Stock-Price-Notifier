DROP TABLE IF EXISTS subscribers;

CREATE TABLE subscribers(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email TEXT NOT NULL UNIQUE,
    phone_number TEXT NOT NULL,
    symbol TEXT NOT NULL,
    threshold FLOAT NOT NULL,
    frequency TEXT NOT NULL,
    notification_mode TEXT NOT NULL
);