-- init_postgres.sql
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL
);

INSERT INTO usuarios (nombre, email) VALUES
('alice', 'alice@example.com'),
('bob', 'bob@example.com'),
('admin', 'admin@local');
