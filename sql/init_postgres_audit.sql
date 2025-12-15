-- Usuario de aplicación con privilegios mínimos
CREATE ROLE appuser LOGIN PASSWORD 'Fuerte#2025';

GRANT CONNECT ON DATABASE postgres TO appuser;
GRANT USAGE ON SCHEMA public TO appuser;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO appuser;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO appuser;

-- Auditoría / logging básico
ALTER SYSTEM SET log_connections = 'on';
ALTER SYSTEM SET log_disconnections = 'on';
ALTER SYSTEM SET log_statement = 'mod'; -- log de DML (INSERT/UPDATE/DELETE)
ALTER SYSTEM SET ssl = 'on';
ALTER SYSTEM SET ssl_cert_file = 'server.crt';
ALTER SYSTEM SET ssl_key_file = 'server.key';

-- (Opcional) Si pgaudit está disponible
-- ALTER SYSTEM SET shared_preload_libraries = 'pgaudit';
-- ALTER SYSTEM SET pgaudit.log = 'read, write, ddl';
